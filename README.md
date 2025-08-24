# Simple SQL Pipeline – Step 1: Single Table Queries

##📌 Objective

The goal of this project is to build an AI-powered SQL chatbot that allows users to query their database in natural language and instantly get both tabular results and interactive visualizations — without needing SQL or BI expertise.
This advanced version supports multi-table queries, automatic schema handling, and PowerBI-style dashboards.

✨ What It Can Do (Current Capabilities)
🔹 Natural Language → SQL
Converts plain-English questions into optimized MySQL queries using an LLM.
Supports multi-table joins, aggregations, CTEs, window functions, and date operations.
Schema-aware: Reads tables, columns, and relationships dynamically to improve accuracy.
Error handling: Auto-corrects invalid queries with retry logic.

🔹 Safe Query Execution
Only executes SELECT or WITH queries.
Blocks destructive SQL (DROP, DELETE, INSERT, UPDATE).
Validates queries before execution.

🔹 Interactive Data Visualizations
Generates charts directly from query results.
Supported commands:
auto → Let AI choose best chart
options → Show all chart types
pie category → Pie chart by category
histogram price → Distribution of numeric column
scatter x y → Correlation between two metrics
bar category → Bar chart by category
line date sales → Trends over time
box column → Distribution & outliers
heatmap → Correlation matrix
dashboard → Auto-generated multi-chart dashboard (PowerBI-style)
3d col1 col2 col3 → 3D scatter visualization

🔹 CLI Interaction
Conversational interface for asking questions.
Commands:
exit → Quit the program.
schema → Show tables & columns.
Visualization commands (listed above).
Prints both executed SQL and query results. 
---

##🛠 Steps Taken to Ensure Reliability

1.Strict Query Safety Checks
Executes only SELECT and WITH queries.
Blocks destructive SQL (DROP, DELETE, INSERT, UPDATE, ALTER).
Ensures SQL always starts with SELECT or WITH.

2.Dynamic Schema Awareness
Automatically inspects database schema (tables, columns, relationships).
Provides this schema context to the LLM for accurate query generation.
Supports multi-table joins by leveraging schema information.

3.Multi-Stage SQL Cleaning & Normalization
Extracts only the SQL query from raw LLM output.
Cleans extra text, explanations, or invalid tokens.
Normalizes column/table references and fixes formatting issues.

4.Pre-Execution Validation
Runs EXPLAIN to validate query syntax and execution plan.
Applies retry logic with schema hints if query fails.
Rejects unsafe or ambiguous queries.

5.Robust Error Handling & Feedback
Provides structured, human-readable error messages.
Suggests corrections (e.g., missing joins, invalid columns).
Prevents pipeline crashes with graceful fallbacks. 

---

## 🚀 How to Run  
1. **Set up your environment variables in `config.py`**  
   ```python
   GROQ_API_KEY = "your_groq_api_key"
   MYSQL_HOST = "localhost"
   MYSQL_USER = "root"
   MYSQL_PASSWORD = "password"
   MYSQL_DB = "your_database_name"
   ```
2. **Install dependencies**  
   ```bash
   pip install sqlalchemy pymysql langchain-groq
   ```
3. **Run the interactive CLI**  
   ```bash
   python simple_main.py
   ```

---

## 🖥 Example Usage  
```plaintext
🚀 Welcome to Simple SQL Pipeline - Step 1!
This version handles basic single-table queries.
Type 'exit' to quit, 'schema' to see tables.

💬 Ask me about your data: show me customers

✅ SUCCESS
Question: show me customers
Table: customers
SQL: SELECT * FROM customers
Found: 20 rows
```

---

## 📅 Next Steps  
- Support multi-table joins.  
- Add aggregation and grouping features.  
- Build a web-based UI.  
