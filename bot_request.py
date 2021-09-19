import json
from PIL import Image
import requests
from io import BytesIO
import discord
from discord.ext import commands
from better_profanity import profanity
import os

from PIL import Image, ImageDraw
from nudenet import NudeDetector
# from nudenet import NudeClassifier

class NsfwArea:
    def __init__(self, bounds, label, score, censorImage = True):
        if censorImage:
            self.y_min = bounds[1]
            self.x_min = bounds[0]
            self.y_max = bounds[3]
            self.x_max = bounds[2]
        else:
            self.y_min = bounds[0][1]
            self.x_min = bounds[0][0]
            self.y_max = bounds[2][1]
            self.x_max = bounds[2][0]
        self.label = label
        self.score = score

def getNsfwAreas(results, censorImage):
    nsfwAreas = []
    if censorImage:
        for nsfwArea in results:
            nsfwAreas.append(NsfwArea(nsfwArea["box"],
                                      nsfwArea["label"],
                                      nsfwArea["score"],
                                      True))
    else:
        for word in results:
            nsfwAreas.append(NsfwArea(word["vertices"],
                                      word["description"],
                                      0,
                                      False))

    return nsfwAreas

def censorImage(results, nsfwImagePath, sfwImagePath = "", censorImage = True):
    nsfwAreas = getNsfwAreas(results, censorImage)

    with Image.open(nsfwImagePath) as img:
        draw = ImageDraw.Draw(img)
        for nsfwArea in nsfwAreas:
            if (sfwImagePath == ""):
                draw.rectangle([nsfwArea.x_min, nsfwArea.y_min, nsfwArea.x_max, nsfwArea.y_max], '#0f0f0f80', '#0f0f0f80', 2)
            else:
                sfwImage = Image.open(sfwImagePath)

                size = nsfwArea.x_max - nsfwArea.x_min, nsfwArea.y_max - nsfwArea.y_min
                sfwImage = sfwImage.resize(size)

                offset = nsfwArea.x_min, nsfwArea.y_min

                img.paste(sfwImage, offset, mask=sfwImage)

    censoredImagePath = "sfw_" + nsfwImagePath

    img.save(censoredImagePath)
    return censoredImagePath

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

            #req = self.get_request(f"http://127.0.0.1:5000/ocr?url={url}")
            #ocr_text = req["text"]
            #ocr_words = req["words"]
            #print(ocr_text, ocr_words)
            req = {
                "text": {
                    "description": "Fuck this shitty ass game bro this jungler is so bad look\nat him man going from blue buff to red buff to krugs to\nraptors to wolves gromp permafarming stupid ass kid\n",
                    "vertices": [
                        [
                            20,
                            18
                        ],
                        [
                            1563,
                            18
                        ],
                        [
                            1563,
                            243
                        ],
                        [
                            20,
                            243
                        ]
                    ]
                },
                "words": [
                    {
                        "description": "Fuck",
                        "vertices": [
                            [
                                24,
                                18
                            ],
                            [
                                153,
                                18
                            ],
                            [
                                153,
                                63
                            ],
                            [
                                24,
                                63
                            ]
                        ]
                    },
                    {
                        "description": "this",
                        "vertices": [
                            [
                                174,
                                18
                            ],
                            [
                                267,
                                18
                            ],
                            [
                                267,
                                63
                            ],
                            [
                                174,
                                63
                            ]
                        ]
                    },
                    {
                        "description": "shitty",
                        "vertices": [
                            [
                                292,
                                18
                            ],
                            [
                                435,
                                18
                            ],
                            [
                                435,
                                75
                            ],
                            [
                                292,
                                75
                            ]
                        ]
                    },
                    {
                        "description": "ass",
                        "vertices": [
                            [
                                456,
                                30
                            ],
                            [
                                549,
                                30
                            ],
                            [
                                549,
                                63
                            ],
                            [
                                456,
                                63
                            ]
                        ]
                    },
                ]
            }
            ocr_text = req["text"]
            ocr_words = req["words"]
            print(ocr_text['description'])
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
            ocrDict = {"data": ocrResults}

            if len(ocrResults) == 0:
                sfw_path = self.get_request(f"http://127.0.0.1:5000/pic-analysis?nsfw_path={nsfwImagePath}&sfw_path={sfwImagePath}")["path"]
            else:
                sfw_path = censorImage(ocrResults, nsfwImagePath, sfwImagePath, False)

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

