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
        self.client = OpenAI()
        self.model_name = model_name

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
                model=self.model_name,
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
        system_prompt = "Your job is to improve and simplify a user-provided prompt by focusing on its strengths and weaknesses. Analyze the feedback from the user to create a clearer, engaging, and easy-to-understand version. Avoid using complex technical jargon and aim to explain ideas in a straightforward way, especially for beginners. Provide specific examples of potential improvements, such as simplifying code snippets or giving clearer explanations. Present your revised prompt in a JSON format and include a short list of key enhancements made."
        user_prompt = (f"Original Prompt: {original_prompt}\n\n"
            f"Good Parts: {good_parts}\n\n"
            f"Bad Parts: {bad_parts}\n\n")

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "system", "content": system_prompt},{"role": "user", "content": user_prompt}],    
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

    def recursive_prompt_upgrade(self,remain_rounds: int, initial_prompt: str, user_prompt: str | None = None) -> str:
        if remain_rounds <= 0:
            logging.info("Final prompt after upgrades:")
            logging.info(initial_prompt)
            return initial_prompt

        try:
            if(user_prompt is None):
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[{"role": "user", "content": initial_prompt}]
                )
            else: 
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[{"role": "system", "content": initial_prompt},{"role": "user", "content": user_prompt}]
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

            return self.recursive_prompt_upgrade(remain_rounds - 1, updated_prompt, user_prompt)
        except Exception as e:
            logging.error(f"Unexpected error in recursive upgrade: {e}")
            return initial_prompt

if __name__ == "__main__":
    prompt_enhancer = PromptImprovement(model_name="gpt-4o-mini")
    initial_prompt = "You are a prompt improver. The user will present the 'original prompt', 'the strength of the prompt', and 'the bad of the prompt'. Improve the prompt based on the results of this analysis. Please suggest an improved version of the prompt in JSON format: {'updated_prompt':string, 'key_improvements':string}"
    user_prompt = ("Original Prompt: 너는 Magi라는 재귀적 프롬프트 개선 AI다. 사용자가 제공하는 전체 코드를 바탕으로, Magi의 프롬프트 개선 및 업데이트 프로세스에 따라 개선안을 제안하라. 사용자의 코드 개선 방향을 명확히 전달하고, 구체적인 제안은 간결하게 제시하라. 각 제안에 대한 장단점을 논의하고, 사용자가 제공한 코드 샘플에 직접 적용할 수 있는 해당 언어의 관련 코드 예시를 포함하여 사용자가 개선 제안의 영향을 잘 이해할 수 있도록 하라. 친숙하지 않은 프로그래머를 위해 각 제안의 개념과 맥락을 제공하고, 다양한 프로그래밍 언어에서의 적용 가능성을 포함하도록 조정하라. 마지막으로, 재귀적 개선 프로세스의 목표와 작동 방식을 명확히 설명하고, 성능 관련 제안의 경우 사용자에게 가능한 영향을 구체적으로 설명하라.\n\nGood Parts: - The output provides detailed suggestions for code improvements, including specific explanations of each suggestion's merits and drawbacks.\n- Code examples are provided alongside each suggestion, which helps the user understand how to implement the advised changes directly.\n- The suggestions address common coding issues such as exception handling, return value consistency, logging, and documentation, which are crucial for better code quality and maintainability.\n- The output maintains clarity and sufficiency for a programmer who might not be familiar with the nuances of the code, making it suitable for various programming contexts.\n\nBad Parts: - The initial prompt could be overly complex, potentially leading to a misunderstanding of the main goals by the AI. Simplifying the prompt could yield more direct and focused outputs.- The analysis does not explicitly state how the recursive prompt upgrade process works, which is referenced in some suggestions. Clarifying this could enhance understanding.- While the output discusses the importance of the suggestions, it lacks a summary or conclusion that synthesizes the key takeaways from the proposed improvements, which could be helpful for the user.\n\n")
            
    max_rounds = 5
    prompt_enhancer.recursive_prompt_upgrade(max_rounds, initial_prompt, user_prompt)