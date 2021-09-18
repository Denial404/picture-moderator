try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import os

img ='./test/cs.jpg'
# set tesseract path os var
pytesseract.pytesseract.tesseract_cmd=r'{}'.format(os.environ['TESS_PATH'])
text = pytesseract.image_to_string(img)
print(text)

# print(pytesseract.image_to_boxes(Image.open(img)))

# Get verbose data including boxes, confidences, line and page numbers
print(pytesseract.image_to_data(Image.open(img)))
