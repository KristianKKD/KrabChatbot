from dotenv import load_dotenv

from twitchio.ext import commands
import os

class KrabBot(commands.Bot):
    def __init__(self):
        super().__init__(
            token=os.environ["TWITCH_TOKEN"],
            client_id=os.environ["TWITCH_CLIENT_ID"],
            nick='KrabBot',
            prefix='!',
            initial_channels=['KrabGor']
        )

    async def event_message(self, message):
        print(message.author.name, message.content)

if __name__ == "__main__":
    load_dotenv("keys.env")  # Make sure to specify your env file if it's not .env
    if not os.environ.get("TWITCH_TOKEN") or not os.environ.get("TWITCH_CLIENT_ID"):
        raise ValueError("TWITCH_TOKEN and TWITCH_CLIENT_ID must be set in the environment variables.")
    
    print("Starting KrabBot...")
    
    bot = KrabBot()
    bot.run()