#%%
import boto3
from dotenv import load_dotenv
import os

load_dotenv()

client = boto3.client(
    's3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("region_name"),
    endpoint_url=os.getenv("endpoint_url")
)

response = client.list_objects(Bucket=os.getenv("BUCKET_NAME"))
#%%