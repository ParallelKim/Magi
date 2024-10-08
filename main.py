from magi import Magi

if __name__ == "__main__":
    magi = Magi(model_name="gpt-4o-mini")
    initial_prompt = "난너무기여워"
    user_prompt = None
    max_rounds = 5


    magi.recursive_prompt_upgrade(max_rounds, initial_prompt, user_prompt)