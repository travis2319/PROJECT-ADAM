# from fastapi import APIRouter, Depends, HTTPException
# from utils.database import Database
# import pandas as pd

# # Router setup
# router = APIRouter(
#     prefix="/engine-health",
#     tags=["Engine Health"],
# )

# # Database instance (connection string should match your environment)
# db_instance = Database("postgresql://postgres:mysecretpassword@db:5432/mydb")

# @router.get("/data")
# def fetch_engine_health_data():
#     """
#     Fetch all data related to engine health from the database.
#     """
#     try:
#         data = db_instance.fetch_all_data("engine_health_table")  # Replace with the actual table name
#         return {"data": data.to_dict(orient="records")}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
