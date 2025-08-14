from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon', quiet=True)

_sia = SentimentIntensityAnalyzer()

def get_sentiment(text: str):
    if not text.strip():
        return 0.0, "neutral"
    scores = _sia.polarity_scores(text)
    compound = scores["compound"]
    if compound >= 0.05:
        label = "positive"
    elif compound <= -0.05:
        label = "negative"
    else:
        label = "neutral"
    return compound, label
