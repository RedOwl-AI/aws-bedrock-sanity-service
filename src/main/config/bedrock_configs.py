import os
from dotenv import load_dotenv

load_dotenv()

guardrail_id = os.getenv('AWS_BEDROCK_GUARDRAIL_ID')
guardrail_version = os.getenv('AWS_BEDROCK_GUARDRAIL_VERSION')

GUARDRAIL_CONFIG = {
    'guardrailIdentifier': guardrail_id,
    'guardrailVersion': guardrail_version,
    'trace': 'enabled'
}