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
from nudenet import NudeClassifier
from cloud_storage import upload_blob, download_blob
import numpy as np

bucket_name = "image_paths"


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

def censorImage(results, nsfw_image_bytes, sfwImagePath = "", censorImage = True):
    nsfwAreas = getNsfwAreas(results, censorImage)

    with Image.open(BytesIO(nsfw_image_bytes)) as img:
        draw = ImageDraw.Draw(img)
        for nsfwArea in nsfwAreas:
            if (sfwImagePath == ""): # 
                draw.rectangle([nsfwArea.x_min, nsfwArea.y_min, nsfwArea.x_max, nsfwArea.y_max], '#0f0f0f80', '#0f0f0f80', 2)
            else:
                sfw_image_bytes = download_blob(bucket_name, sfwImagePath)
                sfwImage = Image.open(BytesIO(sfw_image_bytes))

                size = nsfwArea.x_max - nsfwArea.x_min, nsfwArea.y_max - nsfwArea.y_min
                sfwImage = sfwImage.resize(size)

                offset = nsfwArea.x_min, nsfwArea.y_min

                img.paste(sfwImage, offset, mask=sfwImage)

    # censoredImagePath = "sfw_" + nsfw_image_bytes

    # img.save(censoredImagePath)

    buf = BytesIO()
    img.save(buf, format="PNG")
    img_bytes = buf.getvalue()
    censoredImagePath = "nsfw_censored"
    upload_blob(bucket_name, img_bytes, "nsfw_censored", "image/png")
    return censoredImagePath

def pic_analysis(nsfw_path, sfwImagePath):
    # download the images from cloud storage
    nsfw_image_bytes = download_blob(bucket_name, nsfw_path) # returns the image downloaded as bytes

    img =  Image.open(BytesIO(nsfw_image_bytes))
    detector = NudeDetector()  # detector = NudeDetector('base') for the "base" version of detector.
    detector_json = detector.detect(np.array(img))
    print("CENSORED AREAS", detector_json)
    # pass the nsfw_image (bytes) and sfw_path (the cat.png on cloud) 
    result_path = censorImage(detector_json, nsfw_image_bytes, sfwImagePath) 
    return {"path": result_path}

def classifyImage(nsfw_path):
    nsfw_image_bytes = download_blob(bucket_name, nsfw_path) # returns the image downloaded as bytes
    img =  Image.open(BytesIO(nsfw_image_bytes))

    classifier = NudeClassifier()
    result = classifier.classify(np.array(img))
    print(result)
    return result[0]["safe"]


class BotRequest(commands.Cog):
    def __init__(self, client):
        self.client = client

    def get_request(self, url):
        # server url
        print("URL", url)
        res = requests.get(url)
        print("GET_REQUEST", res)
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

            # text analysis
            # site = "http://127.0.0.1:5000/"
            site = "https://flask-server-dot-endless-orb-325023.ue.r.appspot.com/"

            req = self.get_request(f"{site}ocr?url={url}")
            ocr_text = req["text"]
            ocr_words = req["words"]

            #Sentient analysis
            try:
                text_info = self.get_request(f"{site}analyze-text?text={ocr_text['description']}")
            except:
                print("ERRORRRR AT SENTIENT ANALYSIS")

            ocrResults = []
            for ocr_word in ocr_words:
                if profanity.contains_profanity(ocr_word["description"]):
                    ocrResults.append(ocr_word)

            ### img analysis
            # get image data
            # response = requests.get(url)
            # img = Image.open(BytesIO(response.content))
            # nsfwImagePath = "nsfw.png"
            # # save nsfw image
            # img.save(nsfwImagePath)
            # sfwImagePath = "cat.png"
            ## -- revised version --
            nsfwImagePath = "nsfw_image"
            sfwImagePath = "sfw_image"
            upload_blob(bucket_name, url, nsfwImagePath, "image/png")

            # sfw_path = self.get_request(f'{site}pic-analysis?nsfw_path={nsfwImagePath}&sfw_path={sfwImagePath}')["path"]
            sfw_path = pic_analysis(nsfwImagePath, sfwImagePath)
            sfw_path = sfw_path["path"] # nsfw_censored on cloud storage
            cennsored_image_bytes = download_blob(bucket_name, sfw_path) # download the censored images we just uploaded as bytes

            if len(ocrResults) != 0:
                sfw_path = censorImage(ocrResults, cennsored_image_bytes, sfwImagePath, False)

            final_image_bytes = download_blob(bucket_name, sfw_path)
            final_image = Image.open(BytesIO(final_image_bytes))

            with BytesIO() as image_binary:
                final_image.save(image_binary, "PNG")
                image_binary.seek(0)
                f = discord.File(fp=image_binary, filename="image.png")
            await ctx.send(file=f)
            # setup embed
            embed = discord.Embed(title='Picture Police', colour=0xf6dae4)
            embed.set_author(name=f'{ctx.author.display_name}')
            # positive

            # classifier
            sfw_level = classifyImage(nsfwImagePath)

            try:                
                value = "⭐"   
                value = value * round(sfw_level * 10 // 2)

                if not value:
                    value = "⭐"  

                embed.add_field(name='Image SFW',
                                value=value,
                                inline=True)
                if bool(text_info['analysis']['profanity']):
                    embed.add_field(name='Profanity?',
                                    value='🤬',
                                    inline=True)
                else:
                    embed.add_field(name='Profanity?',
                                    value='👌',
                                    inline=True)

                if text_info['analysis']['scores']['neg'] >= 60 or bool(text_info['analysis']['profanity']):
                    embed.add_field(name='Text Positivity',
                                value='😔',
                                inline=True)
                else:
                    embed.add_field(name='Text Positivity',
                                    value='😊',
                                    inline=False)
            except:
                print('ERRORREEROROR AT EMVED ADD FIELD')

            await ctx.send(embed=embed)

