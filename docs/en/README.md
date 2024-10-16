# Magi

[한국어](README.md) | [English](docs/en/README.md)

Magi is a personal toy project experimenting with AI's ability to improve prompts autonomously.

## Overview

The Magi project uses Large Language Models (LLMs) to analyze LLM outputs and iteratively improve prompts based on the results. Through this process, it explores the possibilities and limitations of AI self-improvement.

## Core Architecture

Magi's architecture consists of three key elements:

1. Recursive Prompt Upgrade
2. Multi-perspective Analysis System
3. Meta-evaluation and Optimization

### Recursive Prompt Upgrade

This process involves repeatedly analyzing LLM outputs through the LLM itself and improving prompts based on the results.

### Multi-perspective Analysis System

The system analyzes prompts from various angles using multiple characters:

1. Melchior (Strategist): Evaluates and develops the overall effectiveness of the work.
2. Caspar (Innovator): Presents innovative and original ideas.
3. Balthasar (Analyst): Minimizes inefficient tasks based on data and logic.

### Meta-evaluation and Optimization

The Magi character acts as an administrator, determining the most critical responsibilities of the process:

1. Analyzing the user's initial prompt intent
2. Objectively evaluating each character's suggestions
3. Synthesizing various ideas
4. Maintaining the project's direction

## Installation

1. Clone the repository:
    ```
    git clone https://github.com/ParallelKim/Magi.git
    ```
2. Install dependencies:
    ```
    pip install -r requirements.txt
    ```
3. Set environment variable:
    ```
    export OPENAI_API_KEY=<your_openai_api_key>
    ```

## Usage Example

```python
from magi import Magi
magi = Magi(model_name="gpt-4-1106-preview")
initial_prompt = "Please explain AI self-improvement."
improved_prompt = magi.recursive_prompt_upgrade(5, initial_prompt)
print(improved_prompt)
```

## Current Challenges

1. Improving character personas
2. Enhancing improvement evaluation criteria
3. Increasing scalability
4. Integrating user feedback

## Contributing

If you'd like to contribute to the project, please follow these steps:

1. Fork this repository.
2. Create a new branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

## License

This project is distributed under the MIT License. See the `LICENSE` file for more details.

## Contact

Project Manager - parallelkim12@gmail.com

Project Link: [https://github.com/ParallelKim/Magi](https://github.com/ParallelKim/Magi)

## Additional Information

The full code and experimental results of the project can be found in the [GitHub repository](https://github.com/ParallelKim/Magi).
