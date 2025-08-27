from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from app.database import Base, engine
from app import models
from app.routers import candidates

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="TailentTrail")

# CORS (open by default; tighten for prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"message": "API is running on Vercel!"}

app.include_router(candidates.router)

# At bottom of main.py
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)