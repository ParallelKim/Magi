import logging
from colorama import Fore, Back, Style, init
from io import StringIO
import os
from datetime import datetime
import re

class TeeStringIO(StringIO):
    def __init__(self, initial_value='', newline='\n'):
        super(TeeStringIO, self).__init__(initial_value, newline)
        self.console = StringIO(initial_value, newline)

    def write(self, s):
        super(TeeStringIO, self).write(s)
        self.console.write(s)
        print(s, end='')  # 실시간 출력

def init_logger(name: str):
    init(autoreset=True)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    if not os.path.exists('private'):
        os.makedirs('private')
    
    stream = TeeStringIO()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(logging.Formatter(Fore.RED + '%(name)s' + Fore.RESET + ' - %(message)s'))
    logger.addHandler(handler)
    
    return logger

httpx_logger = logging.getLogger("httpx")
httpx_logger.setLevel(logging.WARNING)

def read_file(file_path: str) -> str:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
    except Exception as e:
        logger.error(f"Unexpected error reading file: {e}")
    return ""


def strip_ansi_codes(text):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def save_result(prompts, logs):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'private/result_{prompts[0]}_{timestamp}.txt'
    
    with open(filename, 'w', encoding='utf-8') as f:
        for i, prompt in enumerate(prompts):
            f.write(f"{i}. {prompt}\n\n")
        f.write("--- full logs ---\n\n")
        f.write(strip_ansi_codes(logs))
    
    print(f"결과가 {filename}에 저장되었습니다.")
