from fastapi import APIRouter, Response, Depends, Request

from app.middleware.auth_middleware import authenticate_user, is_valid_token, access_required
from app.views.users_schema import UserBaseSchema
from app.views.organization_schema import OrganizationRoles

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@auth_router.post("/login")
def login(user: UserBaseSchema, response: Response):
    """This route receives an UserBase Object"""

    auth_token = authenticate_user(user)

    # Set the JWT token as a cookie
    response.set_cookie(
        key="token",
        value=auth_token,
        httponly=True,
        secure=True,
        samesite="none"
        )

    return {"status": "ok"}

@auth_router.get("/verify", dependencies=[Depends(is_valid_token)])
def auth_test(request: Request):
    """This route is a test for the authentication middleware"""
    
    # api_logger.debug(f"Request headers: {request.headers}")
    return {"valid": True}


@auth_router.get("/test-role-admin", dependencies=[Depends(is_valid_token)])
@access_required(access_level=OrganizationRoles.admin)
def access_test_role_admin(request: Request):
    """This route is a test for the authentication middleware"""

    return {"message": "You have access!"}


@auth_router.get("/test-role-manager", dependencies=[Depends(is_valid_token)])
@access_required(access_level=OrganizationRoles.manager)
def access_test_role_manager(request: Request):
    """This route is a test for the authentication middleware"""

    return {"message": "You have access!"}


@auth_router.get("/test-role-user", dependencies=[Depends(is_valid_token)])
@access_required(access_level=OrganizationRoles.user)
def access_test_role_user(request: Request):
    """This route is a test for the authentication middleware"""

    return {"message": "You have access!"}

