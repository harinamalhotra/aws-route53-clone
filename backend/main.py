from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine, SessionLocal
from models import User

from auth import hash_password

from routers import auth
from routers import zones
from routers import records


# =====================================
# CREATE DATABASE TABLES
# =====================================

Base.metadata.create_all(
    bind=engine
)


# =====================================
# CREATE FASTAPI APPLICATION
# =====================================

app = FastAPI(
    title="AWS Route53 Clone API",
    description="Mock Route53 backend",
    version="1.0.0"
)


# =====================================
# CORS
# =====================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:3000"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# =====================================
# CREATE DEMO USER
# =====================================

def create_demo_user():

    db = SessionLocal()

    existing_user = db.query(
        User
    ).filter(
        User.email == "admin@example.com"
    ).first()

    if not existing_user:

        user = User(
            name="Route53 Admin",

            email="admin@example.com",

            password=hash_password(
                "password123"
            )
        )

        db.add(user)

        db.commit()

    db.close()


create_demo_user()


# =====================================
# API ROUTES
# =====================================

app.include_router(
    auth.router,
    prefix="/api/auth",
    tags=["Authentication"]
)


app.include_router(
    zones.router,
    prefix="/api/zones",
    tags=["Hosted Zones"]
)


app.include_router(
    records.router,
    prefix="/api",
    tags=["DNS Records"]
)


# =====================================
# ROOT
# =====================================

@app.get("/")
def root():

    return {
        "message": "AWS Route53 Clone API is running"
    }