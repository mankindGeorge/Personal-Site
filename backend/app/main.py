from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routers import docs_router, announcements_router, auth_router, sse_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="George's Geek Space API",
    description="极客网站后端 API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(docs_router)
app.include_router(announcements_router)
app.include_router(auth_router)
app.include_router(sse_router)


@app.get("/")
def root():
    return {"message": "George's Geek Space API", "version": "1.0.0"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
