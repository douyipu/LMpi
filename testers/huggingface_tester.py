import logging
import sys
from typing import Dict
from .base_tester import ModelTester

class HuggingFaceModelTester(ModelTester):
    def __init__(self, model_name: str):
        try:
            from transformers import AutoTokenizer, AutoModelForCausalLM
        except ImportError:
            logging.error("transformers library not installed. Install it to test Hugging Face models.")
            sys.exit(1)
        
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)

    def test(self, prompt: str) -> Dict:
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(**inputs)
        response = self.tokenizer.decode(outputs[0])
        return {"type": "HuggingFace", "model": self.model_name, "prompt": prompt, "response": response}