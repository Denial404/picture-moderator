import json
import requests

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
