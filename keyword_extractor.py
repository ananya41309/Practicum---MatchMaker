import nltk
from collections import Counter
import re

# Download required resources once
nltk.download("stopwords", quiet=True)
nltk.download("punkt", quiet=True)

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def extract_keywords(text, top_n=15):
    """
    Extract top N keywords from text
    """
    # Lowercase
    text = text.lower()

    # Remove punctuation & numbers
    text = re.sub(r"[^a-z\s]", " ", text)

    # Tokenize
    words = word_tokenize(text)

    # Remove stopwords and short words
    stop_words = set(stopwords.words("english"))
    keywords = [
        w for w in words
        if w not in stop_words and len(w) > 2
    ]

    # Count frequency
    freq = Counter(keywords)

    return [word for word, _ in freq.most_common(top_n)]
