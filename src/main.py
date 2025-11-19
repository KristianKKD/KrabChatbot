from dotenv import load_dotenv
from TwitchBot import KrabBot
import asyncio
import os
from TTSManager import TextToSpeech
from DiscordIntegration import DiscordBot
from OBSIntegration import OBSComms

#BUG:spam whilst the TTS is beign read out makes the files get replaced before the next tts is read out so it never gets read out, just reads the latest multiple times

async def main():
    print("Starting KrabBot...")
    
    bot = None
    bot = DiscordBot()
    asyncio.create_task(bot.start(os.getenv("DISCORD_BOT_TOKEN")))

    obs = None
    #obs = OBSComms()

    tts_enabled = True
    model_enabled = False
    twitch_input_enabled = False

    slurs = load_filtered_words()

    twitch_bot = KrabBot(   
                        tts_enabled=tts_enabled,
                        model_enabled=model_enabled, 
                        twitch_input_enabled=twitch_input_enabled, 
                        discord_bot=bot, 
                        obs_comms=obs,
                        filtered_words=slurs
                        )

    await twitch_bot.connect()

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

        async def manual_tts(content):
            tts = TextToSpeech(id=0)
            await tts.speak(text=content, user="UIGor", discord_bot=bot, obs_comms=obs)
            return True
        
        async def disconnect_discord(_):
            bot.disconnect()
            return True

        commands = {
            "exit": handle_exit,
            "enabletts": handle_enable_message_tts,
            "enablemodel": handle_enable_model,
            "enabletwitchinput": handle_enable_twitch_input,
            "tts": manual_tts,
            "stoptts": stop_tts,
            "disconnectdiscord": disconnect_discord
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

def load_filtered_words():
    slurs = []
    if os.path.exists("censoredwords"):
        with open("censoredwords", "r") as f:
            slurs = [line.strip().lower() for line in f if line.strip()]
    return slurs

###############################################
if __name__ == "__main__":
    load_dotenv("keys.env")
    if not os.environ["TWITCH_TOKEN"] or not os.environ["TWITCH_CLIENT_ID"]:
        raise ValueError("TWITCH_TOKEN and TWITCH_CLIENT_ID must be set in the environment variables.")
    
    asyncio.run(main())