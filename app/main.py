from fastapi import FastAPI

from app.routers.agents import agents_router


app = FastAPI(
    responses = {404: {"description": "Not Found"}}
)

app.include_router(agents_router)
