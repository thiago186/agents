"""This file contains all the routes that are used in the common parts of the application"""

from fastapi import APIRouter, Depends, Request, HTTPException

from app.models.organizations_model import organizationsCollection
from app.middleware.auth_middleware import is_valid_token
from app.utils.auth_utils import decode_jwt


commons_router = APIRouter(
    prefix="/commons",
    tags=["commons"],
    responses={404: {"description": "Route not found"}}
)

@commons_router.get("/user-orgs", dependencies=[Depends(is_valid_token)])
async def get_user_orgs(request: Request):
    """This route gets the user_id from the JWT token and returns the organizations that the user is part of"""
    try:
        decoded_jwt = decode_jwt(request)
        print(f"Decoded JWT: {decoded_jwt}")
        user_id = decoded_jwt.get("sub", None)
        print(f"User ID: {user_id}")

        if not user_id:
            raise Exception("User not found in the token")
        
        user_orgs = organizationsCollection.retrieve_user_organizations(user_id)
        print(f"User Orgs: {user_orgs}")
        user_orgs = [
            {
                "organizationName": org.organization_name,
                "role": org.members.get(user_id),
                "organizationId": org.id,
            } for org in user_orgs
        ]

        return {"organizations": user_orgs}
    
    except Exception:
        # api_logger.exception("An error occurred while retrieving the user organizations")
        raise HTTPException(status_code=500, detail="An error occurred while retrieving the user organizations")
