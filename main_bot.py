import os
import discord
from discord.ext import commands
from bot_request import BotRequest
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()

client = commands.Bot(command_prefix='pp ', case_insensitive=True, help_command=None)
client.add_cog(BotRequest(client))

@client.event
async def on_ready():
    await client.change_presence(
        activity=discord.Activity(type=discord.ActivityType.listening, name='protecting the people'))
    print('Logged on as {0}!'.format(client.user))



def imageChecker(url):                
    suffix = url.split(".")[-1]
    if suffix == "jpg" or suffix =="jpeg" or suffix == "png":
        return True
    else:
        return False


@client.event
async def on_message(message):
    content = message.content
    # log bot output
    if message.author == client.user:
        print(message.content)
        return
    
    ctx = await client.get_context(message)

    if len(message.attachments) > 0: 
        for i, v in enumerate(message.attachments):
            # get suffix 
            url = v.url
            isImage = imageChecker(url)
            if isImage:
                # do nude net stuff
                br = client.get_cog('BotRequest')
                await br.image_analyze(ctx, url)
    
    if imageChecker(message.content):
        br = client.get_cog('BotRequest')
        await br.image_analyze(ctx, message.content)

    # 
    # await message.channel.send("don't send bad stuff ;) ;)")
    # resume bot (DO NOT DELETE)
    await client.process_commands(message)


@client.command(name='test')
async def test(ctx):
    await ctx.send('test')

def bot_start():
    print("hi", os.getenv('BOT_TOKEN'))
    client.run(os.getenv('BOT_TOKEN'))
    # client.run(os.environ('BOT_TOKEN'))

# run
if __name__ == "__main__":
    # pycharm getenv
    bot_start()

    # vscode get.environ 
    # print("hi", os.environ('BOT_TOKEN'))
