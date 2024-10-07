from magi import Magi

if __name__ == "__main__":
    magi = Magi(model_name="gpt-4o-mini")
    initial_prompt = "사용자 개입 없이 재귀적으로 프롬프트를 업그레이드하는 AI 프로젝트를 만들고 싶다"
    user_prompt = None
    max_rounds = 5


    magi.recursive_prompt_upgrade(max_rounds, initial_prompt, user_prompt)