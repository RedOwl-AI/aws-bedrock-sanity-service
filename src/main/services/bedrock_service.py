from src.main.utils.bedrock_utils import generate_response, get_default_prompt, get_default_model, get_generic_model, get_generic_prompt

def generate_default_response(user_prompt: str) -> str:
    system_prompt = get_default_prompt()
    model_id = get_default_model()
    return generate_response(user_prompt, model_id, system_prompt)

def generate_response_with_custom_prompt_id(user_prompt: str, prompt_id: str, model_id: str) -> str:
    system_prompt = get_generic_prompt(prompt_id)
    model_id = get_generic_model(model_id)
    return generate_response(user_prompt, model_id, system_prompt)

def generate_response_with_custom_system_prompt(user_prompt: str, system_prompt: str, model_id: str) -> str:
    system_prompt = system_prompt
    model_id = get_generic_model(model_id)
    return generate_response(user_prompt, model_id, system_prompt)