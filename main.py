
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, EmailStr, Field
from supabase import Client, create_client

# Load environment variables from .env
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError(
        "SUPABASE_URL and SUPABASE_KEY must be set in your .env file"
    )

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Adds the Authorize button in Swagger UI
security = HTTPBearer(auto_error=False)


class AuthRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)


app = FastAPI(title="FlyRank Assignment 4 - Auth API")


@app.get("/")
def root():
    return {"message": "FlyRank Assignment 4 Auth API is running"}


# Public endpoint
@app.get("/public/info")
def public_info():
    return {"message": "Welcome! This information is public."}


# Signup
@app.post("/auth/signup", status_code=status.HTTP_201_CREATED)
def signup(data: AuthRequest):
    try:
        result = supabase.auth.sign_up(
            {
                "email": str(data.email),
                "password": data.password,
            }
        )

        if not result.user:
            raise HTTPException(
                status_code=400,
                detail="Supabase could not create the user.",
            )

        return {
            "message": "Signup request successful",
            "user": {
                "id": result.user.id,
                "email": result.user.email,
            },
            "email_confirmation_required": result.session is None,
        }

    except HTTPException:
        raise
    except Exception as exc:
        # Print the real error in the VS Code terminal for debugging.
        print("SUPABASE SIGNUP ERROR:", repr(exc))
        raise HTTPException(
            status_code=400,
            detail="Signup failed. Check the VS Code terminal for details.",
        ) from exc


# Login
@app.post("/auth/login")
def login(data: AuthRequest):
    try:
        result = supabase.auth.sign_in_with_password(
            {
                "email": str(data.email),
                "password": data.password,
            }
        )

        if not result.session:
            raise HTTPException(
                status_code=401,
                detail="Invalid login credentials.",
            )

        return {
            "access_token": result.session.access_token,
            "refresh_token": result.session.refresh_token,
            "token_type": "bearer",
        }

    except HTTPException:
        raise
    except Exception as exc:
        print("SUPABASE LOGIN ERROR:", repr(exc))
        raise HTTPException(
            status_code=401,
            detail="Invalid login credentials.",
        ) from exc


# Reusable authentication dependency
def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
):
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=401,
            detail="Access token required. Use the Authorize button.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        result = supabase.auth.get_user(credentials.credentials)

        if not result.user:
            raise HTTPException(
                status_code=401,
                detail="Invalid or expired access token.",
            )

        return result.user

    except HTTPException:
        raise
    except Exception as exc:
        print("TOKEN VERIFICATION ERROR:", repr(exc))
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired access token.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc


# Protected profile endpoint
@app.get("/protected/profile")
def profile(user=Depends(get_current_user)):
    return {
        "id": user.id,
        "email": user.email,
        "created_at": user.created_at,
    }


# Second protected endpoint
@app.get("/protected/dashboard")
def dashboard(user=Depends(get_current_user)):
    return {
        "message": "Welcome to your protected dashboard!",
        "user_id": user.id,
        "email": user.email,
    }


# Protected logout endpoint
@app.post("/auth/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    user=Depends(get_current_user),
):
    try:
        # Use the authenticated user's token for sign-out.
        user_client = create_client(SUPABASE_URL, SUPABASE_KEY)
        user_client.auth.set_session(
            credentials.credentials,
            "",
        )
        user_client.auth.sign_out()
        return None

    except Exception as exc:
        print("SUPABASE LOGOUT ERROR:", repr(exc))
        raise HTTPException(
            status_code=400,
            detail="Logout failed. Check the VS Code terminal.",
        ) from exc
