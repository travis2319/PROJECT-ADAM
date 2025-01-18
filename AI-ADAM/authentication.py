# from datetime import datetime, timedelta
# from typing import Optional, Dict, Any
# import jwt
# from fastapi import HTTPException, Security, Depends
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# import bcrypt
# import log_config
# from log_config import Logger
# import json
#
#
# class AuthConfig:
#     """Authentication Configuration"""
#     CURRENT_UTC_TIME = "2025-01-18 12:20:05"
#     CURRENT_USER = "VOID-001"
#     SECRET_KEY = "your-secret-key-here"  # Change this in production
#     ALGORITHM = "HS256"
#     ACCESS_TOKEN_EXPIRE_MINUTES = 30
#     REFRESH_TOKEN_EXPIRE_DAYS = 7
#
#     # Password requirements
#     MIN_PASSWORD_LENGTH = 8
#     REQUIRE_SPECIAL_CHAR = True
#     REQUIRE_NUMBER = True
#     REQUIRE_UPPERCASE = True
#
#
# class AuthHandler:
#     """Authentication handler class"""
#     security = HTTPBearer()
#
#     def __init__(self, logger: Optional[Logger] = None):
#         self.secret_key = AuthConfig.SECRET_KEY
#         self.algorithm = AuthConfig.ALGORITHM
#         self.logger = logger or logging.getLogger(__name__)
#
#     def _hash_password(self, password: str) -> str:
#         """Hash a password using bcrypt."""
#         return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
#
#     def verify_password(self, plain_password: str, hashed_password: str) -> bool:
#         """Verify a password against its hash."""
#         return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())
#
#     def validate_password_strength(self, password: str) -> bool:
#         """Validate password meets security requirements."""
#         if len(password) < AuthConfig.MIN_PASSWORD_LENGTH:
#             return False
#         if AuthConfig.REQUIRE_SPECIAL_CHAR and not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
#             return False
#         if AuthConfig.REQUIRE_NUMBER and not any(c.isdigit() for c in password):
#             return False
#         if AuthConfig.REQUIRE_UPPERCASE and not any(c.isupper() for c in password):
#             return False
#         return True
#
#     def encode_token(self, user_id: str, is_refresh: bool = False) -> str:
#         """Generate JWT token."""
#         try:
#             if is_refresh:
#                 expiration = datetime.utcnow() + timedelta(days=AuthConfig.REFRESH_TOKEN_EXPIRE_DAYS)
#                 token_type = "refresh"
#             else:
#                 expiration = datetime.utcnow() + timedelta(minutes=AuthConfig.ACCESS_TOKEN_EXPIRE_MINUTES)
#                 token_type = "access"
#
#             payload = {
#                 "exp": expiration,
#                 "iat": datetime.utcnow(),
#                 "sub": user_id,
#                 "type": token_type
#             }
#             return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
#         except Exception as e:
#             self.logger.error(f"Token encoding error: {str(e)}")
#             raise HTTPException(status_code=500, detail="Token generation failed")
#
#     def decode_token(self, token: str) -> Dict[str, Any]:
#         """Decode and validate JWT token."""
#         try:
#             payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
#             if payload["type"] not in ["access", "refresh"]:
#                 raise HTTPException(status_code=401, detail="Invalid token type")
#             return payload
#         except jwt.ExpiredSignatureError:
#             raise HTTPException(status_code=401, detail="Token has expired")
#         except jwt.InvalidTokenError as e:
#             raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
#
#     def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)) -> Dict[str, Any]:
#         """Wrapper for token validation in FastAPI endpoints."""
#         try:
#             return self.decode_token(auth.credentials)
#         except Exception as e:
#             self.logger.error(f"Authentication error: {str(e)}")
#             raise HTTPException(status_code=401, detail="Invalid authentication")
#
#     def get_current_user(self, auth: HTTPAuthorizationCredentials = Security(security)) -> str:
#         """Get current user from token."""
#         payload = self.decode_token(auth.credentials)
#         return payload.get("sub")
#
#
# class SessionManager:
#     """Manage user sessions"""
#
#     def __init__(self):
#         self.active_sessions: Dict[str, Dict[str, Any]] = {}
#         self.logger = logging.getLogger(__name__)
#
#     def create_session(self, user_id: str, metadata: Dict[str, Any]) -> None:
#         """Create a new user session."""
#         self.active_sessions[user_id] = {
#             "created_at": datetime.utcnow(),
#             "last_activity": datetime.utcnow(),
#             "metadata": metadata
#         }
#         self.logger.info(f"Created session for user {user_id}")
#
#     def end_session(self, user_id: str) -> None:
#         """End a user session."""
#         if user_id in self.active_sessions:
#             del self.active_sessions[user_id]
#             self.logger.info(f"Ended session for user {user_id}")
#
#     def update_session_activity(self, user_id: str) -> None:
#         """Update last activity timestamp for a session."""
#         if user_id in self.active_sessions:
#             self.active_sessions[user_id]["last_activity"] = datetime.utcnow()
#
#
# # Example usage
# auth_handler = AuthHandler()
# session_manager = SessionManager()
#
#
# def get_current_user_id(credentials: HTTPAuthorizationCredentials = Security(HTTPBearer())) -> str:
#     """FastAPI dependency for getting current user."""
#     payload = auth_handler.decode_token(credentials.credentials)
#     return payload["sub"]
#
#
# # Example protected endpoint decorator
# def require_auth(user_id: str = Depends(get_current_user_id)):
#     """Decorator for protected endpoints."""
#
#     def decorator(func):
#         async def wrapper(*args, **kwargs):
#             session_manager.update_session_activity(user_id)
#             return await func(*args, **kwargs)
#
#         return wrapper
#
#     return decorator