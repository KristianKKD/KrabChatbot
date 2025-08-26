from twitchio.ext import commands
import os

class KrabBot(commands.Bot):
    messages = []
    message_head = -1
    message_tail = -1

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
        self.messages.append({message.author.name, message.content})
        self.message_head += 1
        
    async def read_message(self):
        if self.message_head > self.message_tail:
            user, msg = self.messages[self.message_head]
            self.message_tail += 1
            print(user, msg)
            return user, msg
        else:
            return None
