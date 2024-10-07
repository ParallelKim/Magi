from magi import Magi

if __name__ == "__main__":
    magi = Magi(model_name="gpt-4o-mini")
    initial_prompt = "프론트엔드 개발자 이력서를 만들어줘"
    user_prompt = None
    max_rounds = 5


    magi.recursive_prompt_upgrade(max_rounds, initial_prompt, user_prompt)