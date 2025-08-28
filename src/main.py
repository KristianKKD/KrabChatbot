from dotenv import load_dotenv
from bot import KrabBot
from model import AIModel
import my_input
import asyncio
import os
from tts import TextToSpeech

async def main():
    print("Starting KrabBot...")

    bot = KrabBot()
    model = AIModel()
    tts = TextToSpeech()

    await asyncio.gather(
        model.create_model(),
        bot.connect()
    )

    print ("Bot connected. Listening for messages...")
    while True:
        message = await bot.read_message()
        if message:
            await receive_message(bot, model, tts, message)

        await my_input.capture_input(model, bot, tts)  # Pass dependencies


async def receive_message(bot, model, tts, message, raw = False):
    usr, msg = message
    response = await model.generate_response(msg, raw=raw)
    print(f"Bot response: {response}")
    if bot.ttsEnabled:
        tts.speak(response)


###############################################
if __name__ == "__main__":
    load_dotenv("keys.env")
    if not os.environ["TWITCH_TOKEN"] or not os.environ["TWITCH_CLIENT_ID"]:
        raise ValueError("TWITCH_TOKEN and TWITCH_CLIENT_ID must be set in the environment variables.")
    
    asyncio.run(main())

