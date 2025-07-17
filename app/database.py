
"""
database.py
Handles DynamoDB connection setup and provides resource access.
"""

import boto3
import os
from dotenv import load_dotenv

load_dotenv()

DYNAMODB_LOCAL_URL = os.environ["DYNAMODB_LOCAL_URL"]
AWS_REGION = os.environ["AWS_DEFAULT_REGION"]

def get_dynamodb_resource():
    """
    Returns a DynamoDB resource instance (local or AWS).
    """
    return boto3.resource(
        'dynamodb',
        region_name=AWS_REGION,
        endpoint_url=DYNAMODB_LOCAL_URL,
        aws_access_key_id='dummy',  # Any value for local
        aws_secret_access_key='dummy'  # Any value for local
    )
