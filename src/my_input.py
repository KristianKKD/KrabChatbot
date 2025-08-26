import asyncio
from model_interaction import AIModel

async def capture_input(model):

    model_input_keyword = "input:"

    while True:
        user_input = await asyncio.to_thread(input, "Enter input:")

        if user_input == "exit":
            break
        elif user_input == "resetai":
            model.disable_model()
            model.load_model()
        elif user_input == "enableai":
            model.enable_model()
        elif len(user_input) > len(model_input_keyword) and user_input[0:len(model_input_keyword)] == model_input_keyword:
            response = await model.generate_response(user_input[len(model_input_keyword):])
            print(f"AI response: {response}")
        else:
            print("Invalid input.")
