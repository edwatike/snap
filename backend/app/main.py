from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import search, emails, auth
from app.db import init_db

app = FastAPI(title="B2B Search Service")

# CORS настройки
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(search.router, prefix="/api/search", tags=["search"])
app.include_router(emails.router, prefix="/api/emails", tags=["emails"])

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.get("/")
async def root():
    return {"message": "Hello World"} 