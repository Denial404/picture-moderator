from PIL import Image, ImageDraw
from nudenet import NudeDetector
from nudenet import NudeClassifier

class NudeArea:
    def __init__(self, bounds, label, score):
        self.y_min = bounds[1]
        self.x_min = bounds[0]
        self.y_max = bounds[3]
        self.x_max = bounds[2]
        self.label = label
        self.score = score

def getNudeAreas(nudeResults):
    nudeAreas = []
    for nudeResult in nudeResults:
        nudeAreas.append(NudeArea(nudeResult["box"],
                                  nudeResult["label"],
                                  nudeResult["score"]))

    return nudeAreas

def censorImage(nsfwImagePath, sfwImagePath = ""):
    detector = NudeDetector() # detector = NudeDetector('base') for the "base" version of detector.
    nudeResults = detector.detect(nsfwImagePath)
    #classifier = NudeClassifier()
    #pokemon = classifier.classify(nsfwImagePath)

    nudeAreas = getNudeAreas(nudeResults)

    with Image.open(nsfwImagePath) as img:
        draw = ImageDraw.Draw(img)
        for nudeArea in nudeAreas:
            if (sfwImagePath == ""):
                draw.rectangle([nudeArea.x_min, nudeArea.y_min, nudeArea.x_max, nudeArea.y_max], '#0f0f0f80', '#0f0f0f80', 2)

            else:
                print("hello")

    x = nsfwImagePath.split("/")
    del x[-1]
    censoredImagePath = "sfw_" + nsfwImagePath

    img.save(censoredImagePath)

    return censoredImagePath
