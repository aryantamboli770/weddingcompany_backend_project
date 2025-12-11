# Organization Management Service

**Backend Intern Assignment — Multi-tenant Organization Management Service**

---

## Project Overview

This repository contains a FastAPI backend service that implements a **multi-tenant style** organization management system. The service maintains a **Master Database** (MongoDB) for global metadata and dynamically creates per-organization collections when a new organization is registered.

**Objective:** Create and manage organizations, create an admin user for each org, support admin login (JWT), and provide REST APIs for CRUD operations on organizations.

---

## Features

* Create organization (dynamic MongoDB collection creation)
* Get organization details
* Update organization (with dynamic handling of collection rename / migration)
* Delete organization (with collection cleanup)
* Admin login using JWT authentication
* Passwords stored securely (bcrypt hashing)
* Clean modular code structure (models / services / repositories / routers)

---

## Tech Stack

* Python 3.9+
* FastAPI
* Uvicorn (ASGI server)
* MongoDB (Atlas or local)
* PyMongo
* python-jose (JWT)
* passlib[bcrypt] (password hashing)
* python-dotenv (environment variables)

---

## Architecture (High-level)

**Simple ASCII diagram (quick view):**

```
+----------------------+        +-----------------------+        +----------------+
| Client (Postman / UI)| <----> | FastAPI Backend (app) | <----> | MongoDB Master |
+----------------------+        +-----------------------+        +----------------+
                                       |   ^
                                       |   |
                          dynamic org collections (org_<name>) created in same DB
```

**PlantUML-style (if you want to render later):**

```
@startuml
actor Client
package "FastAPI App" {
  [API Router]
  [Services]
  [Repositories]
}
database "MongoDB (Master)" as DB
Client --> [API Router]
[API Router] --> [Services]
[Services] --> [Repositories]
[Repositories] --> DB : store org metadata
DB --> [API Router] : returns org metadata
@enduml
```

---

## Repository Structure

```
org-management-service/
├─ app/
│  ├─ main.py              # FastAPI app and startup/shutdown
│  ├─ config.py            # App configuration (env loader)
│  ├─ models/              # Pydantic / domain models
│  ├─ repositories/        # DB interaction layer (MongoDB operations)
│  ├─ services/            # Business logic (create org, auth)
│  └─ routers/             # FastAPI route definitions (endpoints)
├─ requirements.txt
├─ .env.example
├─ Dockerfile
├─ docker-compose.yml
└─ README.md
```

---

## Environment Variables

Copy `.env.example` to `.env` and set the values before running.

```
MONGODB_URL=your-mongodb-connection-string
MONGODB_DB_NAME=org_master_db
SECRET_KEY=some-long-random-secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
APP_NAME=Organization Management Service
DEBUG=True
```

> **Important:** Do not commit `.env` to git. Use environment variables or secrets in production.

---

## Setup & Run (Windows)

1. Open PowerShell and change to project directory:

```powershell
cd C:\path\to\org-management-service
```

2. Create and activate a virtual environment (Windows PowerShell):

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, run as administrator:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
```

3. Install requirements:

```powershell
pip install -r requirements.txt
```

4. Create `.env` (copy .env.example) and update MongoDB URL.

5. Run the app (development):

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

6. Open API docs in browser: `http://localhost:8000/docs`

---

## Docker (optional)

A `Dockerfile` and `docker-compose.yml` are included for containerized runs. Edit `.env` or docker-compose secrets before using.

---

## API Endpoints (Summary)

> Base URL: `http://localhost:8000`

### 1. Create Organization

* **Endpoint:** `POST /org/create`
* **Body (JSON):**

```json
{
  "organization_name": "acme",
  "email": "admin@acme.com",
  "password": "StrongPass123"
}
```

* **Behavior:** Creates `org_acme` collection, stores metadata in master DB, creates admin user (hashed password).
* **Response:** Organization metadata and success message.

**cURL example:**

```bash
curl -X POST "http://localhost:8000/org/create" \
  -H "Content-Type: application/json" \
  -d '{"organization_name":"acme","email":"admin@acme.com","password":"StrongPass123"}'
```

---

### 2. Get Organization by Name

* **Endpoint:** `GET /org/get?organization_name=acme`
* **Response:** Organization metadata from master DB or 404 if not found.

---

### 3. Update Organization

* **Endpoint:** `PUT /org/update`
* **Body (JSON):**

```json
{
  "organization_name": "acme",
  "email": "admin@acme.com",
  "password": "NewPass@123"
}
```

* **Behavior:** Validates uniqueness, optionally creates or migrates collection and updates admin credentials.

---

### 4. Delete Organization

* **Endpoint:** `DELETE /org/delete?organization_name=acme`
* **Behavior:** Requires authenticated admin (JWT). Deletes org metadata and drops `org_acme` collection.

---

### 5. Admin Login

* **Endpoint:** `POST /admin/login`
* **Body (JSON):**

```json
{
  "email":"admin@acme.com",
  "password":"StrongPass123"
}
```

* **Behavior:** Validates credentials; returns JWT on success. JWT contains admin ID and organization identifier.

**cURL example:**

```bash
curl -X POST "http://localhost:8000/admin/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@acme.com","password":"StrongPass123"}'
```

---

## Authentication (JWT)

* Use the `Authorization: Bearer <token>` header for protected endpoints.
* Tokens include admin identification and the associated organization ID.

---

## Design Choices & Notes (Brief)

* **Master DB design:** A single master database keeps organization metadata and admin references. This simplifies discovery and management.
* **Dynamic collections:** Using `org_<name>` collections isolates organization data while keeping a single logical database. This is simple and works well for modest scale.
* **Security:** Passwords are hashed with bcrypt. JWT is signed with a strong secret. Never log plaintext secrets.
* **Scalability considerations:** For many tenants or strict isolation, consider separate databases/tenants perorg, or sharded clusters. Also consider a connection-pool manager for many DB connections.

**Trade-offs:**

* Single DB with many collections: easy to manage but might hit collection limits or performance bottlenecks at massive scale.
* Separate DB per tenant: better isolation and easier backup per tenant, but more complex connection management and higher resource usage.

---

## Testing

* Use the interactive Swagger UI at `/docs` to test endpoints.
* Recommended tests: create org → login as admin → get org → update org → delete org.

---

## Troubleshooting Tips

* If you see SSL / OpenSSL errors when connecting to MongoDB, try updating `pyOpenSSL` and `cryptography` to compatible versions (e.g., `pyOpenSSL==23.2.0`, `cryptography==41.0.0`).
* Ensure your `.env` MONGODB_URL is correct and network access to Atlas (if used) is allowed.
* If `venv` activation fails on PowerShell, run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` as admin or activate using the `.\venv\Scripts\Activate.ps1` script.

---

## How to submit (for the assignment)

1. Push your code to GitHub and share the repository link.
2. Ensure the repository contains:

   * Clean modular code (class-based where applicable)
   * `README.md` with clear run instructions
   * `architecture.md` or an architecture diagram
   * A working `requirements.txt` and `.env.example`

---

## Contact / Author

* **Author:** Aryan Tamboli
* **Project:** Backend Intern Assignment — Organization Management Service

---


