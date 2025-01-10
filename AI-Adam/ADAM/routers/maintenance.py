# from fastapi import APIRouter, HTTPException
# from utils.database import Database
# import pandas as pd

# # Router setup
# router = APIRouter(
#     prefix="/maintenance",
#     tags=["Predictive Maintenance"],
# )

# db_instance = Database("postgresql://postgres:mysecretpassword@db:5432/mydb")

# @router.get("/data")
# def fetch_maintenance_data():
#     """
#     Fetch all data related to car maintenance from the database.
#     """
#     try:
#         data = db_instance.fetch_all_data("maintenance_table")  # Replace with the actual table name
#         return {"data": data.to_dict(orient="records")}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
