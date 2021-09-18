import nltk
import os
# nltk.download()
from nltk.sentiment import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()
text = 'you have a big heart :)'

words = [w for w in text if w.isalpha()]
stopwords = nltk.corpus.stopwords.words('english')
filtered_words = [w for w in words if w.lower() not in stopwords]

print(sia.polarity_scores('you have a big heart :)'))
print(sia.polarity_scores(text))

