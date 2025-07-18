
"""
models.py
Pydantic models for User and Event data structures.
"""

from pydantic import BaseModel
from typing import List, Optional

class User(BaseModel):
    """
    Data model for a user.
    """
    id: str
    firstName: str
    lastName: str
    phoneNumber: Optional[str]
    email: str
    avatar: Optional[str]
    gender: Optional[str]
    job_title: Optional[str]
    company: Optional[str]
    city: Optional[str]
    state: Optional[str]
    events_hosted: List[str] = []
    events_attended: List[str] = []

class Event(BaseModel):
    """
    Data model for an event.
    """
    id: str
    slug: str
    title: str
    description: Optional[str]
    startAt: str
    endAt: str
    venue: Optional[str]
    maxCapacity: int
    owner: str
    hosts: List[str] = []
