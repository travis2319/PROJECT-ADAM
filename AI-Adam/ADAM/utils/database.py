# utils/database.py
from psycopg2 import pool
from contextlib import contextmanager

class DatabaseConfig:
    DB_HOST = "localhost"
    DB_PORT = "5432"
    DB_NAME = "mydb"
    DB_USER = "postgres"
    DB_PASSWORD = "mysecretpassword"
    MIN_CONNECTIONS = 1
    MAX_CONNECTIONS = 20

class Database:
    _pool = None

    @classmethod
    def initialize(cls):
        if cls._pool is None:
            cls._pool = pool.ThreadedConnectionPool(
                DatabaseConfig.MIN_CONNECTIONS,
                DatabaseConfig.MAX_CONNECTIONS,
                host=DatabaseConfig.DB_HOST,
                port=DatabaseConfig.DB_PORT,
                database=DatabaseConfig.DB_NAME,
                user=DatabaseConfig.DB_USER,
                password=DatabaseConfig.DB_PASSWORD
            )
    
    @classmethod
    def get_connection(cls):
        if cls._pool is None:
            cls.initialize()
        return cls._pool.getconn()
    
    @classmethod
    def return_connection(cls, conn):
        cls._pool.putconn(conn)
    
    @classmethod
    def close_all(cls):
        if cls._pool is not None:
            cls._pool.closeall()
            cls._pool = None

    @classmethod
    @contextmanager
    def get_db(cls):
        conn = cls.get_connection()
        try:
            yield conn
        finally:
            cls.return_connection(conn)

# #Utils/database.py 
# import os
# import pandas as pd
# import psycopg2
# from psycopg2 import sql, OperationalError

# # Environment variables for database connection
# POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
# POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
# POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
# POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "mysecretpassword")
# POSTGRES_DB = os.getenv("POSTGRES_DB", "mydb")

# def connect_to_db():
#     try:
#         conn = psycopg2.connect(
#             host=POSTGRES_HOST,
#             port=POSTGRES_PORT,
#             user=POSTGRES_USER,
#             password=POSTGRES_PASSWORD,
#             dbname=POSTGRES_DB
#         )
#         print("Database connected successfully!")
#         return conn
#     except OperationalError as e:
#         raise Exception(f"Database connection failed: {e}")

# def fetch_table_data(columns):
#     conn = None
#     try:
#         print("connecting to db to fetch tables.....")
#         conn = connect_to_db()
#         with conn.cursor() as cursor:
#             # Build the query dynamically to fetch only the specified columns
#             query = sql.SQL("SELECT {fields} FROM obdtest").format(
#                 fields=sql.SQL(", ").join(map(sql.Identifier, columns))
#             )
#             cursor.execute(query)
#             rows = cursor.fetchall()

#             # Extract column names and format data as dictionaries
#             colnames = [desc[0] for desc in cursor.description]
#             print(colnames)
#             return [dict(zip(colnames, row)) for row in rows]
#     except Exception as e:
#         raise Exception(f"Error fetching data from database: {e}")
#     finally:
#         if conn:
#             conn.close()
#             print("Database connection closed.")

# def fetch_raw_data():
#     """
#     Fetch all data from the 'obdtest' table and return as a Pandas DataFrame.
#     """
#     conn = None
#     try:
#         print("connecting to db.....")
#         conn = connect_to_db()
#         query = "SELECT * FROM obdtest"
#         df = pd.read_sql_query(query, conn)
#         print(f"Fetched {len(df)} rows from 'obdtest'.")
#         return df
#     except Exception as e:
#         raise Exception(f"Error fetching raw data: {e}")
#     finally:
#         if conn:
#             conn.close()
#             print("Database connection closed.")