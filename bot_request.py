import json
from PIL import Image
import requests
from io import BytesIO
from nudenet import NudeDetector
from nudenet import NudeClassifier
import server.censoring as cen
import discord
from discord.ext import commands


class BotRequest(commands.Cog):
    def __init__(self, client):
        self.client = client

    def get_request(self, url):
        # server url
        res = requests.get(url)
        res_content = json.loads(res.content)
        return res_content

    @commands.command(name='info', aliases=['pp', 'pipo'])
    async def info(self, ctx):
        async with ctx.typing():
            pic_info = self.get_request('https://endless-orb-325023.ue.r.appspot.com/nude-net')
        await ctx.send(pic_info)

    @commands.command(name='ppp')
    async def ppp(self, ctx):
        await ctx.channel.purge(limit=1)
        async with ctx.typing():
            url = ctx.message.attachments[0].url
            #print(url)
            # get image data
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
            imagePath = "nsfw.png"
            # save nsfw image
            img.save(imagePath)

            sfw_path = cen.censorImage(imagePath, "")
            with open(sfw_path, "rb") as fh:
                f = discord.File(fh, filename=sfw_path)
            await ctx.send(file=f)

