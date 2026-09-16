# Blog Management API

A mini blogging system built with FastAPI, SQLite, SQLAlchemy, JWT authentication, and email notifications.

## Features

- User registration
- User login
- JWT authentication
- Password hashing
- Create blog posts
- View blog posts
- Update own posts
- Delete own posts
- View own posts
- Add comments
- View comments
- Like posts
- Unlike posts
- Prevent duplicate likes
- Email notification for comments
- Email notification for likes
- Input validation
- Swagger UI

## Technologies

- Python
- FastAPI
- SQLite
- SQLAlchemy
- Pydantic
- JWT
- bcrypt
- SMTP

## Project Structure

```text
blog_management_api/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── config.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── post.py
│   │   ├── comment.py
│   │   └── like.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── auth.py
│   │   ├── post.py
│   │   ├── comment.py
│   │   └── like.py
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── posts.py
│   │   ├── comments.py
│   │   └── likes.py
│   │
│   ├── dependencies/
│   │   ├── __init__.py
│   │   └── auth.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── email_service.py
│   │
│   └── utils/
│       ├── __init__.py
│       ├── security.py
│       └── jwt.py
│
├── .env
├── .gitignore
├── requirements.txt
├── README.md
└── blog.db