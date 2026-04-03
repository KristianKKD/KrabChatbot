import copy
from twitchio.ext import commands
import os
import asyncio
from TwitchPlays import process_twitch_input, input
from Integration_OBS import OBSComms
from TTS_Base import TextToSpeechBase
from Integration_Discord import DiscordBot


class KrabBot(commands.Bot):
    twitch_input_enabled:bool = False

    tts_inprogress:list[TextToSpeechBase] = []

    tts_engine:TextToSpeechBase
    discord_bot:DiscordBot
    obs_comms:OBSComms

    filtered_words:list[str] = []

    def __init__(self,  tts_engine:TextToSpeechBase = None,
                        twitch_input_enabled:bool = False, 
                        discord_bot:DiscordBot = None, 
                        obs_comms:OBSComms = None,
                        filtered_words:list[str] = []
                ):
        super().__init__(
            token=os.environ["TWITCH_TOKEN"],
            client_id=os.environ["TWITCH_CLIENT_ID"],
            nick='KrabBot',
            prefix='!',
            initial_channels=['KrabGor']
        )
        
        self.tts_engine = tts_engine
        self.twitch_input_enabled = twitch_input_enabled
        self.discord_bot = discord_bot
        self.obs_comms = obs_comms
        self.filtered_words = filtered_words
        return

    async def connect(self):
        await super().connect()
        print ("Bot connected. Listening for messages...")
        return

    async def event_message(self, message):
        usr:str = message.author.name
        content:str = message.content

        if (self.has_slurs(content)):
            content = '!filtered'

        print("-------------incoming_message: User: " + usr + "Message: " + content)

        #TWITCH PLAYS
        if self.twitch_input_enabled: 
            await process_twitch_input(content) #True if accepted input
            return

        #check if tts command
        if len(content) <= 1 or content[0] != '!':
            return #ignore commands too small
        content = content[1:] #strip the first !

        asyncio.create_task(self.speak(content, user=usr))
        return

    async def stop_tts(self):
        print("Stopping all TTS messages")
        for tts in self.tts_inprogress:
            tts.stop_audio()
        if self.discord_bot is not None:
            self.discord_bot.stop_tts()
        self.tts_inprogress = []
        return

    async def speak(self, text = "", user = ""):
        tts:TextToSpeechBase = copy.copy(self.tts_engine)
        self.tts_inprogress.append(tts)

        #run in background so no blocking
        async def speak_and_cleanup():
            await tts.speak(text=text, user=user, discord_bot=self.discord_bot, obs_comms=self.obs_comms)
            if tts in self.tts_inprogress:
                self.tts_inprogress.remove(tts)

        asyncio.create_task(speak_and_cleanup())
        return

    def has_slurs(self, message:str) -> bool:
        return any(word in message.lower() for word in self.filtered_words)
        