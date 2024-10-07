#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "ParallelKim"
__version__ = "0.1.0"
__license__ = "MIT"

from openai import OpenAI
import json


client = OpenAI()

def analyze_output(prompt, output_text):
    analysis_prompt = (
        f"I will present the prompts presented to LLM and their outputs. First, analyze the prompt and the output content. Next, evaluate the prompt based on the analysis. Finally, present your strengths and weaknesses to complement the prompt:\n\n"
        f"Prompt: {prompt}\n\n"
        f"Output: {output_text}\n\n"
        "Please return the analysis in JSON format.{'good_parts':string, 'bad_parts':string}"
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": analysis_prompt}],
        response_format={"type": "json_object"}
    )

    analysis_output = response.choices[0].message.content

    json_output = json.loads(analysis_output)

    good_parts = json_output.get("good_parts", "")
    bad_parts = json_output.get("bad_parts", "")


    return good_parts, bad_parts

def update_prompt(original_prompt, good_parts, bad_parts):
    update_prompt_text = (
        f"Based on the analysis, here's an improved prompt:\n\n"
        f"Original Prompt: \"{original_prompt}\"\n\n"
        f"Good Parts: {good_parts}\n\n"
        f"Bad Parts: {bad_parts}\n\n"
        "Please suggest an improved version of the prompt in JSON format.{'updated_prompt':string, 'key_improvements':string}"
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": update_prompt_text}],    
        response_format={"type": "json_object"})

    updated_prompt = response.choices[0].message.content
    json_output = json.loads(updated_prompt)
    updated_prompt = json_output.get("updated_prompt", "")
    key_improvements = json_output.get("key_improvements", "")

    return updated_prompt, key_improvements

def recursive_prompt_upgrade(initial_prompt, remain_rounds):
    if remain_rounds <= 0:
        print("Final prompt after upgrades:")
        print(initial_prompt)
        return initial_prompt

    response = client.chat.completions.create(model="gpt-4o-mini",
    messages=[{"role": "user", "content": initial_prompt}])

    output_text = response.choices[0].message.content

    good_parts, bad_parts = analyze_output(initial_prompt, output_text)

    updated_prompt, key_improvements = update_prompt(initial_prompt, good_parts, bad_parts)

    print(f"------------------------Life: {remain_rounds}------------------------")
    print(f"Initial Prompt: {initial_prompt}")
    print(f"Output Text: {output_text}")
    print(f"Good Parts: {good_parts}")
    print(f"Bad Parts: {bad_parts}")
    print(f"Key Improvements: {key_improvements}")

    return recursive_prompt_upgrade(updated_prompt, remain_rounds - 1)

if __name__ == "__main__":
    initial_prompt = "재귀적인 메타 프로세스를 이용해 스스로 발전하고 업데이트하는 AI 서비스명을 추천해줘. 간결하고 인상적인 발음이어야 한다."
    max_rounds = 5
    recursive_prompt_upgrade(initial_prompt, max_rounds)

