from dotenv import load_dotenv
from TwitchBot import KrabBot
import asyncio
import os
from DiscordIntegration import create_discord_bot

async def main():
    print("Starting KrabBot...")
    twitch_bot = KrabBot(tts_enabled=True)
    await twitch_bot.connect()

    bot = create_discord_bot()
    discord_task = asyncio.create_task(bot.start(os.getenv("DISCORD_BOT_TOKEN")))

    print ("Bot connected. Listening for messages...")
    while True:
        async def handle_exit(_):
            return False

        async def handle_enable_model(content = "true"):
            await twitch_bot.enable_model((content.lower() == "true"))
            return True

        async def handle_enable_message_tts(content = "true"):
            await twitch_bot.enable_tts((content.lower() == "true"))
            return True

        async def handle_enable_twitch_input(content = "true"):
            await twitch_bot.enable_twitch_input((content.lower() == "true"))
            return True

        async def stop_tts(_):
            await twitch_bot.stop_tts()
            return True

        commands = {
            "exit": handle_exit,
            "enabletts": handle_enable_message_tts,
            "enablemodel": handle_enable_model,
            "enabletwitchinput": handle_enable_twitch_input,
            "stoptts": stop_tts,
        }

        model_input_keyword = "input:"
        while True:
            user_input = await asyncio.to_thread(input, "Enter input:\n")
            content = user_input.strip()

            #commands
            if ':' in content:
                cmd, arg = content.split(':', 1)
                cmd = cmd.strip().lower()
                arg = arg.strip()
            else:
                cmd = content.lower()
                arg = ""

            if cmd in commands:
                if len(arg) > 0:
                    should_continue = await commands[cmd](arg)
                else:
                    should_continue = await commands[cmd]()

                if should_continue is False:
                    break
                continue

            #manual model input
            if content.lower().startswith(model_input_keyword):
                message = content[len(model_input_keyword):].strip()
                await twitch_bot.handle_model_response('krabgor', message)
            else:
                print("Invalid input:" + user_input)


###############################################
if __name__ == "__main__":
    load_dotenv("keys.env")
    if not os.environ["TWITCH_TOKEN"] or not os.environ["TWITCH_CLIENT_ID"]:
        raise ValueError("TWITCH_TOKEN and TWITCH_CLIENT_ID must be set in the environment variables.")
    
    asyncio.run(main())

