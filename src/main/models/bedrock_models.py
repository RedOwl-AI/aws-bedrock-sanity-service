from pydantic import BaseModel

class GenerateDefaultResponseRequest(BaseModel):
    user_prompt: str

class GenerateResponseCustomPromptIDRequest(BaseModel):
    user_prompt: str
    prompt_id: str
    model_id: str

class GenerateResponseCustomSystemPromptRequest(BaseModel):
    user_prompt: str
    system_prompt: str
    model_id: str