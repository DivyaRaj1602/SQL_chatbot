# Simple SQL Pipeline – Step 1: Single Table Queries

## 📌 Objective  
The goal of this project is to build a **natural language to SQL pipeline** that allows users to ask questions about their database in plain English and get relevant answers — without writing any SQL themselves.  
This version focuses on **basic single-table queries**, making it a simple and practical starting point for learning, prototyping, and interviews.

---

## ✨ What It Can Do (Current Capabilities)  
- **Natural Language to SQL**: Converts plain-English questions into SQL queries using a Large Language Model (LLM).  
- **Table Identification**: Automatically detects which table the question refers to.  
- **Schema Awareness**: Reads the database schema (tables and columns) to improve query accuracy.  
- **Safe SQL Execution**:  
  - Allows only `SELECT` queries.  
  - Blocks dangerous operations like `DROP`, `DELETE`, `INSERT`, `UPDATE`, etc.  
  - Validates query syntax before execution.  
- **Result Display**: Presents query results in a clean tabular format with row count.  
- **Interactive CLI**:  
  - `exit` → Quit the program.  
  - `schema` → Show the available tables and columns.  

---

## 🛠 Steps Taken to Ensure Reliability  
1. **Strict Query Safety Checks**  
   - Only runs `SELECT` queries.  
   - Detects and blocks harmful SQL commands.  
   - Checks for unbalanced quotes and parentheses.  

2. **Schema-Aware Querying**  
   - Reads database schema at startup.  
   - Provides table and column context to the LLM for accurate query generation.  

3. **Multi-Stage SQL Cleaning**  
   - Removes unwanted explanations from LLM output.  
   - Extracts only the SQL portion.  
   - Fixes formatting and quote issues.  

4. **Syntax Validation Before Execution**  
   - Uses `EXPLAIN` to verify SQL validity before running the actual query.  

5. **Clear Error Handling**  
   - Returns structured error messages for easier debugging.  

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
