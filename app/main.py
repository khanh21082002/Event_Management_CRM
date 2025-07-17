from fastapi import HTTPException
# Tạo event
from fastapi import FastAPI, Depends, Query
from . import crud, schemas, dependencies
from typing import List, Optional

app = FastAPI()




###########################
# USER ENDPOINTS
###########################
@app.get("/users/all", response_model=List[schemas.UserOut] , tags=["User"])
def get_all_users(db=Depends(dependencies.get_db)):
    return crud.get_all_users(db)

@app.post("/users", response_model=schemas.UserOut , tags=["User"])
def create_user(user: schemas.UserCreate, db=Depends(dependencies.get_db)):
    return crud.create_user(db, user)

@app.get("/users/{user_id}", response_model=schemas.UserOut , tags=["User"])
def get_user(user_id: str, db=Depends(dependencies.get_db)):
    return crud.get_user(db, user_id)

@app.put("/users/{user_id}", response_model=schemas.UserOut , tags=["User"])
def update_user(user_id: str, user: schemas.UserCreate, db=Depends(dependencies.get_db)):
    return crud.update_user(db, user_id, user)

@app.delete("/users/{user_id}" , tags=["User"])
def delete_user(user_id: str, db=Depends(dependencies.get_db)):
    return crud.delete_user(db, user_id)

@app.get("/users", response_model=List[schemas.UserOut] , tags=["User"])
def filter_users(
    company: Optional[str] = None,
    job_title: Optional[str] = None,
    city: Optional[str] = None,
    state: Optional[str] = None,
    events_hosted_min: Optional[int] = None,
    events_hosted_max: Optional[int] = None,
    events_attended_min: Optional[int] = None,
    events_attended_max: Optional[int] = None,
    skip: int = 0,
    limit: int = 10,
    sort_by: Optional[str] = None,
    db=Depends(dependencies.get_db)
):
    return crud.filter_users(
        db,
        company,
        job_title,
        city,
        state,
        events_hosted_min,
        events_hosted_max,
        events_attended_min,
        events_attended_max,
        skip,
        limit,
        sort_by
    )
# User register for event
@app.post("/users/{user_id}/events/{event_id}/register", tags=["User"])
def register_user_for_event(user_id: str, event_id: str, db=Depends(dependencies.get_db)):
    return crud.register_event(db, event_id, user_id)

###########################
# EVENT ENDPOINTS
###########################
# Tạo event
@app.post("/events", response_model=schemas.EventOut , tags=["Event"])
def create_event(event: schemas.EventCreate, db=Depends(dependencies.get_db)):
    event_dict = crud.create_event(db, event)
    return event_dict

# Lấy danh sách event
@app.get("/events", response_model=List[schemas.EventOut] , tags=["Event"])
def list_events(db=Depends(dependencies.get_db)):
    return crud.list_events(db)

@app.get("/events/all", response_model=List[schemas.EventOut] , tags=["Event"])
def get_all_events(db=Depends(dependencies.get_db)):
    return crud.list_events(db)

@app.get("/events/{event_id}", response_model=schemas.EventOut , tags=["Event"])
def get_event(event_id: str, db=Depends(dependencies.get_db)):
    return crud.get_event(db, event_id)

@app.put("/events/{event_id}", response_model=schemas.EventOut , tags=["Event"])
def update_event(event_id: str, event: schemas.EventCreate, db=Depends(dependencies.get_db)):
    return crud.update_event(db, event_id, event)

@app.delete("/events/{event_id}" , tags=["Event"])
def delete_event(event_id: str, db=Depends(dependencies.get_db)):
    return crud.delete_event(db, event_id)



###########################
# MAIL ENDPOINTS
###########################
@app.get("/email-logs" , tags=["Mail"])
def get_email_logs(db=Depends(dependencies.get_db)):
    return crud.get_email_logs(db)


@app.post("/send-emails" , tags=["Mail"])
def send_emails(
    filter: schemas.UserFilter,
    db=Depends(dependencies.get_db)
):
    return crud.send_emails_to_users(db, filter)


# Analytics: user engagement
@app.get("/analytics/user-engagement" , tags=["Analytics"])
def user_engagement_analytics(db=Depends(dependencies.get_db)):
    return crud.user_engagement_analytics(db)
