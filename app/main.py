from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.agents_routes import agents_router
from app.routers.auth_routes import auth_router
from app.routers.commons import commons_router


app = FastAPI(responses={404: {"description": "Not Found"}})

allowed_origins = [
    "https://127.0.0.1",
    "http://127.0.0.1",
    "http://localhost",
    "https://localhost",
    "https://localhost:5173",
    "http://localhost:5173",
    "http://localhost:4173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Set-Cookie"],
)

app.include_router(agents_router)
app.include_router(auth_router)
app.include_router(commons_router)
app.include_router(agents_router)
