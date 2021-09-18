import json

def detect_text_uri(uri):
    """Detects text in the file located in Google Cloud Storage or on the Web.
    """
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = uri

    response = client.text_detection(image=image)
    texts = response.text_annotations
    # print('Texts:')
    result = []
    for text in texts:
        obj = {}
        vertices = []
        for vertex in text.bounding_poly.vertices:
            vertices.append((vertex.x, vertex.y))
        obj[text.description] = vertices
        result.append(obj)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
                    
    print(json.dumps(result, indent = 2))
    return result
    
if __name__ == '__main__':
    url = "https://cdn.vox-cdn.com/thumbor/cV8X8BZ-aGs8pv3D-sCMr5fQZyI=/1400x1400/filters:format(png)/cdn.vox-cdn.com/uploads/chorus_asset/file/19933026/image.png"
    detect_text_uri(url)

# {
# text: 'text in image',
# text_coords: [('text', array of coords), (...), ...]
# }