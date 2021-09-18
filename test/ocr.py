import pytesseract
import os

img ='./test/cs.jpg'
# set tesseract path os var
pytesseract.pytesseract.tesseract_cmd=r'{}'.format(os.environ['TESS_PATH'])
text = pytesseract.image_to_string(img)
print(text)

