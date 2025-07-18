# Event_Management_CRM

## Description
Event Management CRM system built with FastAPI and DynamoDB. Supports user and event management, event registration, advanced user filtering, mock email sending with logs, and analytics.

## Features
- CRUD for users
- CRUD for events
- Event registration
- Advanced user filtering (by company, job title, city, number of events hosted/attended, etc.)
- Send emails to users (mock, with logging)
- User engagement analytics
- Swagger UI with endpoints grouped by function

## Technology Stack
- Python 3.x
- FastAPI
- DynamoDB (local or AWS)
- Pydantic
- Boto3
- Python-dotenv

## API
![User](https://github.com/khanh21082002/Event_Management_CRM/blob/main/img/api.png)
![Event and Email](https://github.com/khanh21082002/Event_Management_CRM/blob/main/img/api1.png)

## Setup
1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd Event_Management_CRM
   ```
2. Install Python packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Start DynamoDB local (if using local):
   - Download DynamoDB local from AWS
   - Run: `java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb -port 8001`
4. Create DynamoDB tables:
   ```bash
   python -m app.init_dynamodb
   ```
5. Create a `.env` file (if needed):
   ```env
   DYNAMODB_LOCAL_URL=http://localhost:8001
   AWS_DEFAULT_REGION=us-east-1
   ```
6. Start the server:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Usage
- Access Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- Endpoints are grouped by User, Event, Mail, Analytics.

### Example: Filter users (GET)
```
/users?company=ABC&job_title=DEV&events_hosted_min=1
```

### Example: Send emails to users (POST)
```
POST /send-emails
{
  "company": "ABC",
  "events_hosted_min": 1
}
```

## API Testing

You can test the API using:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Postman**: Import the provided `postman_collection.json` file in this repo.
- **cURL**: See examples below.

### Sample cURL Commands

#### Get all users
```sh
curl -X GET "http://localhost:8000/users/all"
```

#### Create a user
```sh
curl -X POST "http://localhost:8000/users" \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "John",
    "lastName": "Doe",
    "email": "john@example.com"
  }'
```

#### Create an event
```sh
curl -X POST "http://localhost:8000/events" \
  -H "Content-Type: application/json" \
  -d '{
    "slug": "unit-test-event",
      "title": "Unit Test Event",
      "startAt": "2025-17-07T10:00:00Z",
      "endAt": "2023-17-07T12:00:00Z",
      "maxCapacity": 100,
      "owner": "unit_test_owner"
```

#### Filter users
```sh
curl -X GET "http://localhost:8000/users?company=ABC&job_title=DEV"
```

#### Send emails to users
```sh
curl -X POST "http://localhost:8000/send-emails" \
  -H "Content-Type: application/json" \
  -d '{
    "company": "ABC",
    "events_hosted_min": 1
  }'
```

#### Analytics
 ```sh
   curl -X GET "http://localhost:8000/analytics/user-engagement"
```

## Project Structure
- `app/main.py`: API definitions
- `app/crud.py`: Business/data logic
- `app/schemas.py`: Pydantic schemas
- `app/database.py`: DynamoDB connection
- `app/init_dynamodb.py`: Table creation script
- `app/dependencies.py`: FastAPI dependencies (Database sessions) 

## Notes
- Email sending is mocked, not real.
- DynamoDB can run locally or on AWS.
- If you encounter filter issues, check your input data and ensure correct query/body format.