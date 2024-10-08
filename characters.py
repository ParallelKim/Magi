from openai import OpenAI
from typing import Tuple, List, Dict, Optional
import json
from colorama import Fore
from prompts import SYSTEM_COMMON_PROMPT
from utils import init_logger

class Character:
    def __init__(self, name: str, model_name: str, personas: str, magi):
        self.name = name
        self.model_name = model_name
        self.personas = personas
        self.client = OpenAI()
        self.logger = init_logger(name)
        self.magi = magi

    def create_completion(self, messages: List[Dict[str, str]]) -> str:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            response_format={"type": "json_object" if any("json" in message["content"].lower() for message in messages) else "text"},
        )
        return response.choices[0].message.content
       
        
    def update_prompt(self, original: str, output) -> Tuple[str, List[str]]:
        user_content = f"Prompt: {original}\n\nOutput: {output}\n\n"
        messages = [
            {"role": "system", "content": "Your name is " + self.name + " and " + self.personas + SYSTEM_COMMON_PROMPT + f'Expected purpose from user initial prompt is {self.magi.original_purpose}. Check if the improved prompt is aligned with the original purpose. Answer in {self.magi.original_language}'},
            {"role": "user", "content": user_content},
        ]
        updated = self.create_completion(messages)

        if not updated:
            self.logger.warning("No updated prompt returned from the LLM.")
            return "", []
        
        updated = json.loads(updated)
        updated_prompt = updated.get("updated_prompt", "")

        return updated_prompt
        
    def upgrade_prompt(self, initial_prompt: str, out: str) -> Dict[str, str]:
        work = {}

        updated_prompt = self.update_prompt(initial_prompt, out)

        self.logger.info(Fore.YELLOW + "Updated Prompt: " + updated_prompt)

        work["initial_prompt"] = initial_prompt
        work["updated_prompt"] = updated_prompt
    
        return work