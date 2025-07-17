"""
service.py
Business logic for user, event, registration, filtering, analytics, and email log operations using DynamoDB.
"""


import logging
from .models import User, Event
from .schemas import UserFilter, UserCreate, UserOut
from typing import List, Optional
import uuid

# Configure logging
logger = logging.getLogger("event_crm")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
handler.setFormatter(formatter)
if not logger.hasHandlers():
    logger.addHandler(handler)


def get_user(db, user_id):
    """
    Retrieve a user by user_id from the users table.
    """
    table = db.Table('users')
    response = table.get_item(Key={'id': user_id})
    item = response.get('Item')
    if not item:
        raise Exception('User not found')
    item['events_hosted'] = item.get('events_hosted', [])
    item['events_attended'] = item.get('events_attended', [])
    return UserOut(**item)

def update_user(db, user_id, user: UserCreate):
    """
    Update a user's information by user_id.
    """
    table = db.Table('users')
    user_dict = user.dict()
    user_dict['id'] = user_id
    user_dict['events_hosted'] = []
    user_dict['events_attended'] = []
    table.put_item(Item=user_dict)
    return UserOut(**user_dict)

def delete_user(db, user_id):
    """
    Delete a user by user_id.
    """
    table = db.Table('users')
    table.delete_item(Key={'id': user_id})
    return {"status": "deleted"}

def get_event(db, event_id):
    """
    Retrieve an event by event_id from the events table.
    """
    table = db.Table('events')
    response = table.get_item(Key={'id': event_id})
    item = response.get('Item')
    if not item:
        raise Exception('Event not found')
    item['hosts'] = item.get('hosts', [])
    item['attendees'] = item.get('attendees', [])
    return item

def update_event(db, event_id, event):
    """
    Update an event's information by event_id.
    """
    table = db.Table('events')
    event_dict = event.dict()
    event_dict['id'] = event_id
    event_dict['attendees'] = []
    table.put_item(Item=event_dict)
    return event_dict

def delete_event(db, event_id):
    """
    Delete an event by event_id.
    """
    table = db.Table('events')
    table.delete_item(Key={'id': event_id})
    return {"status": "deleted"}

def get_email_logs(db):
    """
    Retrieve all email logs from the email_logs table.
    """
    table = db.Table('email_logs')
    response = table.scan()
    return response.get('Items', [])

def get_all_users(db):
    """
    Retrieve all users from the users table.
    """
    table = db.Table('users')
    response = table.scan()
    items = response.get('Items', [])
    # Convert DynamoDB items to UserOut
    users = []
    for item in items:
        # Ensure events_hosted and events_attended are lists
        item['events_hosted'] = item.get('events_hosted', [])
        item['events_attended'] = item.get('events_attended', [])
        users.append(UserOut(**item))
    return users

def create_event(db, event):
    """
    Create a new event and update the events_hosted list for the owner and hosts.
    """
    import uuid
    table = db.Table('events')
    event_id = str(uuid.uuid4())
    event_dict = event.dict()
    event_dict['id'] = event_id
    event_dict['attendees'] = []
    table.put_item(Item=event_dict)
    # Update events_hosted for the owner
    user_table = db.Table('users')
    owner_id = event.owner
    user_table.update_item(
        Key={'id': owner_id},
        UpdateExpression='SET events_hosted = list_append(if_not_exists(events_hosted, :empty), :e)',
        ExpressionAttributeValues={':e': [event_id], ':empty': []}
    )
    # Update events_hosted for each host
    for host_id in event.hosts:
        user_table.update_item(
            Key={'id': host_id},
            UpdateExpression='SET events_hosted = list_append(if_not_exists(events_hosted, :empty), :e)',
            ExpressionAttributeValues={':e': [event_id], ':empty': []}
        )
    return event_dict

def list_events(db):
    """
    Retrieve all events from the events table.
    """
    table = db.Table('events')
    response = table.scan()
    items = response.get('Items', [])
    return items

def register_event(db, event_id, user_id):
    """
    Register a user for an event. Adds user to event's attendees and event to user's events_attended.
    """
    event_table = db.Table('events')
    user_table = db.Table('users')
    # add user to event's attendees
    event_table.update_item(
        Key={'id': event_id},
        UpdateExpression='SET attendees = list_append(if_not_exists(attendees, :empty), :u)',
        ExpressionAttributeValues={':u': [user_id], ':empty': []}
    )
    # add event to user's events_attended
    user_table.update_item(
        Key={'id': user_id},
        UpdateExpression='SET events_attended = list_append(if_not_exists(events_attended, :empty), :e)',
        ExpressionAttributeValues={':e': [event_id], ':empty': []}
    )
    return {'event_id': event_id, 'user_id': user_id, 'status': 'registered'}

def user_engagement_analytics(db):
    """
    Generate analytics for user engagement (number of events hosted/attended).
    """
    user_table = db.Table('users')
    response = user_table.scan()
    items = response.get('Items', [])
    result = []
    for item in items:
        result.append({
            'user_id': item['id'],
            'firstName': item.get('firstName'),
            'lastName': item.get('lastName'),
            'events_hosted': len(item.get('events_hosted', [])),
            'events_attended': len(item.get('events_attended', []))
        })
    return result

def create_user(db, user: UserCreate):
    """
    Create a new user in the users table.
    """
    user_id = str(uuid.uuid4())
    user_dict = user.dict()
    user_dict["id"] = user_id
    user_dict["events_hosted"] = []
    user_dict["events_attended"] = []
    table = db.Table('users')
    table.put_item(Item=user_dict)
    return UserOut(**user_dict)

def filter_users(db, company, job_title, city, state, events_hosted_min, events_hosted_max, events_attended_min, events_attended_max, skip, limit, sort_by):
    """
    Filter users by company, job title, city, state, number of events hosted/attended, with sorting and pagination.
    """
    table = db.Table('users')
    response = table.scan()
    items = response.get('Items', [])
    users = []
    for item in items:
        item['events_hosted'] = item.get('events_hosted', [])
        item['events_attended'] = item.get('events_attended', [])
        # Filtering
        if company and item.get('company') != company:
            continue
        if job_title and item.get('job_title') != job_title:
            continue
        if city and item.get('city') != city:
            continue
        if state and item.get('state') != state:
            continue
        if events_hosted_min is not None and len(item['events_hosted']) < events_hosted_min:
            continue
        if events_hosted_max is not None and len(item['events_hosted']) > events_hosted_max:
            continue
        if events_attended_min is not None and len(item['events_attended']) < events_attended_min:
            continue
        if events_attended_max is not None and len(item['events_attended']) > events_attended_max:
            continue
        users.append(item)
    # Sorting
    if sort_by:
        users.sort(key=lambda x: x.get(sort_by, ''))
    # Pagination
    users = users[skip:skip+limit]
    return [UserOut(**u) for u in users]

def send_emails_to_users(db, filter: UserFilter):
    """
    Find users matching the filter and send real emails to them, logging the result.
    """
    from app.email_utils import send_email
    results = []
    email_log_table = db.Table('email_logs')
    import time
    users = filter_users(
        db,
        filter.company,
        filter.job_title,
        filter.city,
        filter.state,
        filter.events_hosted_min,
        filter.events_hosted_max,
        filter.events_attended_min,
        filter.events_attended_max,
        filter.skip,
        filter.limit,
        filter.sort_by
    )
    for user in users:
        status = "sent"
        if not send_email(user.email, "Notification from Event CRM", "You have matched a filter query in the Event Management CRM system."):
            status = "failed"
            logger.error(f"Failed to send email to {user.email}")
        else:
            logger.info(f"Email sent to {user.email}")
        log_item = {
            "id": str(uuid.uuid4()),
            "user_id": user.id,
            "email": user.email,
            "status": status,
            "timestamp": int(time.time())
        }
        email_log_table.put_item(Item=log_item)
        results.append({
            "user_id": user.id,
            "email": user.email,
            "status": status
        })
    return {"results": results, "count": len(results)}
