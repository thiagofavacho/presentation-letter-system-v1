from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app import models
from app.routes import auth, letters, promoters, stores, users

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Presentation Letter System",
    description="API for managing and generating cover letters.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://presentation-letter-system-frt.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(promoters.router)
app.include_router(stores.router)
app.include_router(letters.router)


@app.get("/")
def home():
    return {
        "message": "Presentation Letter System is running successfully!"
    }