import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from main.controllers.health_controller import router as health_router

app = FastAPI(title="aws-bedrock-sanity-service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/sanity-app/v1")

if __name__ == "__main__":
    uvicorn.run("src.main.app:app", host="0.0.0.0", port=8000, reload=True)