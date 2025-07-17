"""
dependencies.py
Defines FastAPI dependencies for database access.
"""

from fastapi import Depends
from .database import get_dynamodb_resource

def get_db():
    """
    Dependency that provides a DynamoDB resource instance.
    """
    return get_dynamodb_resource()
