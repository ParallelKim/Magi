from magi import Magi

if __name__ == "__main__":
    magi = Magi(model_name="gpt-4o-mini")
    initial_prompt = "재귀적 메타 프로세스를 통해 프롬프트를 개선하는 프로젝트, Magi에 대해 설명하는 짧은 Github README.md를 만들고 싶다"
    user_prompt = None
    max_rounds = 5


    magi.recursive_prompt_upgrade(max_rounds, initial_prompt, user_prompt)