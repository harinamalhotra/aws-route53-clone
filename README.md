# AWS Route 53 Clone

A simplified AWS Route 53 clone built using Next.js, TypeScript, FastAPI and SQLite.

## Project Overview

This project demonstrates the basic functionality of a DNS management system inspired by AWS Route 53.

The application contains:

- Mock user authentication
- Hosted Zone management
- DNS Record management
- REST APIs using FastAPI
- SQLite database for persistence
- Next.js and TypeScript frontend
- Swagger API documentation

## Technology Stack

### Frontend
- Next.js
- TypeScript
- React
- CSS

### Backend
- Python
- FastAPI
- SQLAlchemy
- SQLite
- JWT authentication

## Features

### Authentication
- Demo login system
- JWT based authentication
- Demo credentials:

Email:
`admin@example.com`

Password:
`password123`

### Hosted Zones

The backend supports:

- Create hosted zone
- View hosted zones
- Search hosted zones
- Update hosted zone
- Delete hosted zone

### DNS Records

The backend supports DNS records including:

- A
- AAAA
- CNAME
- TXT
- MX
- NS
- PTR
- SRV
- CAA

Record operations include:

- Create
- Read
- Update
- Delete
- Search

## Project Structure

```text
aws-route53-clone/
│
├── backend/
│   ├── routers/
│   │   ├── auth.py
│   │   ├── zones.py
│   │   └── records.py
│   ├── auth.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── requirements.txt
│   └── route53.db
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── tsconfig.json
│
└── README.md