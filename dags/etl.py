from airflow import DAG
from airflow.decorators import task
from datetime import datetime, timedelta
import requests
import pandas as pd
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

default_args = {
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    dag_id='ETL_Basic',
    start_date=datetime(2025, 7, 29),
    schedule="@daily",
    end_date=datetime(2025, 7, 31),
    default_args=default_args,
    catchup=False,
    description='ETL Pipeline Basics',
) as dag:

    @task
    def extract():
        url = 'http://universities.hipolabs.com/search?country=United+States'
        data = requests.get(url).json()
        return data

    @task
    def transform(data):
        df = pd.DataFrame(data)
        df = df[df['name'].str.contains('California')]
        df['domains'] = df['domains'].apply(lambda x: ','.join(x))
        df['web_pages'] = df['web_pages'].apply(lambda x: ','.join(x))
        df = df.reset_index(drop=True)
        return df.to_json(orient='records')  # ✅ Trả về JSON chuỗi (để tránh lỗi dict lớn)

    @task
    def load(df_json):
        df = pd.read_json(df_json)  # ✅ Đọc lại từ chuỗi JSON
        DB_USER = os.getenv('DB_USER')
        DB_PASSWORD = os.getenv('DB_PASSWORD')
        DB_HOST = os.getenv('DB_HOST')
        DB_PORT = os.getenv('DB_PORT')
        DB_DATABASE = os.getenv('DB_DATABASE')

        engine = create_engine(
            f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}'
        )

        df.to_sql('cal_uni', engine, if_exists='replace', index=False)

    # ✅ Cách chaining chuẩn
    raw_data = extract()
    transformed = transform(raw_data)
    load(transformed)
