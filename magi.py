import json
from typing import Tuple, List, Dict, Optional
from colorama import Fore, Back, Style, init
import concurrent.futures
from characters import Character
from openai import OpenAI

from prompts import PERSONA_PROMPT, SYSTEM_MAGI_PROMPT
from utils import init_logger

class Magi(Character):
    def __init__(self, model_name: str):
        self.client = OpenAI()
        self.model_name = model_name
        self.logger = init_logger('Magi')
        self.original_language = None
        self.original_purpose = None
        self.characters = [
            Character(name="🧙 Melchior", personas=PERSONA_PROMPT["🧙 Melchior"], model_name=model_name),
            Character(name="🧑‍💻 Balthasar", personas=PERSONA_PROMPT["🧑‍💻 Balthasar"], model_name=model_name),
            Character(name="👶 Caspar", personas=PERSONA_PROMPT["👶 Caspar"], model_name=model_name),
        ]

    def translate_to_english(self, text: str) -> str:
        messages = [
            {"role": "system", "content": "You are a professional translator. Please translate the given text into English. Present just the translation result."},
            {"role": "user", "content": f"Translate the following text into English: {text}"}
        ]
        out = self.create_completion(messages)
        return out

    def translate_to_original_language(self, text: str) -> str:
        messages = [
            {"role": "system", "content": f"You are a professional translator. Please translate the given text into {self.original_language}. Present just the translation result."},
            {"role": "user", "content": f"Translate the following text into {self.original_language}: {text}"}
        ]
        out = self.create_completion(messages)
        return out

    def analyze_initial_prompt(self, initial_prompt: str) -> Dict[str, str]:
        messages = [
            {"role": "system", "content": "You are an expert in analyzing the initial prompt. Extract the following two pieces of information: 1) The language of the prompt, 2) The user's intention and purpose. Present the result in JSON format like this: {'language': '...', 'intention_and_purpose': '...'}"},
            {"role": "user", "content": f"Analyze the following prompt: {initial_prompt}"}
        ]
        out = self.create_completion(messages)
        analysis = json.loads(out)
        return analysis['language'], analysis['intention_and_purpose']

    def run_character_prompts(self, initial_prompt: str, rounds: int) -> Dict[str, str]:
        results = {}

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_character = {
                executor.submit(character.upgrade_prompt, initial_prompt, rounds): character 
                for character in self.characters
            }

            for future in concurrent.futures.as_completed(future_to_character):
                character = future_to_character[future]

                try:
                    updated_prompt = future.result()
                    results[character.name] = updated_prompt
                except Exception as e:
                    self.logger.error(f"{character.name} 캐릭터 처리 중 오류 발생: {e}")
                    results[character.name] = "오류"

        return results

    def compare_and_upgrade(self, results: Dict[str, str], original_prompt: str) -> Tuple[str, List[str]]:
        user_content =  f"Original Prompt: {original_prompt}\n\nImproved Prompt: {results}"
        messages = [
            {"role": "system", "content": f'Purpose of the expected user prompt: {self.original_purpose}' + SYSTEM_MAGI_PROMPT},
            {"role": "user", "content": user_content}
        ]
        out = self.create_completion(messages)
        self.logger.info(Fore.GREEN + "평가 및 업그레이드 결과: " + out)
        result = json.loads(out)

        return result['updated_prompt'], result['key_improvements']
        

    def recursive_prompt_upgrade(self, remain_rounds: int, initial_prompt: str, user_prompt: Optional[str] = None) -> str:
        if not self.original_language:
            initial_language, initial_purpose = self.analyze_initial_prompt(initial_prompt)
            self.original_language = initial_language
            self.original_purpose = initial_purpose
            initial_prompt = self.translate_to_english(initial_prompt)

        if remain_rounds <= 0:
            self.logger.info("Upgrade process completed.")
            if self.original_language != 'English':
                result =  self.translate_to_original_language(initial_prompt)
            else:
                result = initial_prompt
            
            self.logger.info(Fore.YELLOW + "Final Prompt: "+f"{result}")
            return result



        self.logger.info(Fore.GREEN + f"------------------------Round { remain_rounds } Start------------------------")
        messages = [{"role": "user", "content": initial_prompt}] if user_prompt is None else [
            {"role": "system", "content": initial_prompt},
            {"role": "user", "content": user_prompt}
        ]

        out = self.create_completion(messages)
        self.logger.info(Fore.YELLOW + "Messages: " + Fore.RESET + f"{messages}")
        self.logger.info(Fore.YELLOW + "Output: " + Fore.RESET + f"{out}")

        results = self.run_character_prompts(initial_prompt, out)
        updated_prompt, key_improvements = self.compare_and_upgrade(results, initial_prompt)
        
        self.logger.info(Fore.BLUE + "Updated Prompt: "+ Fore.RESET + f"{updated_prompt}")
        self.logger.info(Fore.BLUE + "Key Improvements: "+ Fore.RESET + f"{key_improvements}")

        return self.recursive_prompt_upgrade(remain_rounds - 1, updated_prompt, user_prompt)
