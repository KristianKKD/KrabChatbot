import discord
from discord.ext import commands
from discord.client import VoiceClient
import asyncio

#VOICE_CHANNEL_ID = 1416079575628251167 #DiscGor
VOICE_CHANNEL_ID = 471406637643464724 #kami weebs
#VOICE_CHANNEL_ID = 1201274493289648239 #kami chamber

class DiscordBot(commands.Bot): 
    play_queue = []
    playing = False

    def __init__(self):
        intents = discord.Intents.default()
        intents.voice_states = True
        super().__init__(
            command_prefix="!",
            intents=intents
        )

    async def on_ready(self):
        print("Bot connected as: " +  str(self.user))
        for guild in self.guilds:
            channel = guild.get_channel(VOICE_CHANNEL_ID)
            if channel:
                break
        
        if channel and isinstance(channel, discord.VoiceChannel):
            await channel.connect()
            print("Joined voice channel: " + str(channel.name))
        else:
            print("Voice channel not found or not a voice channel.")

    async def queue_play(self, file_path):
        def play_callback(err):
            if len(self.play_queue) > 0:
                self.play_queue.pop(0)

            if err:
                print("Failed callback, RIP")
                return

            if (len(self.play_queue) > 0):
                play()
            else:
                self.playing = False

        def play():
            self.playing = True

            voice_client : VoiceClient = self.voice_clients[0]
            try:
                source = discord.FFmpegPCMAudio(self.play_queue[0])
                voice_client.play(source=source, after=play_callback)
                #print("Playing " + file_path)
            except Exception as e:
                print("Error playing file: " + str(e))

        #play if nothing is going on, otherwise queue it
        if file_path is not None:
            self.play_queue.append(file_path)
        if not self.playing:
            play()

    async def disconnect(self):
        guild = self.guilds[0]
        channel = guild.get_channel(VOICE_CHANNEL_ID)
        if channel and isinstance(channel, discord.VoiceChannel):
            voice_client = guild.voice_client
            await voice_client.disconnect()