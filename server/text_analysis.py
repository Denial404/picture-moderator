import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

def sentiment(text):
    sia = SentimentIntensityAnalyzer()
    ### clean text
    # keep alpha chars
    words = [w for w in text if w.isalpha()]
    stopwords = nltk.corpus.stopwords.words('english')
    # remove stopwords
    filtered_words = [w for w in words if w.lower() not in stopwords]
    filtered_text = ' '.join(filtered_words)
    return sia.polarity_scores(text)
