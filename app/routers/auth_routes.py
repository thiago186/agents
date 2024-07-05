from fastapi import APIRouter

from app.models.auth_model import authHandler
from app.views.users_schema import UserSchema


auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@auth_router.post("/login")
def login(user: UserSchema):
    """This route receives an UserBase Object"""