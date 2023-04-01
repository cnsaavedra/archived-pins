import discord
import os
from dotenv import load_dotenv
load_dotenv()

# creation of discord client to access the bot through typing
intents = discord.Intents.all()
client = discord.Client(intents=intents)


# client.events are for reading inputs from user in discord, and for bot to return a msg
@client.event
async def on_ready():
    print("BELLO! I'm ready to archive your pins (Hosted from a local computer).".format(client))


@client.event
async def on_message(message):
    if message.content.startswith('!create_archived_pins'):
        # # Check if the author has the necessary permissions to perform the action
        # if not message.author.permissions_in(message.channel).manage_channels:
        #     await message.channel.send('You do not have the necessary permissions to perform this action.')
        #     return

        # Ask the user to select/type an existing channel name
        await message.channel.send('Please type the name of the channel you want to archive pins from:')
        response = await client.wait_for('message', check=lambda msg: msg.author == message.author)
        channel_name = response.content

        # Check if the selected channel exists
        channel = discord.utils.get(message.guild.channels, name=channel_name)
        if not channel:
            await message.channel.send(f'The channel "{channel_name}" does not exist on this server.')
            return

        # Create the new archived_pins channel
        archived_pins_channel_name = f'archived-pins-{channel_name}'
        i = 1
        while True:
            archived_pins_channel = discord.utils.get(
                message.guild.channels, name=archived_pins_channel_name)
            if not archived_pins_channel:
                break
            archived_pins_channel_name = f'archived-pins-{channel_name} ({i})'
            i += 1
        archived_pins_channel = await message.guild.create_text_channel(archived_pins_channel_name)

        # Copy the existing pins from the selected channel to the new archived_pins channel
        pins = await channel.pins()
        for pin in pins:
            if pin.content or pin.attachments:
                if pin.attachments:
                    for attachment in pin.attachments:
                        await archived_pins_channel.send(pin.content + '\n' + attachment.url)
                if pin.content:
                    await archived_pins_channel.send(pin.content)

        await message.channel.send(f'The pins from "{channel_name}" have been archived to "{archived_pins_channel_name}".')


# runs the client using secret token from our env file
client.run(os.getenv('BOT_TOKEN'))
