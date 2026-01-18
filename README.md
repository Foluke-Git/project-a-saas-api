🚀 Running the Project Locally
1️⃣ Clone the repository
git clone <your-repo-url>
cd project-a-saas-api

2️⃣ Create and activate virtual environment
python -m venv .venv


Windows
.venv\Scripts\Activate.ps1

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Set up environment variables
copy .env.example .env


Edit .env if needed (defaults work for local development).

5️⃣ Start PostgreSQL with Docker
docker compose up -d


Confirm DB is running:
docker ps

6️⃣ Start the FastAPI server
uvicorn app.main:app --reload

📚 API Documentation

Once running, open:

Swagger UI:
http://127.0.0.1:8000/docs

OpenAPI JSON:
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

{
  "email": "user@example.com",
  "password": "StrongPassword123"
}


Responses

200 OK

401 Unauthorized (invalid credentials)

🧪 Database Verification (Optional)

Connect to PostgreSQL:

docker exec -it saas_db psql -U postgres -d saas_db

SELECT id, email, hashed_password FROM users;


Passwords are stored as Argon2 hashes.

🧭 Next Planned Features

JWT authentication (access tokens)

Protected routes (/users/me)

Role-based access control

Alembic migrations

Test suite (pytest)

CI-ready configuration

🧑‍💻 Author
Built as part of a Backend Software Engineer (Python) learning and portfolio project, following real-world backend practices.