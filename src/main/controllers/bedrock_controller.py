import logging

from fastapi import APIRouter, HTTPException

from src.main.models.bedrock_models import (
    GenerateDefaultResponseRequest,
    GenerateResponseCustomPromptIDRequest,
    GenerateResponseCustomSystemPromptRequest,
)
from src.main.services.bedrock_service import (
    generate_default_response,
    generate_response_with_custom_prompt_id,
    generate_response_with_custom_system_prompt,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/bedrock-router", tags=["Bedrock Router"])


@router.post("/generate-default-response")
def generate_default_response_endpoint(request: GenerateDefaultResponseRequest):
    try:
        return generate_default_response(request.user_prompt)
    except Exception as e:
        logger.error("generate-default-response failed", extra={"error": str(e)})
        raise HTTPException(status_code=500, detail="Failed to generate response") from e


@router.post("/generate-response-custom-prompt-id")
def generate_response_with_custom_prompt_id_endpoint(request: GenerateResponseCustomPromptIDRequest):
    try:
        return generate_response_with_custom_prompt_id(
            request.user_prompt, request.prompt_id, request.model_id
        )
    except Exception as e:
        logger.error("generate-response-custom-prompt-id failed", extra={"error": str(e)})
        raise HTTPException(status_code=500, detail="Failed to generate response") from e


@router.post("/generate-response-custom-system-prompt")
def generate_response_with_custom_system_prompt_endpoint(request: GenerateResponseCustomSystemPromptRequest):
    try:
        return generate_response_with_custom_system_prompt(
            request.user_prompt, request.system_prompt, request.model_id
        )
    except Exception as e:
        logger.error("generate-response-custom-system-prompt failed", extra={"error": str(e)})
        raise HTTPException(status_code=500, detail="Failed to generate response") from e