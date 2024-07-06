from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.agents import agents_router
from app.routers.auth_routes import auth_router


app = FastAPI(
    responses = {404: {"description": "Not Found"}}
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "http://localhost:3000"],  # Ajuste conforme necessário
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agents_router)
app.include_router(auth_router)
