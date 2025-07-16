import boto3
import os
from dotenv import load_dotenv

load_dotenv()

DYNAMODB_LOCAL_URL = os.getenv("DYNAMODB_LOCAL_URL", "http://localhost:8001")
AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

# Kết nối DynamoDB local

def get_dynamodb_resource():
    return boto3.resource(
        'dynamodb',
        region_name=AWS_REGION,
        endpoint_url=DYNAMODB_LOCAL_URL,
        aws_access_key_id='dummy',  # Dùng giá trị bất kỳ cho local
        aws_secret_access_key='dummy'  # Dùng giá trị bất kỳ cho local
    )
