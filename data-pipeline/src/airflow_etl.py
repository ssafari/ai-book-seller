from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine

# Define your database connection string
DATABASE_URI = "postgresql://user:password@host:port/database_name"

# Define default arguments
default_args = {
    "owner": "Sepehr Safari",                      # The owner of the project
    "start_date": days_ago(1),                     # The start date for the DAG
    "retries": 1,                                  # Number of retries in case of failure
    "retry_delay": timedelta(minutes=5),           # Time delay between retries
    "catchup": False                               # Prevent running backlogged DAGs
}

@dag(
    dag_id="taskflow_database_etl",
    #start_date=datetime(2025, 1, 1),
    schedule="@daily",
    default_args=default_args,
    catchup=False,
    tags=["books", "database"],
)
def taskflow_database_etl_dag():
    @task
    def extract_data_from_db():
        """
        Extracts data from a database table.
        """
        engine = create_engine(DATABASE_URI)
        query = "SELECT * FROM public.source_table;"
        df = pd.read_sql(query, engine)
        return df.to_json(orient="records") # Convert DataFrame to JSON string for XCom

    @task
    def transform_data(json_data):
        """
        Transforms the extracted data.
        """
        df = pd.read_json(json_data, orient="records")
        # Example transformation: add a new column
        df["transformed_value"] = df["original_value"] * 2
        return df.to_json(orient="records")

    @task
    def load_data_to_db(json_data):
        """
        Loads the transformed data into another database table.
        """
        df = pd.read_json(json_data, orient="records")
        engine = create_engine(DATABASE_URI)
        df.to_sql("public.target_table", engine, if_exists="append", index=False)
        print("Data loaded successfully to public.target_table")

    # Define the task flow
    extracted_data = extract_data_from_db()
    transformed_data = transform_data(extracted_data)
    load_data_to_db(transformed_data)

# Instantiate the DAG
taskflow_database_etl_dag()
