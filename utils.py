import logging
from colorama import Fore, Back, Style, init

def init_logger(name: str):
    init(autoreset=True)
    logging.basicConfig(
        level=logging.INFO,
        format=Fore.RED + '%(name)s' + Fore.RESET + ' - %(message)s',
    )
    logger = logging.getLogger(name) 
   
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

