import hashlib
from datetime import datetime, timedelta

import jwt


SECRET_KEY = "route53-demo-secret-key"

ALGORITHM = "HS256"


def create_token(user_id: int):

    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def decode_token(token: str):

    try:

        return jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

    except jwt.InvalidTokenError:

        return None


def hash_password(password: str):

    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


def verify_password(
    password: str,
    hashed_password: str
):

    return hash_password(password) == hashed_password