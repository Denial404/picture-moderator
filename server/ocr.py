import json

def detect_text_uri(uri):
    """Detects text in the file located in Google Cloud Storage or on the Web.
    """
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = uri


    # {
    #   text: { 1st thing}
    #    words: [{}{}{}{}]
    # }
    print(uri)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    # print('Texts:')
    result = {"text": {}, "words": []}
    for i,text in enumerate(texts):
        if i == 0: 
            result["text"]["description"] = text.description
            result["text"]["vertices"] = []

            for vertex in text.bounding_poly.vertices:
                result["text"]["vertices"].append((vertex.x, vertex.y))
        else:
            obj = {}
            obj["description"] = text.description
            obj["vertices"] = []

            for vertex in text.bounding_poly.vertices:
                obj["vertices"].append((vertex.x, vertex.y))
            result["words"].append(obj)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
                    
    # print(json.dumps(result, indent = 2))
    return result
    
if __name__ == '__main__':
    url = "https://cdn.vox-cdn.com/thumbor/cV8X8BZ-aGs8pv3D-sCMr5fQZyI=/1400x1400/filters:format(png)/cdn.vox-cdn.com/uploads/chorus_asset/file/19933026/image.png"
    detect_text_uri(url)

# {
# text: 'text in image',
# text_coords: [('text', array of coords), (...), ...]
# }