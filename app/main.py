from fastapi import HTTPException
# Tạo event
from fastapi import FastAPI, Depends, Query
from . import crud, schemas, dependencies
from typing import List, Optional

app = FastAPI()

# Tạo event
@app.post("/events", response_model=schemas.EventOut)
def create_event(event: schemas.EventCreate, db=Depends(dependencies.get_db)):
    event_dict = crud.create_event(db, event)
    return event_dict

# Lấy danh sách event
@app.get("/events", response_model=List[schemas.EventOut])
def list_events(db=Depends(dependencies.get_db)):
    return crud.list_events(db)

# Đăng ký tham dự event
@app.post("/events/{event_id}/register")
def register_event(event_id: str, user_id: str, db=Depends(dependencies.get_db)):
    return crud.register_event(db, event_id, user_id)

# Analytics: user engagement
@app.get("/analytics/user-engagement")
def user_engagement_analytics(db=Depends(dependencies.get_db)):
    return crud.user_engagement_analytics(db)

# Lấy tất cả người dùng
@app.get("/users/all", response_model=List[schemas.UserOut])
def get_all_users(db=Depends(dependencies.get_db)):
    return crud.get_all_users(db)

@app.post("/users", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db=Depends(dependencies.get_db)):
    return crud.create_user(db, user)

@app.get("/users", response_model=List[schemas.UserOut])
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

@app.post("/send-emails")
def send_emails(
    filter: schemas.UserFilter,
    db=Depends(dependencies.get_db)
):
    return crud.send_emails_to_users(db, filter)
