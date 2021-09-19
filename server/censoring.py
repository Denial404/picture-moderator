from PIL import Image, ImageDraw
from nudenet import NudeDetector
# from nudenet import NudeClassifier

class NsfwArea:
    def __init__(self, bounds, label, score):
        self.y_min = bounds[1]
        self.x_min = bounds[0]
        self.y_max = bounds[3]
        self.x_max = bounds[2]
        self.label = label
        self.score = score

def getNsfwAreas(nudeResults):
    nsfwAreas = []
    print(nudeResults)
    for nsfwArea in nudeResults:
        nsfwAreas.append(NsfwArea(nsfwArea["box"],
                                  nsfwArea["label"],
                                  nsfwArea["score"]))

    return nsfwAreas

def censorImage(results, nsfwImagePath, sfwImagePath = ""):
    nsfwAreas = getNsfwAreas(results)

    with Image.open(nsfwImagePath) as img:
        draw = ImageDraw.Draw(img)
        for nsfwArea in nsfwAreas:
            if (sfwImagePath == ""):
                draw.rectangle([nsfwArea.x_min, nsfwArea.y_min, nsfwArea.x_max, nsfwArea.y_max], '#0f0f0f80', '#0f0f0f80', 2)
            else:
                sfwImage = Image.open(sfwImagePath)

                size = nsfwArea.x_max - nsfwArea.x_min, nsfwArea.y_max - nsfwArea.y_min
                sfwImage.resize(size)

                offset = nsfwArea.x_min, nsfwArea.y_min

                img.paste(sfwImage, offset)

    x = nsfwImagePath.split("/")
    del x[-1]
    censoredImagePath = "sfw_" + nsfwImagePath

    img.save(censoredImagePath)

    return censoredImagePath