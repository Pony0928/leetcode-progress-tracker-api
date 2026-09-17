# LeetCode Progress Tracker

A backend-first web application for recording coding practice, tracking independent problem-solving progress, and scheduling reviews.

**Status:** In development. Problem CRUD, PostgreSQL integration, registration, and login/token issuance are implemented in the current source. `GET /me` now validates bearer tokens and retrieves the current user. Database configuration is environment-based. Practice tracking is not yet implemented. Manual verification is recorded below; automated tests and deployment remain pending.

## Why this project

A solved-problem count does not show whether I solved a problem independently, how my performance changes across attempts, or what I should review next. This application will turn practice records into a personal dashboard and a review queue.

The first release will support this workflow:

> Register → log in → record an attempt → view personal progress → review due problems.

## Current implementation

| Area | Current source status |
| --- | --- |
| FastAPI health endpoint | Implemented; reports application status, not database readiness |
| Problem CRUD | Implemented using PostgreSQL and SQLAlchemy |
| Request validation | Implemented for difficulty, URLs, and account email |
| Registration | Password hashing and duplicate-email check implemented |
| Login | Password verification and expiring JWT issuance implemented |
| Token validation and `/me` | Implemented; missing/fake tokens return 401 and a valid token returns the current user in manual checks |
| Environment configuration | `DATABASE_URL` loaded from environment; missing database configuration fails clearly; `.env.example` added |
| Authorization and user data isolation | Not implemented; only `/me` currently requires authentication |
| Attempts, statistics, review scheduling | Not implemented |
| Automated tests, CI, migrations | Not implemented |
| Frontend, containers, public deployment | Not implemented |

Implementation status does not imply independently verified correctness or production readiness.

## Technology choices

| Technology | Purpose | Status |
| --- | --- | --- |
| Python / FastAPI / Pydantic | API implementation and input validation | In use |
| PostgreSQL / SQLAlchemy | Relational storage and database access | In use |
| PyJWT / password hashing | Login tokens and password verification | Partially integrated |
| Alembic | Versioned database schema changes | Planned |
| pytest / HTTPX | Automated API and logic tests | Planned |
| GitHub Actions | Run tests on pushes and pull requests | Planned |
| Docker / Compose | Reproducible backend and database setup | Planned |
| React / TypeScript | Small usable frontend | Planned after backend workflow |
| Cloud hosting | Public demonstration | Planned; provider not selected |

## First-release scope

- Register, log in, and retrieve the current user.
- Browse a problem catalog and record personal attempts.
- Record outcome, independent completion, duration, and mistake notes.
- View statistics by date, topic, and difficulty.
- View and complete scheduled reviews.
- Run meaningful automated tests and provide a reproducible setup.
- Provide a small frontend and a working demonstration.

## Data model — existing and planned

### User

Existing account model: ID, unique email, unique username, hashed password, and creation time.

### Problem

Shared catalog: ID, unique LeetCode number, title, difficulty, topic, and URL. Personal outcomes belong in attempts, not in the catalog. One topic per problem is sufficient for the first release; multiple tags can be added later if needed.

### Attempt (planned)

One row per practice session: ID, user ID, problem ID, attempted time, solved status, independent completion, duration in seconds, and optional mistake notes. A user can have multiple attempts for the same problem.

### ReviewState (planned)

One row per user/problem pair: next review time, last reviewed time, and review stage. A unique constraint on `(user_id, problem_id)` prevents duplicate schedules. Attempt history remains separate from the current review schedule.

### Access rules

- Users can read the shared catalog.
- Public catalog mutation will be disabled for the first release; a maintainer seed/import script will manage catalog entries.
- Every attempt, review, and statistics query must be scoped to the authenticated user.
- Cross-user resource access returns 404 to avoid disclosing private resource existence.
- Catalog deletion must preserve history or reject deletion when referenced; it must not silently erase attempts.

## Development milestones

Testing starts with each milestone rather than waiting until the end. Complete one milestone before expanding scope.

### 1. Complete authentication and make setup reproducible

- [x] Implement a current-user dependency validating token signature, expiration, subject, and account existence.
- [x] Add `GET /me`; manually verify missing token → 401, valid token → 200, fake token → 401.
- [ ] Add explicit manual/automated tests for expired tokens and deleted accounts.
- [x] Read `DATABASE_URL` from environment and fail clearly when it is missing.
- [x] Add `.env.example` containing placeholders only.
- [x] Verify database create/list, login, and `/me` after the configuration change.
- [x] Fail clearly when `SECRET_KEY` is missing (environment loading already exists).
- [x] Handle duplicate problem numbers with 409 responses and transaction rollback. Manually verified duplicate creation → 409, new creation → 201, and listing → 200 without duplicate records.
- [ ] Complete duplicate email and username conflict handling with transaction rollback.
- [ ] Add automated tests for concurrent duplicate problem creation.
- [ ] Define response schemas and input bounds, including a password policy compatible with the selected hashing implementation.
- [ ] Add Alembic migrations; replace startup table creation with migration commands and preserve existing data.
- [ ] Reject conflicting problem-number values on update.
- [ ] Add automated authentication and conflict tests using an isolated test database.

**Acceptance:** A fresh development database can be initialized from documented commands. Registration, login, and `/me` work. Automated tests verify rejected credentials, duplicate accounts, and exclusion of password hashes from responses.

### 2. Record private practice attempts

- [ ] Add the Attempt model, foreign keys, migration, and request/response schemas.
- [ ] Add create, list, detail, update, and delete operations scoped to the current user.
- [ ] Validate nonnegative duration, referenced problem existence, and sensible field bounds.
- [ ] Add bounded pagination and filters by date, difficulty, and topic.

**Acceptance:** Two test accounts have separate histories. User A cannot read, edit, or delete User B’s attempt. Multiple attempts for one problem persist correctly. Invalid requests do not leave partial writes.

### 3. Add useful statistics and review scheduling

- [ ] Return attempts, distinct practiced problems, solved attempts, and independently solved attempts for a selected date range.
- [ ] Define independent completion rate as independently solved attempts divided by all attempts; return null when there are no attempts.
- [ ] Add topic/difficulty breakdowns and document time-zone handling.
- [ ] Use a transparent initial review rule: first attempt schedules review in 1 day; successful independent reviews advance through 3, 7, 14, then 30 days; unsuccessful or assisted reviews reset to 1 day. Keep later successful reviews at 30 days.
- [ ] Update review state and the review attempt in one transaction. Ordinary practice attempts must not advance the review stage accidentally.
- [ ] Return an authenticated user’s due reviews, ordered by due time.

**Acceptance:** A deterministic fixture produces expected statistics and review dates. Tests cover empty history, date boundaries, schedule resets, and user isolation. Rules are explained as a simple product heuristic, not a scientifically validated learning model.

### 4. Add a small frontend

- [ ] Build login/register, attempt entry, history, summary, and review-queue pages with React and TypeScript.
- [ ] Handle loading, empty, validation, and expired-session states.
- [ ] Decide and document token storage, CORS, and session-expiration behavior before implementation.

**Acceptance:** A user can complete the full core workflow through the UI. Screenshots reflect working functionality.

### 5. Ship a reproducible demonstration

- [ ] Add Docker/Compose for backend and PostgreSQL, with documented migration and seed commands.
- [ ] Configure CI to run tests against an isolated test database; never use the personal development database for tests.
- [ ] Deploy the API, database, and frontend using environment-based configuration and HTTPS.
- [ ] Add safe request/error logging without passwords, bearer tokens, or sensitive notes.
- [ ] Document demo access, hosting limitations, architecture, and troubleshooting.

**Acceptance:** Another person can run the documented setup. CI passes. The public demo supports the core workflow and prevents cross-user access. Publish only measured results and actually implemented features.

## API status and target design

### Existing endpoints

| Method | Path | Current behavior |
| --- | --- | --- |
| GET | `/health` | Application status |
| POST | `/register` | Create an account |
| POST | `/login` | Verify credentials and issue a token |
| GET | `/me` | Validate bearer token and return current user |
| POST / GET | `/problems` | Create/list catalog entries; currently unprotected |
| GET / PUT / DELETE | `/problems/{number}` | Read/update/delete by LeetCode number; currently unprotected |

Existing login accepts a JSON email/password body. Do not assume it supports an OAuth2 form-based token endpoint.

### Planned endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| POST / GET | `/attempts` | Record/list private attempts |
| GET / PATCH / DELETE | `/attempts/{id}` | Manage an owned attempt |
| GET | `/stats/summary` | Personal summary for a date range |
| GET | `/stats/topics` | Personal topic breakdown |
| GET | `/reviews/due` | Personal review queue |
| POST | `/reviews/{problem_id}/complete` | Record a review attempt and update its schedule |

The planned public API will retain catalog reads; catalog writes will move to maintainer tooling.

## Running the current backend

Current setup is manual and does not yet include Docker or migrations.

Prerequisites: Python, a running PostgreSQL server, and a database/account matching `DATABASE_URL` in your environment. Keep real credentials in the untracked `.env`, not in committed code.

```bash
git clone https://github.com/Pony0928/leetcode-progress-tracker-api.git
cd leetcode-progress-tracker-api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Copy `.env.example` to an untracked `.env` in the repository root and replace the placeholders. Create the database named by `DATABASE_URL` using your PostgreSQL administration tools:

```dotenv
DATABASE_URL=postgresql://your_user:your_password@localhost/leetcode_tracker
SECRET_KEY=<replace-with-a-random-local-secret>
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Start the application:

```bash
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000/docs`. The current application creates missing tables at startup; this does not migrate existing table definitions. `DATABASE_URL` is read from the environment. Existing shell environment variables take precedence over `.env` values.

Manual verification on the existing local environment: registration → 201; login → 200; `/me` with missing/fake tokens → 401 and a valid token → 200; problem creation → 201 and listing → 200 after the environment configuration change. These checks do not establish full CRUD correctness or concurrent conflict handling. No public demo or automated test suite is available yet; a clean installation remains unverified.

## Future exploration

After the core product works, collect actual usage data and identify a specific improvement. Start with understandable rules and descriptive statistics for weak-topic insights.

An optional ML experiment must define a useful prediction target, compare with a simple baseline, and evaluate on future/held-out attempts without data leakage. Reproducing labels directly generated from the input features is not evidence of useful predictive performance. If data is insufficient, retain the rule-based feature and document the limitation.

## Out of scope for the first release

Microservices, Kubernetes, Kafka, automated LeetCode scraping, social rankings, mobile apps, payments, and ML prediction are outside the first release.

## Demonstrating engineering understanding

For each completed milestone, retain a short design note explaining a decision, its alternatives, and how correctness was checked. Be able to trace a request through validation, authentication, database access, and response generation; independently change a small requirement; and debug a related failure.

AI assistance is part of the development workflow. Generated code is reviewed and verified before features are marked complete. Planned capabilities are not presented as implemented skills.
