from langchain_community.agent_toolkits import create_sql_agent
from langchain_groq import ChatGroq
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_community.utilities.sql_database import SQLDatabase
from config import GROQ_API_KEY
from db_utils import get_engine


def get_sql_agent():
    engine = get_engine()
    db = SQLDatabase(engine)
    llm = ChatGroq(model="Gemma2-9b-It", groq_api_key=GROQ_API_KEY)
    agent = create_sql_agent(
        llm=llm,
        db=db,
        agent_type="openai-tools",
        verbose=True
    )
    return agent