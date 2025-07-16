from fastapi import Depends
from .database import get_dynamodb_resource

def get_db():
    return get_dynamodb_resource()
