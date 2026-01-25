🚀 SaaS API – Local Development, Testing & CI

A production-style FastAPI SaaS backend using PostgreSQL, JWT authentication, Alembic migrations, automated tests, Docker, and GitHub Actions CI.

🧱 Tech Stack

FastAPI

PostgreSQL

SQLAlchemy 2.x

Alembic

psycopg (v3)

pytest

Docker & Docker Compose

GitHub Actions

📦 Requirements

Python 3.12+

Docker Desktop (Windows/macOS) or Docker Engine (Linux)

Git

🔧 Environment Variables

The application is configured entirely via environment variables.

Minimum required

DATABASE_URL

JWT_SECRET_KEY

JWT_ALGORITHM

ACCESS_TOKEN_EXPIRE_MINUTES

Example .env (local development)
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/saas_db
JWT_SECRET_KEY=dev-secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60


✅ .env.example is committed
❌ .env must NOT be committed

⚠️ Important Notes

This project uses psycopg v3

Database URLs must use:

postgresql+psycopg://


Do not use psycopg2

🏃 Running the App Locally (Development)
1️⃣ Clone the repository
git clone <your-repo-url>
cd project-a-saas-api

2️⃣ Create & activate virtual environment
python -m venv .venv


Windows (PowerShell)

.venv\Scripts\Activate.ps1

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Start PostgreSQL (Docker)
docker compose up -d db


Verify:

docker ps

5️⃣ Run database migrations
$env:DATABASE_URL="postgresql+psycopg://postgres:postgres@localhost:5432/saas_db"
alembic upgrade head


You only need to run this when:

Setting up a fresh database

Adding new migrations

6️⃣ Start the API server
uvicorn app.main:app --reload

📚 API Documentation

Once running:

Swagger UI
http://127.0.0.1:8000/docs

OpenAPI JSON
http://127.0.0.1:8000/openapi.json

🔐 Authentication Endpoints
Register

POST /auth/register

{
  "email": "user@example.com",
  "password": "StrongPassword123"
}


Responses

201 Created

409 Conflict (email already exists)

Login

POST /auth/login
(Form data)

Responses

200 OK

401 Unauthorized

👤 User Endpoints
Get current user

GET /users/me

Header:

Authorization: Bearer <access_token>

Update current user

PATCH /users/me

{
  "email": "new@example.com"
}

🧪 Running Tests
✅ Option A (Recommended): Run tests in Docker

This matches CI exactly and avoids Windows networking issues.

docker compose run --rm tests


This will:

Start the test database

Run Alembic migrations automatically

Execute pytest

Option B: Run tests locally on Windows
1️⃣ Start test DB
docker compose up -d test_db

2️⃣ Set environment variables
$env:DATABASE_URL="postgresql+psycopg://postgres:postgres@localhost:55433/saas_test_db"
$env:JWT_SECRET_KEY="test-secret"
$env:JWT_ALGORITHM="HS256"
$env:ACCESS_TOKEN_EXPIRE_MINUTES="60"
$env:SKIP_DB_INIT="1"

3️⃣ Run tests
pytest -q


✅ Alembic migrations are run automatically by tests/conftest.py

🗂 Database Migrations (Alembic)
Create a migration
alembic revision --autogenerate -m "describe change"

Apply migrations
alembic upgrade head


⚠️ Always commit files inside:

alembic/versions/


Tests and CI depend on these files.

🤖 GitHub Actions CI

This project includes fully automated CI via GitHub Actions.

CI does the following:

Starts PostgreSQL

Runs Alembic migrations

Executes pytest

CI will pass as long as:

alembic/versions/*.py are committed

DATABASE_URL is respected in alembic/env.py

Migrations are valid

The workflow lives in:

.github/workflows/test.yml

🧯 Troubleshooting
❌ relation "users" does not exist

Cause: migrations did not run

Fix:

alembic upgrade head

❌ Can't locate revision identified by ...

Cause: database references a migration that no longer exists

Fix (local test DB):

docker compose down
docker compose up -d test_db

🧑‍💻 Author

Built as part of a Backend Software Engineer (Python) learning & portfolio project, following real-world backend practices:

migrations

testing

CI

Dockerized infrastructure