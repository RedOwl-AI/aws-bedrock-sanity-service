from fastapi import APIRouter
from src.main.models.bedrock_models import GenerateResponseRequest

router = APIRouter(prefix="/bedrock-router", tags=["Bedrock Router"])