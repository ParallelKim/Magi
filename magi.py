import json
from typing import Tuple, List, Dict, Optional
from colorama import Fore, Back, Style, init
import concurrent.futures
from characters import Character
from openai import OpenAI

from prompts import SYSTEM_MAGI_PROMPT
from utils import init_logger

class Magi(Character):
    def __init__(self, model_name: str):
        self.client = OpenAI()
        self.model_name = model_name
        self.logger = init_logger('Magi')
        self.characters = [
            Character(name="👨 Melchior", personas="You are the symbol of the wise old man. You excel in strategic planning and long-term improvements, ensuring that each task is performed with wisdom and achieves the highest performance.", model_name=model_name),
            Character(name="🧑 Balthasar", personas="You are the symbol of a smart young man. You are good at performing tasks efficiently and economically, and producing clear and concise results. You are strong in data analysis and problem solving, and you systematically manage the progress of your project.", model_name=model_name),
            Character(name="👶 Caspar", personas="You are the symbol of a creative boy. You excel in generating innovative and out-of-the-box ideas, actively participating in brainstorming sessions and proposing experimental approaches to enhance the project's creativity.", model_name=model_name),
        ]

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
            {"role": "system", "content": SYSTEM_MAGI_PROMPT},
            {"role": "user", "content": user_content}
        ]
        out = self.create_completion(messages)
        self.logger.info(Fore.GREEN + "평가 및 업그레이드 결과: " + out)
        result = json.loads(out)

        return result['updated_prompt'], result['key_improvements']
        

    def recursive_prompt_upgrade(self, remain_rounds: int, initial_prompt: str, user_prompt: Optional[str] = None) -> str:
        if remain_rounds <= 0:
            self.logger.info("Upgrade process completed.")
            return initial_prompt
        
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
