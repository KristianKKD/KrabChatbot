from dotenv import load_dotenv
from bot import KrabBot
from model_interaction import AIModel
import my_input
import asyncio
import os

async def main():
    print("Starting KrabBot...")

    bot = KrabBot()
    model = AIModel()

    await asyncio.gather(
        model.create_model(),
        bot.connect()
    )

    print ("Bot connected. Listening for messages...")
    while True:
        message = await bot.read_message()
        if message:
            usr, msg = message
            response = await model.GenerateResponse(f"{usr} says: {msg}")
            print(f"Bot response: {response}")

        await my_input.capture_input(model)

if __name__ == "__main__":
    load_dotenv("keys.env")
    if not os.environ["TWITCH_TOKEN"] or not os.environ["TWITCH_CLIENT_ID"]:
        raise ValueError("TWITCH_TOKEN and TWITCH_CLIENT_ID must be set in the environment variables.")
    
    asyncio.run(main())