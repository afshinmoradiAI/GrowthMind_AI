from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager

from app.api.routes_auth import router as auth_router
from app.api.routes_content import router as content_router
from app.api.routes_crm import router as crm_router
from app.api.routes_leads import router as leads_router
from app.core.config import settings
from app.core.database import init_db


@asynccontextmanager
async def lifespan(_app):
    init_db()
    yield

app = FastAPI(title="GrowthMind AI", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(content_router)
app.include_router(leads_router)
app.include_router(crm_router)


@app.get("/health")
async def health():
    return {"status": "ok"}
