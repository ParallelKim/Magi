#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "ParallelKim"
__version__ = "0.2.0"
__license__ = "MIT"

from openai import OpenAI
import json
import logging
from typing import Tuple

logging.basicConfig(level=logging.INFO)

class PromptImprovement:
    def __init__(self, model_name: str):
        self.client = OpenAI(model=model_name)

    def read_py_file(self, file_path: str) -> str:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            return content
        except FileNotFoundError as e:
            logging.error(f"File not found: {e}")
            return ""
        except Exception as e:
            logging.error(f"Unexpected error reading file: {e}")
            return ""

    def analyze_output(self, prompt: str, output_text: str) -> Tuple[str, str]:
        analysis_prompt = (
            f"I will present the prompts presented to LLM and their outputs. First, analyze the prompt and the output content. Next, evaluate the prompt based on the analysis. Finally, present your strengths and weaknesses to complement the prompt:\n\n"
            f"Prompt: {prompt}\n\n"
            f"Output: {output_text}\n\n"
            "Please return the analysis in JSON format.{'good_parts':string, 'bad_parts':string}"
        )

        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": analysis_prompt}],
                response_format={"type": "json_object"}
            )

            analysis_output = response.choices[0].message.content
            json_output = json.loads(analysis_output)

            good_parts = json_output.get("good_parts", "")
            bad_parts = json_output.get("bad_parts", "")
            return good_parts, bad_parts
        except json.JSONDecodeError as e:
            logging.error(f"JSON decoding failed: {e}")
            return "", ""
        except Exception as e:
            logging.error(f"Unexpected error during analysis: {e}")
            return "", ""

    def update_prompt(self, original_prompt: str, good_parts: str, bad_parts: str) -> Tuple[str, str]:
        update_prompt_text = (
            f"Based on the analysis, here's an improved prompt:\n\n"
            f"Original Prompt: \"{original_prompt}\"\n\n"
            f"Good Parts: {good_parts}\n\n"
            f"Bad Parts: {bad_parts}\n\n"
            "Please suggest an improved version of the prompt in JSON format.{'updated_prompt':string, 'key_improvements':string}"
        )

        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": update_prompt_text}],    
                response_format={"type": "json_object"})

            updated_prompt = response.choices[0].message.content
            json_output = json.loads(updated_prompt)
            updated_prompt = json_output.get("updated_prompt", "")
            key_improvements = json_output.get("key_improvements", "")
            return updated_prompt, key_improvements
        except json.JSONDecodeError as e:
            logging.error(f"JSON decoding failed: {e}")
            return "", ""
        except Exception as e:
            logging.error(f"Unexpected error during prompt update: {e}")
            return "", ""

    def recursive_prompt_upgrade(self, initial_prompt: str, remain_rounds: int) -> str:
        if remain_rounds <= 0:
            logging.info("Final prompt after upgrades:")
            logging.info(initial_prompt)
            return initial_prompt

        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": initial_prompt}]
            )

            output_text = response.choices[0].message.content

            good_parts, bad_parts = self.analyze_output(initial_prompt, output_text)

            updated_prompt, key_improvements = self.update_prompt(initial_prompt, good_parts, bad_parts)

            logging.info(f"------------------------Life: {remain_rounds}------------------------")
            logging.info(f"Initial Prompt: {initial_prompt}")
            logging.info(f"Output Text: {output_text}")
            logging.info(f"Good Parts: {good_parts}")
            logging.info(f"Bad Parts: {bad_parts}")
            logging.info(f"Key Improvements: {key_improvements}")

            return self.recursive_prompt_upgrade(updated_prompt, remain_rounds - 1)
        except Exception as e:
            logging.error(f"Unexpected error in recursive upgrade: {e}")
            return initial_prompt

if __name__ == "__main__":
    prompt_enhancer = PromptImprovement(model_name="gpt-4o-mini")
    initial_prompt = "너는 Magi라는 재귀적 프롬프트 개선 AI다. 사용자는 재귀적인 메타 프로세스를 이용해 프롬프트를 개선하고 업데이트하는 프로젝트, Magi의 프로토타입 코드를 작성했다. 너는 이를 참고하여 스스로 개선안을 제안해야 한다. 전체 코드는 사용자가 제공할 것이다. 이것은 너의 시스템 프롬프트다."
    user_prompt = prompt_enhancer.read_py_file("main.py")
    
    max_rounds = 5
    prompt_enhancer.recursive_prompt_upgrade(initial_prompt, max_rounds)