import json
from PIL import Image
import requests
from io import BytesIO

import discord
from discord.ext import commands


class BotRequest(commands.Cog):
    def __init__(self, client):
        self.client = client

    def get_request(self):
        # server url
        url = 'https://endless-orb-325023.ue.r.appspot.com/nude-net'
        res = requests.get(url)
        res_content = json.loads(res.content)
        return res_content

    @commands.command(name='info', aliases=['pp', 'pipo'])
    async def info(self, ctx):
        async with ctx.typing():
            a = self.get_request()
        await ctx.send(a)

    @commands.command(name='ppp')
    async def ppp(self, ctx):
        async with ctx.typing():
            url = ctx.message.attachments[0].url
            print(url)
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
            img.save('picture.png')
        await ctx.send(url)
