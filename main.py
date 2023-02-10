import discord
import os
from dotenv import load_dotenv
load_dotenv()

# creation of discord client to access the bot through typing
client = discord.Client()


# client.events are for reading inputs from user in discord, and for bot to return a msg
@client.event
async def on_ready():
    print("bello".format(client))


@client.event
async def on_message(message):
    if message.content.startswith('!create_archived_pins'):
        await message.channel.send('Please choose a channel to archive the pins.')


# ALL COMMANDS UNDERNEATH, ABOVE IS HOW TO CALL THEM

# runs the client using secret token from our env file
client.run(os.getenv('BOT_TOKEN'))
