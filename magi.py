import json
from typing import Tuple, List, Dict, Optional
from colorama import Fore, Back, Style, init
import concurrent.futures
from characters import Character
from openai import OpenAI

from prompts import PERSONA_PROMPT, SYSTEM_MAGI_PROMPT
from utils import init_logger, save_result

class Magi(Character):
    def __init__(self, model_name: str):
        self.client = OpenAI()
        self.model_name = model_name
        self.logger = init_logger('Magi')
        self.original_language = None
        self.original_purpose = None
        self.max_rounds = None
        self.prompts = []

    def initialize(self, remain_rounds: int, initial_prompt: str):
        self.max_rounds = remain_rounds
        messages = [
            {"role": "system", "content": "You are an expert in analyzing the initial prompt. Extract the following two pieces of information: 1) The language of the prompt, 2) The user's intention and purpose. Present the result in JSON format like this: {'language': '...', 'intention_and_purpose': '...'}"},
            {"role": "user", "content": f"Analyze the following prompt: {initial_prompt}"}
        ]
        out = self.create_completion(messages)
        analysis = json.loads(out)

        self.original_language = analysis['language']
        self.original_purpose = analysis['intention_and_purpose']

        self.characters = [
            Character(name="🧙 Melchior", personas=PERSONA_PROMPT["🧙 Melchior"], model_name=self.model_name, magi=self),
            Character(name="🧑‍💻 Balthasar", personas=PERSONA_PROMPT["🧑‍💻 Balthasar"], model_name=self.model_name, magi=self),
            Character(name="👶 Caspar", personas=PERSONA_PROMPT["👶 Caspar"], model_name=self.model_name, magi=self),
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
            {"role": "system", "content": SYSTEM_MAGI_PROMPT + f'Expected purpose from user initial prompt is {self.original_purpose}. Check if the improved prompt meet the original purpose. Answer in {self.original_language}' },
            {"role": "user", "content": user_content}
        ]
        out = self.create_completion(messages)
        self.logger.info(Fore.GREEN + "Evaluation and Upgrade Result: " + out)
        result = json.loads(out)

        return result['updated_prompt'], result['key_improvements']
        

    def recursive_prompt_upgrade(self, remain_rounds: int, initial_prompt: str, user_prompt: Optional[str] = None) -> str:
        if self.max_rounds is None:
            self.initialize(remain_rounds, initial_prompt)
            self.prompts = [initial_prompt]  # 최초 프롬프트 저장
        
    

        self.logger.info(Fore.GREEN + f"------------------------Round { self.max_rounds - remain_rounds + 1 } {"(final)" if remain_rounds == 0 else f"({remain_rounds} rounds left)"} Start------------------------")
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
        
        self.prompts.append(updated_prompt) 

        if remain_rounds <= 0:
            self.logger.info("Upgrade process completed.")
            result = initial_prompt
            self.logger.info(Fore.YELLOW + "Final Prompt: "+f"{result}")
            save_result(self.prompts, f"{self.logger.handlers[0].stream.getvalue()}")
            return result

        return self.recursive_prompt_upgrade(remain_rounds - 1, updated_prompt, user_prompt)
