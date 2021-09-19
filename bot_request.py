import json
from PIL import Image
import requests
from io import BytesIO
from nudenet import NudeDetector
from nudenet import NudeClassifier
import server.censoring as cen
import discord
from discord.ext import commands
import os


class BotRequest(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.detector = NudeDetector()  # detector = NudeDetector('base') for the "base" version of detector.

    def get_request(self, url):
        # server url
        res = requests.get(url)
        print(res)
        res_content = json.loads(res.content)
        return res_content

    @commands.command(name='info', aliases=['pp', 'pipo'])
    async def info(self, ctx):
        async with ctx.typing():
            pic_info = self.get_request('')
        await ctx.send(pic_info)

    @commands.command(name='ia', aliases=['ppp', 'analyze'])
    async def image_analyze(self, ctx, link=None):
        await ctx.channel.purge(limit=1)
        async with ctx.typing():
            url = link if link else ctx.message.attachments[0].url

            ### text analysis
            print(f"{os.getenv('SERVER_URL')}?url={url}")
            #ocr_text = self.get_request(f"{os.getenv('SERVER_URL')}?url={url}")
            #text_info = self.get_request(f"{os.getenv('SERVER_URL')}?text={ocr_text}")
            #print(text_info)
            #return
            ### img analysis
            # get image data
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
            nsfwImagePath = "nsfw.png"
            # save nsfw image
            img.save(nsfwImagePath)
            sfwImagePath = "cross.png"

            detectingObject = self.detector.detect(nsfwImagePath)
            sfw_path = cen.censorImage(detectingObject, nsfwImagePath, sfwImagePath)
            with open(sfw_path, "rb") as fh:
                f = discord.File(fh, filename=sfw_path)
            await ctx.send(file=f)

