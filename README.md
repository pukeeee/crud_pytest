# User CRUD Service

This repository contains a modern backend service for user management, built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**.  
It demonstrates clean architecture, robust validation, JWT authentication, and a full suite of unit and integration tests.  
The project is designed both as a practical backend solution and as a portfolio example for employers and recruiters.

---

## 🗂️ Project Structure

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

## 🐳 Running with Docker Compose

**Requirements:**  
- [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/)

**Start all services and run tests:**
```bash
docker-compose up --build --abort-on-container-exit
```
- This will start a PostgreSQL database and run all tests in an isolated environment.
- After tests finish, all containers will be stopped automatically.

**You can also run only the database:**
```bash
docker-compose up postgres
```
And then run tests locally (e.g., with `pytest`), connecting to the same database.

---

## ⚙️ Environment Variables

All configuration is managed via environment variables (see `.env` or `.env.test`).  
Key variables:
- `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `POSTGRES_HOST`, `POSTGRES_PORT`

---

## 🚧 Project Status & Future Plans

- The project is actively maintained and will be further developed.
- More tests (unit and integration) will be added to cover additional scenarios.
- Business logic and features will be extended and improved over time.
- Feedback and contributions are welcome!