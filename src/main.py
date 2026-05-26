from dotenv import load_dotenv
import asyncio
import os

from Twitch_BotGor import KrabBot

from Integration_Discord import DiscordBot
from Integration_OBS import OBSComms

from TTS_Base import TextToSpeechBase
from TTS_System import SystemTTS
from TTS_ElevenLabs import ElevenLabsTTS

from SpeechToText import SpeechToText

#BUG:spam whilst the TTS is being read out makes the files get replaced before the next tts is read out so it never gets read out, just reads the latest multiple times

#TODO: [voice] hello i am really cool (add voice selection to TTS)
#TODO: look into adding timings for tts (e.g. slooooow fast)

async def launch_botgor():
    print("Starting KrabBot...")

    twitch_input_enabled:bool = False

    # Declaration
    bot:DiscordBot = None
    obs:OBSComms = None 
    tts:TextToSpeechBase = None
    stt:SpeechToText = None

    # Initialization
    #bot = DiscordBot()
    #obs = OBSComms()
    #tts = SystemTTS()
    #tts = ElevenLabsTTS(api_key=os.environ["ELEVEN_LABS_KEY"], voice="xJ6quMToF3QzDncP3TLF", model_id="")
    #stt = SpeechToText(api_key=os.environ["ELEVEN_LABS_KEY"], model_id="")

    # Launch
    if bot is not None: asyncio.create_task(bot.start(os.getenv("DISCORD_BOT_TOKEN")))
    if stt is not None: stt.start()

    twitch_bot:KrabBot = KrabBot(   
                        tts_engine=tts,
                        twitch_input_enabled=twitch_input_enabled, 
                        discord_bot=bot, 
                        obs_comms=obs,
                        filtered_words=load_filtered_words()
                        )
    await twitch_bot.connect()

    await handle_input(twitch_bot=twitch_bot)
    return

async def handle_input(twitch_bot:KrabBot):
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

        while True:
            user_input:str = str(await asyncio.to_thread(input, "Enter input:\n")).strip()
            cmd:str = user_input.lower().strip()
            arg:str = ""

            if ':' in user_input:
                cmd, arg = user_input.split(':', 1)

            if cmd in commands:
                if len(arg) > 0:
                    should_continue = await commands[cmd](arg)
                else:
                    should_continue = await commands[cmd]()

                if should_continue is False:
                    break
                continue

            print("Invalid input:" + user_input)

def load_filtered_words():
    slurs:list[str] = []
    if os.path.exists("censoredwords"):
        with open("censoredwords", "r") as f:
            slurs = [line.strip().lower() for line in f if line.strip()]
    return slurs

###############################################
if __name__ == "__main__":
    load_dotenv("keys.env")
    if not os.environ["TWITCH_TOKEN"] or not os.environ["TWITCH_CLIENT_ID"]:
        raise ValueError("TWITCH_TOKEN and TWITCH_CLIENT_ID must be set in the environment variables.")
    
    asyncio.run(launch_botgor())