# Tesseract OCR

https://github.com/UB-Mannheim/tesseract/wiki

- download this, add to path

`pip install pytesseract`

pytesseract.pytesseract.tesseract_cmd=r'{}'.format(os.environ['TESS_PATH'])
- set 'TESS_PATH' variable to the location of tesseract.exe

# nltk
`python3 -m pip install nltk`

```
import nltk
nltk.download()
```

- you might need to run using sudo
- download stopwords, vader_lexicon
- do not unzip these files