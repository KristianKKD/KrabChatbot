import discord
from discord.ext import commands

VOICE_CHANNEL_ID = 1416079575628251167

def create_discord_bot():
    intents = discord.Intents.default()
    intents.voice_states = True
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        print(f'Bot connected as {bot.user}')
        guild = bot.guilds[0]
        channel = guild.get_channel(VOICE_CHANNEL_ID)
        if channel and isinstance(channel, discord.VoiceChannel):
            await channel.connect()
            print(f"Joined voice channel: {channel.name}")
        else:
            print("Voice channel not found or not a voice channel.")

    @bot.command()
    async def play(ctx, filename: str):
        """Play an audio file in the voice channel."""
        voice_client = ctx.voice_client or discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if not voice_client:
            await ctx.send("Bot is not connected to a voice channel.")
            return
        if not filename.endswith(".mp3"):
            await ctx.send("Only .mp3 files are supported.")
            return
        try:
            source = discord.FFmpegPCMAudio(filename)
            voice_client.stop()  # Stop any current audio
            voice_client.play(source)
            await ctx.send(f"Playing {filename}")
        except Exception as e:
            await ctx.send(f"Error playing file: {e}")

    return bot

