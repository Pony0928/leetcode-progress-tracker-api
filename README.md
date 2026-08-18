# LeetCode Progress Tracker

A full-stack application for recording solved LeetCode problems, tracking learning progress, identifying recurring mistakes, scheduling spaced-repetition reviews, and surfacing weak topics through a lightweight ML model.

This project is my **main project** built as part of my preparation for 2027 software engineering internship / new grad recruiting.

> Note on scope: [`leetcode-progress-tracker`](#) is where I store my day-to-day LeetCode solutions and practice notes. This repository is a separate, recruiter-facing full-stack engineering project that follows a real product development workflow (requirements → design → implementation → testing → deployment).

## Tech Stack Status

| Technology | Status |
|---|---|
| Python | ✅ Implemented |
| FastAPI | ✅ Implemented |
| Pydantic | ✅ Implemented |
| PostgreSQL | ✅ Implemented |
| SQLAlchemy | ✅ Implemented |
| JWT Authentication | 📋 Planned |
| React + TypeScript | 📋 Planned |
| scikit-learn | 📋 Planned |
| Pytest | 📋 Planned |
| Docker | 📋 Planned |
| Cloud deployment | 📋 Planned |

## Current Progress

- [x] `GET /health` endpoint
- [x] `Problem` data model (Pydantic)
- [x] `POST /problems`
- [x] `GET /problems`
- [x] `GET /problems/{id}`
- [x] `PUT /problems/{id}`
- [x] `DELETE /problems/{id}`
- [x] Migrate to PostgreSQL + SQLAlchemy
- [ ] User model and JWT authentication
- [ ] Attempt / progress tracking model with spaced-repetition fields
- [ ] React frontend (auth, problem CRUD UI, progress dashboard)
- [ ] Lightweight ML model for weak-topic prediction
- [ ] Pytest test suite (10–15+ tests)
- [ ] Dockerize (backend + frontend)
- [ ] Cloud deployment + demo

## Project Goal

This application answers the following questions:

- Which LeetCode problems have I completed?
- Which topics and difficulty levels have I practiced?
- Did I solve a problem independently, and how long did it take?
- Which problems should I review next?
- How much progress have I made this week?
- Based on my own practice history, which topics am I actually weak in — not by guessing, but by a model trained on my own attempt data?

## Development Roadmap

### Stage 1: Basic FastAPI Application
Uses a Python in-memory list instead of a database.

- [x] Health-check endpoint
- [x] Create / view all / view one / update / delete problem records
- [x] Request data validation
- [x] Appropriate HTTP status codes
- [x] Clear error response when a problem does not exist

### Stage 2: PostgreSQL Database
- [x] Define database models with SQLAlchemy
- [x] Create and manage tables
- [x] Persist data, replacing the in-memory list
- [x] Query, update, and delete database records

### Stage 3: User Accounts & Authentication
- Register, hash passwords, log in
- JWT-based request authentication
- Ensure users can access only their own data
- Foundation for all per-user data in later stages

### Stage 4: Attempt & Progress Tracking
- Attempt records linked to a user and a problem: solved status, time spent, solved independently or not, mistake notes
- Spaced-repetition scheduling: next review date, review count
- Filter by topic, difficulty, or review status
- View problems due for review

### Stage 5: React Frontend
- Login / register pages
- Problem CRUD interface consuming the existing API
- Progress dashboard: charts by topic and difficulty (Recharts)
- Review queue view

### Stage 6: Lightweight ML — Weak Topic Insight
- A small scikit-learn model (logistic regression / decision tree) trained on the user's own attempt data (topic, time spent, first-try success, review count)
- `/insights` endpoint returning topics the model flags as needing more review
- Displayed as a module on the frontend dashboard
- Scope note: this is a small applied ML feature built on top of real usage data, not a research-grade ML system — trained and evaluated on a single user's practice history

### Stage 7: Testing, Docker, and Deployment
- Unit and API tests with Pytest (at least 10–15 automated tests), including the `/insights` endpoint
- Dockerfile for backend and frontend
- docker-compose for local multi-service setup
- Cloud deployment with a public link (backend + frontend)

## API Endpoints

### Health Check (implemented)

GET /health
Response:
```json
{ "status": "ok" }
```
### Create a Problem (implemented)

POST /problems

Validates the request body and inserts a new problem record into the PostgreSQL database. Returns the created problem, including its database-generated `id`, with status code `201`.


### View All Problems (implemented)

GET /problems

Returns all problem records currently stored in the database.

### View a Single Problem (implemented)

GET /problems/{number}

Returns the problem matching the given `number`. Returns a `404` error with a clear message if no matching problem exists.

### Update a Problem (implemented)

PUT /problems/{number}

Replaces the existing problem record matching `number` with the provided data. Returns the updated problem with status code `200`, or a `404` error if the problem does not exist.

### Delete a Problem (implemented)

DELETE /problems/{number}

Deletes the problem record matching `number`. Returns status code `204` with no response body, or a `404` error if the problem does not exist.

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

- Mobile app (React Native / native iOS / Android)
- Social features, leaderboards, multi-user comparison
- Automatic LeetCode account synchronization or scraping
- Recommendation algorithms beyond the single weak-topic ML model described in Stage 6
- Deep learning / neural network models — the ML feature intentionally uses a simple, explainable model appropriate for the size of the dataset (one user's own practice history)
- Microservices / Kubernetes
- Payment functionality

These features are intentionally excluded so the core full-stack application — with a real authentication layer, a working frontend, and one honestly-scoped ML feature — can be completed, tested, and deployed first.