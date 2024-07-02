from fastapi import APIRouter, Depends


agents_router = APIRouter(
    prefix="/agents",
    tags=["agents"],
    responses={404: {"description": "Route not found"}}
)

@agents_router.get("/test")
async def agents_api_test():
    return {"message": "Agents API is working!"}