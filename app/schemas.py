from pydantic import BaseModel
from typing import List, Optional

# Event schemas
class EventCreate(BaseModel):
    slug: str
    title: str
    description: Optional[str] = None
    startAt: str
    endAt: str
    venue: Optional[str] = None
    maxCapacity: int
    owner: str
    hosts: List[str] = []

class EventOut(BaseModel):
    id: str
    slug: str
    title: str
    description: Optional[str]
    startAt: str
    endAt: str
    venue: Optional[str]
    maxCapacity: int
    owner: str
    hosts: List[str]
    attendees: List[str] = []

# User schemas
class UserCreate(BaseModel):
    firstName: str
    lastName: str
    email: str
    phoneNumber: Optional[str] = None
    avatar: Optional[str] = None
    gender: Optional[str] = None
    job_title: Optional[str] = None
    company: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None

class UserOut(BaseModel):
    id: str
    firstName: str
    lastName: str
    email: str
    company: Optional[str]
    job_title: Optional[str]
    city: Optional[str]
    state: Optional[str]
    events_hosted: List[str]
    events_attended: List[str]

class UserFilter(BaseModel):
    company: Optional[str]
    job_title: Optional[str]
    city: Optional[str]
    state: Optional[str]
    events_hosted_min: Optional[int] = None
    events_hosted_max: Optional[int] = None
    events_attended_min: Optional[int] = None
    events_attended_max: Optional[int] = None
    sort_by: Optional[str]
    skip: int = 0
    limit: int = 10
