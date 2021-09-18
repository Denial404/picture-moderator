import json
import requests

import discord
from discord.ext import commands


class Request(commands.Cog):
    def __init__(self, client):
        self.client = client

    def get_request(self):
        # server url
        url = ''
        res = requests.get(url)
        res_content = json.loads(res.content)
        return res_content['the field you want']

