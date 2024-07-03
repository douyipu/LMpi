from typing import Dict, List

MODEL_REGISTRY: Dict[str, Dict[str, List[str]]] = {
    "openai": {
        "api": ["gpt-3.5-turbo", "gpt-4", "text-davinci-002", "text-davinci-003"]
    },
    "anthropic": {
        "api": ["claude-1", "claude-2", "claude-instant-1"]
    },
    "cohere": {
        "api": ["command", "command-light", "command-nightly"]
    },
    "huggingface": {
        "huggingface": ["bert-base-uncased", "gpt2", "t5-base"]
    }
}

def get_company_for_model(model_name: str) -> str:
    for company, types in MODEL_REGISTRY.items():
        for model_type, models in types.items():
            if model_name in models:
                return company
    return None

def get_model_type(model_name: str) -> str:
    for company, types in MODEL_REGISTRY.items():
        for model_type, models in types.items():
            if model_name in models:
                return model_type
    return None

def list_available_models() -> Dict[str, List[str]]:
    available_models = {}
    for company, types in MODEL_REGISTRY.items():
        available_models[company] = []
        for models in types.values():
            available_models[company].extend(models)
    return available_models

def is_valid_model(model_name: str) -> bool:
    return get_company_for_model(model_name) is not None