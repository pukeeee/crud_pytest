# User CRUD Service

This repository contains a modern backend service for user management, built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**.
It demonstrates clean architecture, robust validation, JWT authentication, and a full suite of unit and integration tests.

[Українська версія](README_ukr.md)
---

## 🗂️ Project Structure
```
crudPytest/
│
├── src/
│ ├── auth/ # JWT and password hashing logic
│ ├── component/ # Abstract repository interface
│ ├── controller/ # FastAPI routes (API layer)
│ ├── db/ # Database models, repository, and session setup
│ ├── dto/ # Pydantic schemas and validation
│ ├── service/ # Business logic and error classes
│
├── tests/
│ ├── integration/ # Integration tests (API + DB)
│ ├── unit/ # Unit tests (service, validation, repository)
│
├── docker-compose.yml
├── dockerfile
├── requirements.txt
├── pytest.ini
└── README.md
```
---

## 🧩 Main Logic

- **API Layer** (`src/controller/user_controller.py`):
  Handles HTTP requests, dependency injection, and error mapping.
- **Service Layer** (`src/service/user_service.py`):
  Contains business logic, validation, and orchestrates repository calls.
- **Repository Layer** (`src/db/db_repository.py`):
  Directly interacts with the database using SQLAlchemy ORM.
- **DTOs** (`src/dto/`):
  Pydantic models for request/response validation and serialization.
- **Authentication** (`src/auth/`):
  JWT token generation/validation and password hashing.

---

## 🧪 Testing

- **Unit Tests**:
  - Test business logic, validation, and repository in isolation.
  - Located in `tests/unit/`.
- **Integration Tests**:
  - Test the full API stack with a real database (PostgreSQL).
  - Located in `tests/integration/`.
- **How to run tests**:
  - All tests can be run with Docker Compose (see below).
  - You can also run tests locally if you have PostgreSQL running.

---

## 🔄 CI/CD

This project uses [GitHub Actions](.github/workflows/ci-cd.yml) for its Continuous Integration pipeline.

The workflow automatically triggers on every `push` or `pull_request` to the `master` branch and performs the following steps:
- **Sets up a Python environment.**
- **Installs all dependencies.**
- **Runs the complete test suite** (unit and integration tests) against a fresh PostgreSQL database.
- **Sends Telegram notifications** on test failure or successful pull request merges.
- **Automatically merges pull requests** tagged with `automerge` if all tests pass.

---

## 🐳 Running with Docker Compose

**Requirements:**
- [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/)

**Start all services and run tests:**
```bash
docker-compose up --build --abort-on-container-exit
```
- This command builds the Docker image, starts a PostgreSQL database, and runs the complete test suite in an isolated environment.
- After the tests finish, all containers will be stopped automatically.

**Running the database for local development:**
If you want to run only the database and connect to it from your local machine (e.g., for manual testing or running `pytest` locally), use:
```bash
docker-compose up postgres
```
The PostgreSQL database will be available on `localhost:5445`.

---

## ⚙️ Environment Variables

All configuration is managed via an `.env` file in the project root.

**Database:**
- `POSTGRES_USER`: Database username.
- `POSTGRES_PASSWORD`: Database password.
- `POSTGRES_DB`: Database name.
- `POSTGRES_HOST`: Hostname for the database service (used within Docker).
- `POSTGRES_PORT`: Port for the database service (used within Docker).

**Authentication:**
- `SECRET_KEY`: Secret key for signing JWT tokens.
- `ALGORITHM`: Algorithm used for JWT signing (e.g., `HS256`).
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Lifetime of the access token in minutes.
