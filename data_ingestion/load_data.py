#%%

import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import io
from extract_data import response,client

load_dotenv()

def transform_object(file_name:str):
    load_dotenv()
    response_object = client.get_object(Bucket=os.getenv("BUCKET_NAME"),Key=file_name)
    body_bytes = response_object["Body"].read()
    if body_bytes[:4] == b"PAR1":
        return pd.read_parquet(io.BytesIO(body_bytes),engine='pyarrow'),file_name

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("POSTGRES_DB")

URL_connection = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
print(URL_connection)
engine = create_engine(URL_connection)

files = [obj["Key"] for obj in response["Contents"]]

files_df = [transform_object(file_name) for file_name in files]

for file in files_df:
    df = file[0]
    file_name = file[1].split(".")[0]
    df.to_sql(name=file_name, con=engine,if_exists="replace",index=False)
# %%
