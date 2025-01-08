from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd


# Database connection class
class Database:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.engine = create_engine(self.connection_string)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_session(self):
        """Provide a database session."""
        try:
            session = self.SessionLocal()
            yield session
        finally:
            session.close()

    def fetch_all_data(self, table_name):
        """Fetch all data from a table as a DataFrame."""
        query = f"SELECT * FROM {table_name}"
        with self.engine.connect() as connection:
            return pd.read_sql(query, connection)
