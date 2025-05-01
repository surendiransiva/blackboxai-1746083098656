from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from .config import settings

security = HTTPBearer()

def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.SUPABASE_KEY, algorithms=["HS256"], options={"verify_aud": False})
        return payload
    except JWTError:
        return None

async def get_current_user(request: Request):
    credentials: HTTPAuthorizationCredentials = await security(request)
    if credentials:
        token = credentials.credentials
        payload = verify_token(token)
        if payload is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return payload
    else:
        raise HTTPException(status_code=401, detail="Authorization header missing")
