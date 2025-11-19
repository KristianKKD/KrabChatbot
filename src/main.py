from dotenv import load_dotenv
from ElevenLabsTTS import ElevenLabsTTS
from SpeechToText import SpeechToText
from TwitchBot import KrabBot
import asyncio
import os
from SystemTTS import SystemTTS
from DiscordIntegration import DiscordBot
from OBSIntegration import OBSComms
from SystemTTS import SystemTTS

#BUG:spam whilst the TTS is beign read out makes the files get replaced before the next tts is read out so it never gets read out, just reads the latest multiple times

#TODO: [voice] hello i am reall cool
#TODO: look into adding timings

async def main():
    print("Starting KrabBot...")

#####    
    twitch_input_enabled = False

    bot = None #discord bot
    obs = None #obs integration
    tts = None #text to speech
    stt = None #speech to text

    #stt = SpeechToText(api_key=os.environ["ELEVEN_LABS_KEY"], model_id="")
    if stt is not None:
        stt.start()

    #tts = SystemTTS()
    tts = ElevenLabsTTS(api_key=os.environ["ELEVEN_LABS_KEY"], voice="xJ6quMToF3QzDncP3TLF", model_id="")

    bot = DiscordBot()
    if bot is not None:
        asyncio.create_task(bot.start(os.getenv("DISCORD_BOT_TOKEN")))

    #obs = OBSComms()

    twitch_bot = KrabBot(   
                        tts_engine=tts,
                        twitch_input_enabled=twitch_input_enabled, 
                        discord_bot=bot, 
                        obs_comms=obs,
                        filtered_words=load_filtered_words()
                        )
    await twitch_bot.connect()

    print ("Bot connected. Listening for messages...")
######

    while True:
        async def handle_exit(_):
            return False

        async def stop_tts(_):
            await twitch_bot.stop_tts()
            return True

        async def manual_tts(content):
            await twitch_bot.speak(text=content, user="UIGor")
            return True
        
        commands = {
            "exit": handle_exit,
            "tts": manual_tts,
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