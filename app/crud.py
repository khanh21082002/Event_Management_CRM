

from .models import User, Event
from .schemas import UserFilter, UserCreate, UserOut
from typing import List, Optional
import uuid

def get_all_users(db):
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
    import uuid
    table = db.Table('events')
    event_id = str(uuid.uuid4())
    event_dict = event.dict()
    event_dict['id'] = event_id
    event_dict['attendees'] = []
    table.put_item(Item=event_dict)
    # Cập nhật events_hosted cho owner
    user_table = db.Table('users')
    owner_id = event.owner
    user_table.update_item(
        Key={'id': owner_id},
        UpdateExpression='SET events_hosted = list_append(if_not_exists(events_hosted, :empty), :e)',
        ExpressionAttributeValues={':e': [event_id], ':empty': []}
    )
    # Cập nhật events_hosted cho các host khác (nếu có)
    for host_id in event.hosts:
        user_table.update_item(
            Key={'id': host_id},
            UpdateExpression='SET events_hosted = list_append(if_not_exists(events_hosted, :empty), :e)',
            ExpressionAttributeValues={':e': [event_id], ':empty': []}
        )
    return event_dict

def list_events(db):
    table = db.Table('events')
    response = table.scan()
    items = response.get('Items', [])
    return items

def register_event(db, event_id, user_id):
    event_table = db.Table('events')
    user_table = db.Table('users')
    # Thêm user vào attendees của event
    event_table.update_item(
        Key={'id': event_id},
        UpdateExpression='SET attendees = list_append(if_not_exists(attendees, :empty), :u)',
        ExpressionAttributeValues={':u': [user_id], ':empty': []}
    )
    # Thêm event vào events_attended của user
    user_table.update_item(
        Key={'id': user_id},
        UpdateExpression='SET events_attended = list_append(if_not_exists(events_attended, :empty), :e)',
        ExpressionAttributeValues={':e': [event_id], ':empty': []}
    )
    return {'event_id': event_id, 'user_id': user_id, 'status': 'registered'}

def user_engagement_analytics(db):
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
    user_id = str(uuid.uuid4())
    user_dict = user.dict()
    user_dict["id"] = user_id
    user_dict["events_hosted"] = []
    user_dict["events_attended"] = []
    table = db.Table('users')
    table.put_item(Item=user_dict)
    return UserOut(**user_dict)

def filter_users(db, company, job_title, city, state, events_hosted_min, events_hosted_max, events_attended_min, events_attended_max, skip, limit, sort_by):
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
    # Use filter_users to get the list of users matching the filter
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
    # Mock sending emails
    results = []
    for user in users:
        # Here you would call your email sending utility
        results.append({
            "user_id": user.id,
            "email": user.email,
            "status": "sent (mock)"
        })
    return {"results": results, "count": len(results)}
