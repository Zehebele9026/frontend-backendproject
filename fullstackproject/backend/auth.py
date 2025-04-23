from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = "gizli-anahtar"
ALGORITHM = "HS256"
EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
