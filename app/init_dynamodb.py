import boto3
import os
from dotenv import load_dotenv

load_dotenv()

DYNAMODB_LOCAL_URL = os.getenv("DYNAMODB_LOCAL_URL", "http://localhost:8001")
AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

dynamodb = boto3.resource(
    'dynamodb',
    region_name=AWS_REGION,
    endpoint_url=DYNAMODB_LOCAL_URL,
    aws_access_key_id='dummy',
    aws_secret_access_key='dummy'
)

table_name = 'users'

existing_tables = [t.name for t in dynamodb.tables.all()]
if table_name not in existing_tables:
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {'AttributeName': 'id', 'KeyType': 'HASH'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'id', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )
    table.wait_until_exists()
    print("Table created!")
else:
    print("Table already exists.")

# Tạo bảng events
event_table_name = 'events'
if event_table_name not in existing_tables:
    event_table = dynamodb.create_table(
        TableName=event_table_name,
        KeySchema=[
            {'AttributeName': 'id', 'KeyType': 'HASH'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'id', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )
    event_table.wait_until_exists()
    print("Event table created!")
else:
    print("Event table already exists.")
