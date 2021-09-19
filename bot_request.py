import json
from PIL import Image
import requests
from io import BytesIO
import discord
from discord.ext import commands
from better_profanity import profanity
import os


class BotRequest(commands.Cog):
    def __init__(self, client):
        self.client = client

    def get_request(self, url):
        # server url
        res = requests.get(url)
        res_content = res.json()
        print("GET_REQUEST", res_content)
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

            # req = self.get_request(f"http://127.0.0.1:5000/ocr?url={url}")
            # ocr_text = req["text"]
            # ocr_words = req["words"]
            # req2 = self.get_request(f"http://127.0.0.1:5000/analyze-text?text={ocr_text['description']}")

            # print(ocr_text, ocr_words)
            # print(req2)

            req = self.get_request(f"http://127.0.0.1:5000/ocr?url={url}")
            ocr_text = req["text"]
            ocr_words = req["words"]
            print(ocr_text, ocr_words)

            #Sentient analysis
            text_info = self.get_request(f"http://127.0.0.1:5000/analyze-text?text={ocr_text['description']}")

            ocrResults = []
            for ocr_word in ocr_words:
                if profanity.contains_profanity(ocr_word["description"]):
                    ocrResults.append(ocr_word)

            ### img analysis
            # get image data
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
            nsfwImagePath = "nsfw.png"
            # save nsfw image
            img.save(nsfwImagePath)
            sfwImagePath = "cross.png"

            if len(ocrResults) == 0:
                sfw_path = self.get_request(f"http://127.0.0.1:5000/pic-analysis?nsfw_path={nsfwImagePath}&sfw_path={sfwImagePath}")["path"]
            else:
                sfw_path = self.get_request(f"http://127.0.0.1:5000/pic-analysis/{ocrResults}?nsfw_path={nsfwImagePath}&sfw_path={sfwImagePath}")["path"]

            with open(sfw_path, "rb") as fh:
                f = discord.File(fh, filename=sfw_path)
            await ctx.send(file=f)
            # setup embed
            embed = discord.Embed(title='Photo Police', colour=0xf6dae4)
            embed.set_author(name=f'{ctx.author.display_name}')
            # positive
            if text_info['analysis']['scores']['pos'] >= 60:
                embed.add_field(name='Positivity',
                            value='✅',
                             inline=True)
            else:
                embed.add_field(name='Positivity',
                                value='❌', 
                                inline=True)
            # profanity
            if bool(text_info['analysis']['profanity']):
                embed.add_field(name='SFW?',
                                value='🤬', 
                                inline=True)
            else:
                embed.add_field(name='SFW?',
                                value='👌', 
                                inline=True)
            await ctx.send(embed=embed)

