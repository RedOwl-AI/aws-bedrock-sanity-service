from fastapi import APIRouter
from src.main.services.bedrock_service import generate_default_response, generate_response_with_custom_prompt_id, generate_response_with_custom_system_prompt
from src.main.models.bedrock_models import GenerateDefaultResponseRequest, GenerateResponseCustomPromptIDRequest, GenerateResponseCustomSystemPromptRequest

router = APIRouter(prefix="/bedrock-router", tags=["Bedrock Router"])

@router.post("/generate-default-response")
def generate_default_response_endpoint(request: GenerateDefaultResponseRequest):
    return generate_default_response(request.user_prompt)

@router.post("/generate-response-custom-prompt-id")
def generate_response_with_custom_prompt_id_endpoint(request: GenerateResponseCustomPromptIDRequest):
    return generate_response_with_custom_prompt_id(request.user_prompt, request.prompt_id, request.model_id)

@router.post("/generate-response-custom-system-prompt")
def generate_response_with_custom_system_prompt_endpoint(request: GenerateResponseCustomSystemPromptRequest):
    return generate_response_with_custom_system_prompt(request.user_prompt, request.system_prompt, request.model_id)