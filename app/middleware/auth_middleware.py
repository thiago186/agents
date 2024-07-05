"""This module contains the middleware for the authentications matters in the application"""

from fastapi import HTTPException, Request

from app.models.auth_model import authHandler

