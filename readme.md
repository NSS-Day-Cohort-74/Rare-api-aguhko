# Rare API Documentation

The Rare API is a RESTful interface built on Python's HTTP server framework, providing endpoints for managing users, posts, categories, and tags. The API uses JSON for request/response bodies and follows standard HTTP status codes for communication.

## Getting Started

- Base URL: `http://localhost:8088`
- Request Format: JSON
- Response Format: JSON
- Port: `8088`

## Setup Instructions

1. Create a virtual environment and install dependencies:

   ```bash
   pipenv shell
   pipenv install
   ```

2. Create the database:

   ```bash
   touch db.sqlite3
   ```

3. Initialize the database tables:

   ```bash
   python -m sqlite3 db.sqlite3 < loaddata.sql
   ```

4. Start the server:

   ```bash
   python server.py
   ```

## Authentication Endpoints

### Login

```http
POST /login HTTP/1.1
Content-Type: application/json

{
    "username": "string",
    "password": "string"
}

HTTP/1.1 200 OK
Content-Type: application/json

{
    "valid": true,
    "token": "string"
}

HTTP/1.1 406 Not Acceptable
Content-Type: application/json

{
    "valid": false,
}
```

### Register

```http
POST /register HTTP/1.1
Content-Type: application/json

{
    "first_name": "string",
    "last_name": "string",
    "username": "string",
    "password": "string",
    "bio": "string",
    "email": "string"
}

HTTP/1.1 201 Created
Content-Type: application/json

{
    "token": int,
    "valid": True
}

```

## Post Endpoints

### List Posts

```http
GET /posts HTTP/1.1

HTTP/1.1 200 OK
Content-Type: application/json

[
    {
        "id": int,
        "user_id": integer,
        "category_id": int,
        "title": str,
        "publication_date": str,
        "image_url": str,
        "content": string,
        "approved": bool,
        "created_at": string
    },
    {
        "id": int,
        "user_id": integer,
        "category_id": int,
        "title": str,
        "publication_date": str,
        "image_url": str,
        "content": string,
        "approved": bool,
        "created_at": string
    },

]
```

### List Posts by User

```http
GET /posts?user_id=integer HTTP/1.1

HTTP/1.1 200 OK
Content-Type: application/json

[
    {
        "id": int,
        "user_id": integer,
        "category_id": int,
        "title": str,
        "publication_date": str,
        "image_url": str,
        "content": string,
        "approved": bool,
        "created_at": string
    }
]
```

### Create Post

```http
POST /posts HTTP/1.1
Content-Type: application/json

{

    "user_id": int,
    "category_id": int,
    "title": str,
    "publication_date": str,
    "image_url": str,
    "approved": bool,
    "content": string
}

HTTP/1.1 201 Created
Content-Length: 0

HTTP/1.1 422 Unprocessable Entity
Content-Type: application/json

     "Validation error"
```

## Category Endpoints

### List Categories

```http
GET /categories HTTP/1.1

HTTP/1.1 200 OK
Content-Type: application/json

[
    {
        "id": integer,
        "label": string
    }
]
```

### Create Category

```http
POST /categories HTTP/1.1
Content-Type: application/json

{
    "label": string
}

HTTP/1.1 201 Created
{
    "created": "true"
}

HTTP/1.1 400 Bad Request
Content-Type: application/json

{
    "created": "false"
}
```

## Tag Endpoints

### List Tags

```http
GET /tags HTTP/1.1

HTTP/1.1 200 OK
Content-Type: application/json

[
    {
        "id": integer,
        "name": string
    }
]
```

### Create Tag

```http
POST /tags HTTP/1.1
Content-Type: application/json

{
    "name": string
}

HTTP/1.1 201 Created
{
    "message": "Success"
}

HTTP/1.1 400 Bad Request
Content-Type: application/json

{
    "message": "Validation error"
}
```

## Status Codes

| Code | Description                             |
| ---- | --------------------------------------- |
| 200  | OK - Request successful                 |
| 201  | Created - Resource created successfully |
| 400  | Bad Request - Invalid request format    |
| 406  | Not Acceptable - Authentication failed  |
| 422  | Unprocessable Entity - Validation error |

## Note

PUT and DELETE endpoints are currently under development.
