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
        system_prompt = "Your task is to provide feedback on a user's prompt in a clear and friendly manner. Focus on making your suggestions easy for everyone to understand. For example, try breaking down long sentences into shorter ones and using simpler words. Present your feedback using this structure: {'goods': [...], 'bads': [...]}."
        user_prompt = (
            f"Prompt: {prompt}\n\n"
            f"Output: {output_text}\n\n"
        )

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": system_prompt},{"role": "user", "content": user_prompt}],
                response_format={"type": "json_object"}
            )

            analysis_output = response.choices[0].message.content
            json_output = json.loads(analysis_output)

            goods = json_output.get("goods", "")
            bads = json_output.get("bads", "")
            return goods, bads
        except json.JSONDecodeError as e:
            logging.error(f"JSON decoding failed: {e}")
            return "", ""
        except Exception as e:
            logging.error(f"Unexpected error during analysis: {e}")
            return "", ""

    def update_prompt(self, original_prompt: str, goods: str, bads: str) -> Tuple[str, str]:
        system_prompt = "Your job is to improve and simplify a user-provided prompt by focusing on its strengths and weaknesses. Analyze the feedback from the user to create a clearer, engaging, and easy-to-understand version. Avoid using complex technical jargon and aim to explain ideas in a straightforward way, especially for beginners. Provide specific examples of potential improvements, such as simplifying code snippets or giving clearer explanations. Present your revised prompt in a JSON format like this: {'updated_prompt': '...', 'key_improvements': ['...', '...', '...']}."
        user_prompt = (f"Original Prompt: {original_prompt}\n\n"
            f"Good Parts: {goods}\n\n"
            f"Bad Parts: {bads}\n\n")

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

    def recursive_prompt_upgrade(self,remain_rounds: int, initial_prompt: str, user_prompt: str | None) -> str:
        if remain_rounds <= 0:
            logging.info("Final prompt after upgrades:")
            logging.info(initial_prompt)
            return initial_prompt

        try:
            if(user_prompt is None):
                messages = [{"role": "user", "content": initial_prompt}]
            else: 
                messages = [{"role": "system", "content": initial_prompt},{"role": "user", "content": user_prompt}]
                
            response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=messages
                )

            output_text = response.choices[0].message.content

            goods, bads = self.analyze_output(initial_prompt, output_text)

            updated_prompt, key_improvements = self.update_prompt(initial_prompt, goods, bads)

            logging.info(f"------------------------Life: {remain_rounds}------------------------")
            logging.info(f"Initial Prompt: {initial_prompt}")
            logging.info(f"Output Text: {output_text}")
            logging.info(f"Good Parts: {goods}")
            logging.info(f"Bad Parts: {bads}")
            logging.info(f"Key Improvements: {key_improvements}")

            return self.recursive_prompt_upgrade(remain_rounds - 1, updated_prompt, user_prompt)
        except Exception as e:
            logging.error(f"Unexpected error in recursive upgrade: {e}")
            return initial_prompt

if __name__ == "__main__":
    prompt_enhancer = PromptImprovement(model_name="gpt-4o-mini")
    initial_prompt =  "Your job is to analyze the strengths and weaknesses of a user-provided prompt and its output. Focus on the prompt's clarity, engagement, and ease of understanding, avoiding complex technical jargon. Provide specific examples of potential improvements, such as simplifying code snippets or giving clearer explanations. Present your analysis in a JSON format and include a short list of key enhancements made. Please return the analysis in JSON format like this: {'goods':string, 'bads':string}"
    user_prompt = "Prompt: Your task is to enhance and simplify an original prompt based on the strengths and weaknesses provided by the user. Analyze these inputs to generate a clearer, engaging, and contextually appropriate version of the original prompt. Make sure to avoid complex jargon and explain concepts in a way that is easy to understand, especially for beginners. Include specific examples of how the prompt can be improved, such as simplifying certain code snippets or providing clearer explanations. Present your improved prompt in JSON format, along with a brief list of key improvements you made.\n\nOutput: ```json { \"improved_prompt\": \"당신은 Magi라고 불리는 AI로, 재귀적으로 사용자 코드 개선을 지원합니다. 사용자가 제공한 코드를 바탕으로, 개선할 부분을 제안하고 왜 그런지 설명해주세요. 각 제안에는 장점과 단점을 담아 명확히 전달하고, 사용자 코드에 적용할 수 있는 관련 코드 예시를 포함해주세요. 프로그래밍을 잘 모르는 사람도 이해할 수 있도록 제안의 개념을 쉽게 설명해주고, 여러 프로그래밍 언어에서 어떻게 적용할 수 있는지 알려주세요. 마지막으로, 개선 프로세스의 목표와 작동 방식을 간단히 설명하고, 성능 관련 제안이 있을 경우 사용자에게 미칠 수 있는 영향을 명확히 해주세요.\", \"key_improvements\": [ \"간단하고 명확한 언어로 프롬프트 리팩토링\", \"재귀적 개선 프로세스 설명을 추가하여 이해 용이성 증대\", \"각 제안에 대해 요약 및 결론을 추가하여 사용자에게 핵심 내용 정리 제공\", \"코드 예시를 통해 실제 적용을 강조하고, 복잡성 감소\" ] } ``` ### Explanation of Improvements: 1. **Simplified Language**: The revised prompt uses simple and clear language, ensuring that even beginners can easily understand it. 2. **Clarified Process Description**: The prompt now explicitly requests an explanation of the recursive prompt upgrade process, improving comprehension about the AI's functionality. 3. **Summary Request**: By asking for a summary or conclusion, the revisions help users grasp the core ideas from the suggestions provided. 4. **Focused Code Examples**: The instructions emphasize providing relevant code snippets, which helps users see practical applications of the improvements discussed. Overall, this version aligns closely with the strengths of the original but addresses its weaknesses by making it clearer and more engaging."
    max_rounds = 5
    
    prompt_enhancer.recursive_prompt_upgrade(max_rounds, initial_prompt, user_prompt)