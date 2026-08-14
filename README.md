# LeetCode Progress Tracker API

A backend application for recording solved LeetCode problems, tracking learning progress, identifying recurring mistakes, and scheduling future reviews.

This project is my **12-week main project** built as part of my preparation for 2027 software engineering internship recruiting.

> Note on scope: [`leetcode-progress-tracker`](#) is where I store my day-to-day LeetCode solutions and practice notes. This repository is a separate, recruiter-facing backend engineering project that follows a real product development workflow (requirements → design → implementation → testing → deployment).

## Tech Stack Status

| Technology | Status |
|---|---|
| Python | ✅ Implemented |
| FastAPI | ✅ Implemented |
| Pydantic | ✅ Implemented |
| Python in-memory list (temporary storage) | ✅ Implemented |
| PostgreSQL | 📋 Planned |
| SQLAlchemy | 📋 Planned |
| Pytest | 📋 Planned |
| Docker | 📋 Planned |
| Cloud deployment | 📋 Planned |

## Current Progress

- [x] `GET /health` endpoint
- [x] `Problem` data model (Pydantic)
- [x] `POST /problems` (in-memory list)
- [x] `GET /problems`
- [x] `GET /problems/{id}`
- [x] `PUT /problems/{id}`
- [x] `DELETE /problems/{id}`
- [ ] Migrate to PostgreSQL + SQLAlchemy
- [ ] User Progress data model and endpoints
- [ ] User authentication (register / login / password hashing)
- [ ] Pytest test suite (10–15+ tests)
- [ ] Dockerize
- [ ] Cloud deployment + demo

## Project Goal

This application answers the following questions:

- Which LeetCode problems have I completed?
- Which topics and difficulty levels have I practiced?
- Did I solve a problem independently?
- What mistakes did I make?
- Which problems should I review next?
- How much progress have I made this week?

## Development Roadmap

### Stage 1: Basic FastAPI Application (current stage)
Uses a Python in-memory list instead of a database.

- [x] Health-check endpoint
- [ ] Create / view all / view one / update / delete problem records
- [ ] Request data validation
- [ ] Appropriate HTTP status codes
- [ ] Clear error response when a problem does not exist

### Stage 2: PostgreSQL Database
- Define database models with SQLAlchemy
- Create and manage tables
- Persist data, replacing the in-memory list
- Query, update, and delete database records

### Stage 3: User Progress Tracking
- Completion status and completion date
- Whether the problem was solved independently
- Notes about mistakes
- Next review date
- Filter by topic, difficulty, or status
- View problems due for review

### Stage 4: User Accounts
- Register, hash passwords, log in
- Authenticate requests
- Ensure users can access only their own progress records

### Stage 5: Testing and Reliability
- Unit and API tests with Pytest (at least 10–15 automated tests)
- Consistent error response format

### Stage 6: Documentation and Deployment
- Dockerfile and environment-variable configuration
- Cloud deployment with a public link
- Short project demonstration

## API Endpoints

### Health Check (implemented)
```
GET /health
```
Response:
```json
{ "status": "ok" }
```
### Create a Problem (implemented)

POST /problems

Creates and stores a validated problem in the temporary in-memory list.

### View All Problems (implemented)

GET /problems

Returns all problems currently stored in memory.

## Running Locally

```bash
git clone https://github.com/Pony0928/leetcode-progress-tracker-api.git
cd leetcode-progress-tracker-api
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload
```

Visit `http://127.0.0.1:8000/docs` to view the interactive API documentation.

## Out of Scope for This Version

- React or mobile frontend
- Social features, leaderboards
- AI-generated solutions
- Automatic LeetCode account synchronization
- Recommendation algorithms
- Microservices / Kubernetes
- Payment functionality

These features are intentionally excluded so the core backend can be completed, tested, and deployed first.