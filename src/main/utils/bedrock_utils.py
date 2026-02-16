import logging
import os

import boto3
from dotenv import load_dotenv

from main.config.bedrock_configs import GUARDRAIL_CONFIG

load_dotenv()

logger = logging.getLogger(__name__)

default_prompt_id = os.getenv("AWS_BEDROCK_DEFAULT_PROMPT_ID")
default_model_id = os.getenv("AWS_BEDROCK_DEFAULT_MODEL_ID")
default_prompt_version = os.getenv("AWS_BEDROCK_DEFAULT_PROMPT_VERSION")
aws_region = os.getenv("AWS_REGION")

bedrock_agent = boto3.client("bedrock-agent", region_name=aws_region)
bedrock_runtime = boto3.client("bedrock-runtime", region_name=aws_region)

def get_default_prompt() -> str:
    rendered_prompt = bedrock_agent.get_prompt(
        promptIdentifier=default_prompt_id,
        promptVersion=default_prompt_version 
    )
    system_text = rendered_prompt['variants'][0]['templateConfiguration']['text']['text']
    return system_text

def get_default_model() -> str:
    return default_model_id

def get_generic_prompt(prompt_id: str, prompt_version: str = None) -> str:
    if prompt_version is None:
        prompt_version = default_prompt_version
    rendered_prompt = bedrock_agent.get_prompt(
        promptIdentifier=prompt_id,
        promptVersion=prompt_version
    )
    system_text = rendered_prompt['variants'][0]['templateConfiguration']['text']['text']
    return system_text

def get_generic_model(model_id: str) -> str:
    return model_id


def generate_response(user_prompt: str, model_id: str, system_prompt: str) -> str:
    logger.info("Generating Bedrock response", extra={"model_id": model_id})
    try:
        response = bedrock_runtime.converse(
            modelId=model_id,
            messages=[{"role": "user", "content": [{"text": user_prompt}]}],
            system=[{"text": system_prompt}],
            guardrailConfig=GUARDRAIL_CONFIG,
        )
        return response["output"]["message"]["content"][0]["text"]
    except Exception as e:
        logger.error("Bedrock converse failed", extra={"model_id": model_id, "error": str(e)})
        raise
