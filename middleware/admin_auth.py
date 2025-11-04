"""
Admin authentication middleware for ThirdEye
Uses simple session tokens for admin access
"""
from fastapi import HTTPException, Header
from typing import Optional
import secrets
import os
from datetime import datetime, timedelta

# Store active sessions in memory (use Redis/DB in production)
_active_sessions = {}

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
SESSION_DURATION_HOURS = 24


def generate_session_token() -> str:
    """Generate a secure random session token"""
    return secrets.token_urlsafe(32)


def verify_admin_password(password: str) -> bool:
    """Verify if the provided password matches admin password"""
    return password == ADMIN_PASSWORD


def create_admin_session() -> dict:
    """Create a new admin session and return session data"""
    token = generate_session_token()
    expires_at = datetime.utcnow() + timedelta(hours=SESSION_DURATION_HOURS)
    
    _active_sessions[token] = {
        "created_at": datetime.utcnow(),
        "expires_at": expires_at,
    }
    
    return {
        "token": token,
        "expires_at": expires_at.isoformat(),
    }


def verify_admin_session(token: str) -> bool:
    """Verify if a session token is valid and not expired"""
    if token not in _active_sessions:
        return False
    
    session = _active_sessions[token]
    if datetime.utcnow() > session["expires_at"]:
        # Session expired, remove it
        del _active_sessions[token]
        return False
    
    return True


def revoke_admin_session(token: str) -> bool:
    """Revoke an admin session"""
    if token in _active_sessions:
        del _active_sessions[token]
        return True
    return False


async def require_admin_auth(authorization: Optional[str] = Header(None)) -> str:
    """
    Dependency to require admin authentication
    Expects Authorization header with format: Bearer <token>
    Returns the token if valid, raises HTTPException otherwise
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")
    
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization header format")
    
    token = parts[1]
    if not verify_admin_session(token):
        raise HTTPException(status_code=401, detail="Invalid or expired session")
    
    return token
