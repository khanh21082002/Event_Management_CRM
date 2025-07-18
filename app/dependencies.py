"""
dependencies.py
Defines FastAPI dependencies for database access.
"""

"""
The file app/dependencies.py in the FastAPI project is often
used to declare and organize the dependencies used in the routes (endpoints) of the API. 
This is a way to reuse logic (such as database connections, authentication, logging, etc.) 
without having to repeat it in each route.
"""

from fastapi import Depends
from .database import get_dynamodb_resource

def get_db():
    """
    Dependency that provides a DynamoDB resource instance.
    """
    return get_dynamodb_resource()
