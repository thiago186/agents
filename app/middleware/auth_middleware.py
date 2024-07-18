"""This module contains the middleware for the authentications matters in the application"""
from functools import wraps

from fastapi import HTTPException, Request

from app.models.auth_model import authHandler
from app.models.bcrypt_model import bcrypt_manager
from app.models.users_model import usersCollection
from app.models.organizations_model import organizationsCollection
from app.views.organization_schema import OrganizationSchema, OrganizationRoles
from app.views.users_schema import UserBaseSchema
from app.logging_config import api_logger

def authenticate_user(user: UserBaseSchema):
    """
    This function performs the authentication of a user. It receives a UserBaseSchema object
    and returns a JWT token if the informed credentials are valid

    """

    try:
        user_in_db  = usersCollection.retrieve_user_by_email(user.email)

        if not user_in_db:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        if not bcrypt_manager.check_password(user.password, user_in_db.hashed_password):
            api_logger.error(f"Invalid credentials for user {user_in_db.id}")
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        jwt_token = authHandler.create_access_token(data={"sub": user_in_db.id})
        return jwt_token
    
    except Exception as e:
        raise e


def is_valid_token(request: Request):
    """
    This function will be used as Depends on routes that require authentication
    """
    api_logger.debug("Validating token")
    try:
        token = request.cookies.get("token")
        # api_logger.debug(f"Token: {token}")
        if not token:
            api_logger.error("No credentials provided")
            raise HTTPException(status_code=401, detail="No credentials provided")
        
        payload = authHandler.verify_token(token)
        # api_logger.debug(f"Payload: {payload}")
        return payload
    
    except Exception as e:
        raise e
    

def access_required(access_level: OrganizationRoles):
    """
    Decorator function to check if the user has access to a given route

    Args:
        - user_id: in the "sub" field of the jwt token passed as a cookie
        - organization_id: in the "organizationId" field of the request headers
        - access_level: the required access level to access the route. Passed as an argument to the decorator
    """

    if not isinstance(access_level, OrganizationRoles):
        raise TypeError("access_level must be an instance of OrganizationRoles")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            request: Request = kwargs.get('request')
            if not request:
                for arg in args:
                    if isinstance(arg, Request):
                        request = arg
                        break
                raise HTTPException(status_code=500, detail="Request object not found")

            organization_id = request.headers.get('organizationId', None)
            token = request.cookies.get("token", None)

            if not organization_id:
                raise HTTPException(status_code=401, detail="No organizationId provided")
            
            if not token:
                raise HTTPException(status_code=401, detail="Invalid credentials")
            
            decoded_token = authHandler.decode_token(token)
            user_id = decoded_token.get('sub')

            has_access = organizationsCollection.user_has_role(user_id, organization_id, access_level)
            
            if not has_access:
                raise HTTPException(status_code=403, detail="User does not have access to this resource")
            
            return func(*args, **kwargs)
        return wrapper
    return decorator
