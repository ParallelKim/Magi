import json
import logging
from typing import Tuple, List, Dict, Optional
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

logging.basicConfig(
    level=logging.INFO,
    format=Fore.RED + '%(name)s' + Fore.RESET + ' - %(message)s',
)

logger = logging.getLogger("Magi")  # Use a custom logger

# Set the logging level for httpx to WARNING to suppress its logs
httpx_logger = logging.getLogger("httpx")
httpx_logger.setLevel(logging.WARNING)

from openai import OpenAI

# Define system prompts as constants
SYSTEM_ANALYSIS_PROMPT = (
    "Your task is to provide feedback on a user's prompt for LLM. "
    "The user will present the prompts entered into LLM and their output. "
    "Analyze the good and bad aspects of the prompt, specifying any vagueness or lack of clarity within it. "
    "Provide examples of how the prompt could be made clearer or more detailed. "
    "Present your feedback using JSON format like this: {'goods': [...], 'bads': [...], 'examples_of_improvements': [...]}"
)

SYSTEM_UPDATE_PROMPT = (
    "Your job is to improve a prompt for LLM by based on its good and bad. "
    "Use the feedback from the user to create a clearer, engaging, and easy-to-understand version of prompt. "
    "The user will enter the updated prompt into LLM."
    "Provide specific examples of potential improvements. Present your "
    "revised prompt in JSON format like this: {'updated_prompt': '...', key_improvements': ['...']}."
)


def read_file(file_path: str) -> str:
    """Read content from a file and return it as a string.

    Args:
        file_path (str): The path to the file to be read.

    Returns:
        str: The content of the file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
    except Exception as e:
        logger.error(f"Unexpected error reading file: {e}")
    return ""


class Magi:
    def __init__(self, model_name: str):
        """Initialize the Magi class with the OpenAI model.

        Args:
            model_name (str): The OpenAI model name to be used.
        """
        self.client = OpenAI()  # OpenAI API 클라이언트 초기화
        self.model_name = model_name  # 모델 이름 설정

    def create_completion(self, messages: List[Dict[str, str]]) -> str:
        """Create a chat completion with OpenAI API.

        Args:
            messages (List[Dict[str, str]]): The messages to send to the API.

        Returns:
            str: The text response from the API.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                response_format={"type": "json_object" if "json" in messages[0]["content"].lower() else "text"}
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error during OpenAI API call: {e}")
            return ""

    def analyze_prompt(self, prompt: str, output: str) -> Tuple[List[str], List[str]]:
        """Analyze the output of the LLM to evaluate strengths and weaknesses.

        Args:
            prompt (str): The original user prompt.
            output (str): The output received from the LLM.

        Returns:
            Tuple[List[str], List[str]]: A tuple containing lists of good and bad aspects of the prompt.
        """
        user_content = f"Prompt: {prompt}\n\nOutput: {output}\n\n"
        messages = [
            {"role": "system", "content": SYSTEM_ANALYSIS_PROMPT},
            {"role": "user", "content": user_content},
        ]

        analysis = self.create_completion(messages)

        if not analysis:
            logger.warning("No analysis returned from the LLM.")
            return [], []

        try:
            analysis = json.loads(analysis)
            goods = analysis.get("goods", [])
            bads = analysis.get("bads", [])
            
            return goods, bads
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error in analysis response: {e}, response: {analysis}")
            return [], []
        except KeyError as e:
            logger.error(f"Key error in analysis response: {e}")
            return [], []

    def update_prompt(self, original: str, goods: List[str], bads: List[str]) -> Tuple[str, List[str]]:
        """Update the prompt based on the analysis provided.

        Args:
            original (str): The original prompt.
            goods (List[str]): List of good aspects of the prompt.
            bads (List[str]): List of bad aspects of the prompt.

        Returns:
            Tuple[str, List[str]]: The updated prompt and key improvements suggested.
        """
        user_content = f"Original Prompt: {original}\n\nGood Parts: {goods}\n\nBad Parts: {bads}\n\n"
        messages = [
            {"role": "system", "content": SYSTEM_UPDATE_PROMPT},
            {"role": "user", "content": user_content},
        ]

        updated = self.create_completion(messages)

        if not updated:
            logger.warning("No updated prompt returned from the LLM.")
            return "", []

        try:
            updated = json.loads(updated)
            updated_prompt = updated.get("updated_prompt", "")
            key_improvements = updated.get("key_improvements", [])

            return updated_prompt, key_improvements
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error while updating: {e}")
            return "", []
        except KeyError as e:
            logger.error(f"Key error in update response: {e}")
            return "", []

    def validate_prompt(self, prompt: str) -> bool:
        """Validate the user prompt to ensure it is not empty or too long.

        Args:
            prompt (str): The user prompt to validate.

        Returns:
            bool: True if valid, False otherwise.
        """
        if not prompt:
            logger.error("Prompt must not be empty.")
            return False
        if len(prompt) > 500:  # 예시: 최대 길이 500자
            logger.error("Prompt exceeds maximum length of 500 characters.")
            return False
        return True

    def recursive_prompt_upgrade(self, remain_rounds: int, initial_prompt: str, user_prompt: Optional[str] = None) -> str:
        """Recursively upgrade prompts based on analysis."""
        if remain_rounds <= 0:
            logger.info(Fore.GREEN + "Upgrade process completed for all rounds.")
            return initial_prompt

        if not self.validate_prompt(initial_prompt):
            logger.error(Fore.RED + "Invalid initial prompt. Aborting upgrade process.")
            return initial_prompt

        logger.info(Fore.GREEN + f"------------------------Round {max_rounds - remain_rounds + 1} Start------------------------")
        messages = [ {"role": "user", "content": initial_prompt} ] if user_prompt is None else [
            {"role": "system", "content": initial_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        out = self.create_completion(messages)

        if not out:
            logger.warning(Fore.YELLOW + "No output received from the LLM. Continuing with the original prompt.")
            return initial_prompt

        goods, bads = self.analyze_prompt(initial_prompt, out)
        updated_prompt, key_improvements = self.update_prompt(initial_prompt, goods, bads)

        # Log details with colors
        logger.info(Fore.BLUE + f"Initial Prompt:" + Fore.RESET + f" {initial_prompt}")
        logger.info(Fore.BLUE + f"Output Text:" + Fore.RESET + f" {out}")
        logger.info(Fore.BLUE + f"Goods:" + Fore.RESET + f" {goods}")
        logger.info(Fore.BLUE + f"Bads:" + Fore.RESET + f" {bads}")
        logger.info(Fore.BLUE + f"Updated Prompt:" + Fore.YELLOW + f" {updated_prompt}")
        logger.info(Fore.BLUE + f"Key Improvements:" + Fore.RESET + f" {key_improvements}")

        return self.recursive_prompt_upgrade(remain_rounds - 1, updated_prompt, user_prompt)




if __name__ == "__main__":
    prompt_enhancer = Magi(model_name="gpt-4o-mini")
    initial_prompt = "부자되고싶어"
    user_prompt = None
    max_rounds = 1

    prompt_enhancer.recursive_prompt_upgrade(max_rounds, initial_prompt, user_prompt)