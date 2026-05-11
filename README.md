# Task Manager REST API

A production-structured REST API for managing personal tasks. Built with Django and Django REST Framework, following real-world backend architecture patterns.

## Tech Stack

| Technology | Version | Role |
|---|---|---|
| Python | 3.12.10 | Runtime |
| Django | 5.2.13 | Web framework |
| Django REST Framework | 3.15.2 | API layer |
| Simple JWT | latest | Authentication |
| django-filter | latest | Filtering |
| drf-spectacular | latest | API documentation |
| SQLite | — | Local development database |
| PostgreSQL | — | Production database |
| Gunicorn | latest | Production WSGI server |
| WhiteNoise | latest | Static file serving |

## Project Structure

```text
taskmanager/
├── apps/
│   ├── tasks/          # Task model, views, serializers, services, tests
│   └── users/          # Custom User model
├── config/
│   ├── settings/
│   │   ├── base.py     # Shared settings
│   │   ├── local.py    # Development settings
│   │   └── production.py  # Production settings
│   ├── urls.py
│   └── wsgi.py
├── .env                # Environment variables (NOT in Git)
├── manage.py
└── requirements.txt
```

## Local Setup

### Prerequisites

- Python 3.12.10
- Git

### 1. Clone the Repository

```cmd
git clone https://github.com/rahulsharmar1/taskmanager-api.git
cd taskmanager-api
```

### 2. Create and Activate Virtual Environment

```cmd
python3.12 -m venv venv
venv\Scripts\Activate
```

### 3. Install Dependencies

```cmd
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the example and fill in your values:

```cmd
copy .env.example .env
```

Edit `.env`:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

Generate a secret key:

```cmd
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Run Migrations

```cmd
python manage.py migrate
```

### 6. Create a Superuser

```cmd
python manage.py createsuperuser
```

### 7. Run the Development Server

```cmd
python manage.py runserver
```

API is available at `http://127.0.0.1:8000/`

## API Documentation

Interactive documentation is available when the server is running:

| Interface | URL |
|---|---|
| Swagger UI | `http://127.0.0.1:8000/api/schema/swagger-ui/` |
| ReDoc | `http://127.0.0.1:8000/api/schema/redoc/` |
| Raw Schema | `http://127.0.0.1:8000/api/schema/` |

## Authentication

This API uses JWT (JSON Web Tokens).

### Obtain Tokens

```bash
POST /api/auth/token/
Content-Type: application/json

{
    "username": "your_username",
    "password": "your_password"
}
```

**Response:**
```json
{
    "access": "eyJ...",
    "refresh": "eyJ..."
}
```

### Use the Access Token

Include the token in every request:
`Authorization: Bearer eyJ...`

### Refresh the Access Token

```bash
POST /api/auth/token/refresh/
Content-Type: application/json

{
    "refresh": "eyJ..."
}
```

## API Endpoints

All endpoints require authentication. Tasks are scoped to the authenticated user.

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/tasks/` | List all tasks (paginated) |
| `POST` | `/api/tasks/` | Create a new task |
| `GET` | `/api/tasks/{id}/` | Retrieve a task |
| `PUT` | `/api/tasks/{id}/` | Full update a task |
| `PATCH` | `/api/tasks/{id}/` | Partial update a task |
| `DELETE` | `/api/tasks/{id}/` | Delete a task |

### Query Parameters

| Parameter | Example | Description |
|---|---|---|
| `status` | `?status=todo` | Filter by status |
| `due_date` | `?due_date=2025-12-31` | Filter by exact due date |
| `ordering` | `?ordering=-created_at` | Sort results |
| `page` | `?page=2` | Page number |
| `page_size` | `?page_size=5` | Results per page (max 100) |

### Task Object

```json
{
    "id": 1,
    "owner": 1,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "status": "todo",
    "due_date": "2025-12-01",
    "created_at": "2025-10-01T09:00:00Z",
    "updated_at": "2025-10-01T09:00:00Z"
}
```

**Status values:** `todo` | `in_progress` | `done`

## Running Tests

```cmd
python manage.py test apps.tasks.tests --verbosity=2
```

## API Access Points

This project supports two primary environments:

### Local Development Environment
When running `python manage.py runserver`, the API is accessible at:
`http://127.0.0.1:8000/`

### Live Production Environment
The live, deployed API endpoint is:
`https://taskmanager-api-php8.onrender.com/`


## Deployment

Live API: `https://taskmanager-api-php8.onrender.com`


## Git Workflow

This project follows a feature-branch workflow with conventional commits.
```text
main ← merge via PR after review
└── feature/<iteration-topic>
```
Commit format: `<type>(<scope>): <message>`