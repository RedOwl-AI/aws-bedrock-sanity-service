import logging
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.main.controllers.bedrock_controller import router as bedrock_router
from src.main.controllers.health_controller import router as health_router

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="aws-bedrock-sanity-service")


@app.on_event("startup")
def startup():
    logger.info("aws-bedrock-sanity-service started")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/sanity-app/v1")
app.include_router(bedrock_router, prefix="/sanity-app/v1")

if __name__ == "__main__":
    uvicorn.run("src.main.app:app", host="0.0.0.0", port=8000, reload=True)