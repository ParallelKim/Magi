from magi import Magi

if __name__ == "__main__":
    magi = Magi(model_name="gpt-4o-mini")
    initial_prompt = "Magi에 대해 설명해줘"
    user_prompt = None
    max_rounds = 5

    magi.recursive_prompt_upgrade(max_rounds, initial_prompt, user_prompt)

