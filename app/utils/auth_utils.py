"""This module contains the utility functions for authentication"""
from fastapi import Request, HTTPException

from app.models.auth_model import authHandler

def decode_jwt(request: Request) -> dict:
    """
    This function receives a request object and decodes the JWT token
    """
    try:

        if not isinstance(request, Request):
            raise Exception("'decode_jwt' function must receive a Request object")

        token = request.cookies.get("token")
        if not token:
            raise HTTPException(status_code=401, detail="Authentication token not found")
        
        if not authHandler.verify_token(token):
            raise HTTPException(status_code=401, detail="Invalid token")

        payload = authHandler.decode_token(token)
        return payload
    
    except Exception as e:
        raise e
