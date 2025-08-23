from sqlalchemy import create_engine, inspect
from sqlalchemy.engine import Engine
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB

from urllib.parse import quote_plus


def get_engine() -> Engine:
    url = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
    return create_engine(url)



def get_schema_info(engine: Engine):
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    schema = {}
    for table in tables:
        columns = inspector.get_columns(table)
        fks = inspector.get_foreign_keys(table)
        schema[table] = {
            'columns': [col['name'] for col in columns],
            'foreign_keys': fks
        }
    return schema