# advanced_pipeline.py - Advanced SQL Pipeline with Full Database Support

from langchain_groq import ChatGroq
from sqlalchemy import create_engine, text, inspect
from config import GROQ_API_KEY, MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB
import re
from typing import List, Dict, Any, Optional


class AdvancedSQLPipeline:
    """
    Advanced SQL pipeline that handles complex queries including:
    - JOINs (INNER, LEFT, RIGHT, FULL)
    - UNIONs and UNION ALL
    - CTEs (Common Table Expressions)
    - Window Functions
    - Subqueries
    - Aggregations and GROUP BY
    - Complex WHERE conditions
    - And much more!
    """
    
    def __init__(self):
        """Initialize the advanced pipeline with database connection and LLM"""
        print("🚀 Setting up Advanced SQL Pipeline...")
        
        # Create database connection
        self.engine = self._create_db_connection()
        
        # Initialize the LLM (Large Language Model)
        self.llm = ChatGroq(
            api_key=GROQ_API_KEY, 
            model="llama3-8b-8192",
            temperature=0  # Low temperature for consistent results
        )
        
        # Get comprehensive database schema
        self.schema = self._get_comprehensive_schema()
        print(f"✅ Found {len(self.schema)} tables with full schema information")
        print("🚀 Advanced Pipeline ready for complex queries!")
    
    def _create_db_connection(self):
        """Create connection to MySQL database"""
        connection_url = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
        return create_engine(connection_url)
    
    def _get_comprehensive_schema(self) -> Dict[str, Dict[str, Any]]:
        """
        Get comprehensive schema information including:
        - Table names
        - Column names and types
        - Primary keys
        - Foreign keys
        - Indexes
        """
        inspector = inspect(self.engine)
        schema = {}
        
        for table_name in inspector.get_table_names():
            # Get detailed column information
            columns = inspector.get_columns(table_name)
            column_info = {}
            
            for col in columns:
                column_info[col['name']] = {
                    'type': str(col['type']),
                    'nullable': col['nullable'],
                    'default': col['default'],
                    'primary_key': col.get('primary_key', False)
                }
            
            # Get primary keys
            primary_keys = inspector.get_pk_constraint(table_name)
            pk_columns = primary_keys.get('constrained_columns', [])
            
            # Get foreign keys
            foreign_keys = inspector.get_foreign_keys(table_name)
            
            # Get indexes
            indexes = inspector.get_indexes(table_name)
            
            schema[table_name] = {
                'columns': column_info,
                'primary_keys': pk_columns,
                'foreign_keys': foreign_keys,
                'indexes': indexes,
                'column_names': list(column_info.keys())
            }
        
        return schema
    
    def process_query(self, user_question: str) -> Dict[str, Any]:
        """
        Main method: Convert user question to advanced SQL and get results
        
        Steps:
        1. Generate advanced SQL using LLM with full schema context
        2. Validate the SQL is safe
        3. Execute query and return results
        """
        print(f"\n📝 Processing: '{user_question}'")
        
        try:
            # Generate advanced SQL using LLM
            sql_query = self._generate_advanced_sql(user_question)
            print(f"🔧 Generated SQL: {sql_query}")
            
            # Validate the SQL is safe
            if not self._is_safe_sql(sql_query):
                return self._error_response("Generated SQL failed safety check")
            
            print(f"🔧 Final SQL to execute: '{sql_query}'")
            
            # Execute the query
            results = self._execute_query(sql_query)
            
            # Determine the main table(s) involved
            main_tables = self._extract_main_tables(sql_query)
            
            return {
                'success': True,
                'user_question': user_question,
                'target_table': ', '.join(main_tables) if main_tables else 'Multiple tables',
                'sql_query': sql_query,
                'results': results,
                'result_count': len(results)
            }
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return self._error_response(str(e))
    
    def _generate_advanced_sql(self, user_question: str) -> str:
        """
        Generate advanced SQL query using LLM with full schema context
        This method can handle complex queries with JOINs, CTEs, etc.
        """
        # Create a comprehensive schema description for the LLM
        schema_description = self._create_schema_description()
        
        prompt = f"""
        You are an expert SQL developer for MySQL database. Generate a SQL query based on the user's question.
        
        User Question: "{user_question}"
        
        Database Schema:
        {schema_description}
        
        Requirements:
        1. Return ONLY the SQL query, no explanations
        2. ALWAYS consult the schema above before generating SQL
        3. If the requested column does not exist in the mentioned table, 
        identify the correct table from the schema and JOIN using the foreign keys
        If the user asks for "category" or any field not directly in the base table, 
        look at the schema foreign keys to trace the correct relationship. 

        For example:
        - To get category from orders, you must JOIN orders → order_details → products → categories.
        - Never assume a column exists directly in orders if the schema does not list it.
        4. Use proper JOIN syntax when multiple tables are needed
        5. Support CTEs (WITH clauses) if they make the query clearer
        6. Support window functions if needed
        7. Use proper table aliases for clarity
        8. Handle complex WHERE conditions properly
        9. Use appropriate aggregation functions
        10. Start with SELECT statement
        11. Do not add a semicolon at the end
        12. Use MySQL syntax (NOT PostgreSQL)
        13. When aggregating data across multiple tables (e.g., counting orders by category), 
        avoid double-counting by using CTEs or DISTINCT as needed.
        14. If an order may appear multiple times due to joins with order_details or products, 
        use COUNT(DISTINCT order_id) or an intermediate CTE to ensure correct results.

        
        IMPORTANT: Use MySQL date functions:
        - Instead of DATE_TRUNC('month', date) use: DATE_FORMAT(date, '%Y-%m-01')
        - Instead of DATE_TRUNC('year', date) use: DATE_FORMAT(date, '%Y-01-01')
        - For date arithmetic use: DATE_ADD(), DATE_SUB(), INTERVAL
        - Use realistic date ranges: '1990-01-01' instead of '2020-01-01' for sample databases

        When the query requires information across multiple tables, 
        derive the JOINs from the foreign key relationships in the schema.
        Do NOT assume a column exists in a table if the schema does not list it.
        
        Examples of what you can generate:
        - Simple queries: SELECT * FROM customers
        - JOINs: SELECT c.name, o.order_date FROM customers c JOIN orders o ON c.id = o.customer_id
        - CTEs: WITH recent_orders AS (SELECT * FROM orders WHERE order_date > '1990-01-01') SELECT * FROM recent_orders
        - Window functions: SELECT *, ROW_NUMBER() OVER (PARTITION BY category_id ORDER BY price) as rn FROM products
        - Complex aggregations: SELECT category, COUNT(*), AVG(price) FROM products GROUP BY category HAVING COUNT(*) > 5
        - Date grouping: SELECT DATE_FORMAT(order_date, '%Y-%m-01') as month, COUNT(*) FROM orders GROUP BY month
        
        SQL Query:"""
        
        response = self.llm.invoke(prompt).content.strip()
        
        # Clean and extract the SQL
        sql = self._clean_advanced_sql(response)
        return sql
    
    def _create_schema_description(self) -> str:
        """Create a comprehensive schema description for the LLM"""
        description = []
        
        for table_name, table_info in self.schema.items():
            # Table header
            table_desc = [f"Table: {table_name}"]
            
            # Columns
            columns = []
            for col_name, col_info in table_info['columns'].items():
                col_type = col_info['type']
                nullable = "NULL" if col_info['nullable'] else "NOT NULL"
                pk = " (PK)" if col_info['primary_key'] else ""
                columns.append(f"  - {col_name}: {col_type} {nullable}{pk}")
            
            table_desc.extend(columns)
            
            # Foreign keys
            if table_info['foreign_keys']:
                fk_desc = ["  Foreign Keys:"]
                for fk in table_info['foreign_keys']:
                    fk_desc.append(f"    - {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}")
                table_desc.extend(fk_desc)
            
            description.append('\n'.join(table_desc))
        
        return '\n\n'.join(description)
    
    def _clean_advanced_sql(self, sql: str) -> str:
        """Clean up the generated advanced SQL query"""
        print(f"🔍 Raw LLM response: '{sql}'")
        
        # Remove markdown formatting
        sql = re.sub(r'```sql\n?|```\n?', '', sql)
        
        # Extract SQL if it doesn't start with SELECT
        if not sql.strip().upper().startswith('SELECT'):
            sql = self._extract_sql_from_advanced_response(sql)
        
        # Clean up whitespace and remove trailing semicolons
        sql = sql.strip().rstrip(';')
        
        # Normalize whitespace
        sql = ' '.join(sql.split())
        
        print(f"🧹 Cleaned SQL: '{sql}'")
        return sql
    
    def _extract_sql_from_advanced_response(self, response: str) -> str:
        """Extract SQL from LLM response that might contain explanations"""
        
        # First, try to extract the complete SQL query
        # Look for SQL between markdown code blocks
        sql_match = re.search(r'```(?:sql)?\s*\n?(.*?)\n?```', response, re.DOTALL | re.IGNORECASE)
        if sql_match:
            sql = sql_match.group(1).strip()
            print(f"🔍 Extracted from code blocks: '{sql}'")
            return sql
        
        # Check if the response is already pure SQL (contains SQL keywords)
        response_upper = response.upper()
        if any(keyword in response_upper for keyword in ['SELECT', 'WITH', 'FROM', 'JOIN']):
            # Try to extract just the SQL part
            sql_match = re.search(r'(SELECT\s+.+|WITH\s+.+)', response, re.IGNORECASE | re.DOTALL)
            if sql_match:
                clean_response = sql_match.group(1).strip()
                print(f"🔍 Extracted SQL from response: '{clean_response}'")
                return clean_response
            else:
                # Fallback: remove explanatory text and keep SQL
                clean_response = response.strip().rstrip(';').strip()
                print(f"🔍 Using raw response as SQL: '{clean_response}'")
                return clean_response
        
        # Fallback: return the original response
        print(f"🔍 No SQL detected, returning original: '{response.strip()}'")
        return response.strip()
    
    def _is_safe_sql(self, sql: str) -> bool:
        """
        Enhanced safety check for advanced SQL queries
        """
        sql_upper = sql.upper().strip()
        
        # Must start with SELECT, WITH, or be a valid CTE
        if not (sql_upper.startswith('SELECT') or sql_upper.startswith('WITH')):
            print("❌ SQL must start with SELECT or WITH")
            return False
        
        # Check for dangerous operations
        dangerous_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'CREATE', 'ALTER', 'TRUNCATE', 'EXEC', 'EXECUTE']
        for keyword in dangerous_keywords:
            if keyword in sql_upper:
                print(f"❌ Dangerous keyword '{keyword}' found")
                return False
        
        # Check for multiple statements (should be single query)
        if ';' in sql:
            print("❌ Multiple statements not allowed")
            return False
        
        print("✅ SQL passed safety checks")
        return True
    
    def _execute_query(self, sql: str) -> List[Dict[str, Any]]:
        """Execute the SQL query and return results"""
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text(sql))
                columns = result.keys()
                rows = result.fetchall()
                
                # Convert to list of dictionaries
                results = []
                for row in rows:
                    row_dict = {}
                    for i, col in enumerate(columns):
                        row_dict[col] = row[i]
                    results.append(row_dict)
                
                return results
                
        except Exception as e:
            print(f"❌ SQL execution failed: {e}")
            raise e
    
    def _extract_main_tables(self, sql: str) -> List[str]:
        """Extract the main tables involved in the query"""
        # Simple regex to find table names after FROM and JOIN
        table_pattern = r'(?:FROM|JOIN|LEFT\s+JOIN|RIGHT\s+JOIN|INNER\s+JOIN|FULL\s+JOIN)\s+(\w+)'
        tables = re.findall(table_pattern, sql, re.IGNORECASE)
        
        # Remove duplicates and return
        return list(set(tables))
    
    def show_schema(self):
        """Display the database schema in a readable format"""
        print("\n📊 Database Schema:")
        print("=" * 60)
        
        for table_name, table_info in self.schema.items():
            print(f"\n🏷️  Table: {table_name}")
            print("-" * 40)
            
            # Show columns
            for col_name, col_info in table_info['columns'].items():
                pk_marker = " 🔑" if col_info['primary_key'] else ""
                nullable = "NULL" if col_info['nullable'] else "NOT NULL"
                print(f"  📝 {col_name}: {col_info['type']} {nullable}{pk_marker}")
            
            # Show foreign keys
            if table_info['foreign_keys']:
                print("  🔗 Foreign Keys:")
                for fk in table_info['foreign_keys']:
                    print(f"    → {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}")
        
        print("=" * 60)
    
    def _error_response(self, error_message: str) -> Dict[str, Any]:
        """Create an error response"""
        return {
            'success': False,
            'user_question': '',
            'target_table': '',
            'sql_query': '',
            'results': [],
            'result_count': 0,
            'error': error_message
        }
