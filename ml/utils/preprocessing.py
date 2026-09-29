import re
import html
import string
from typing import List

# Common English stopwords list (self-contained to eliminate runtime downloads)
STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
    "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't",
    "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during",
    "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't",
    "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here",
    "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i",
    "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's",
    "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself",
    "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought",
    "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she",
    "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than",
    "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there",
    "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this",
    "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't",
    "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's",
    "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom",
    "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll",
    "you're", "you've", "your", "yours", "yourself", "yourselves"
}

# In sentiment analysis, negations like 'not', 'no', 'nor', 'cannot' are crucial; we preserve them.
SENTIMENT_EXCLUDED_STOPWORDS = {"no", "not", "nor", "never", "cannot", "hardly", "barely"}
SENTIMENT_STOPWORDS = STOPWORDS - SENTIMENT_EXCLUDED_STOPWORDS


def clean_text(text: str, remove_stopwords: bool = False, keep_negations: bool = True) -> str:
    """
    Standard NLP text cleaning pipeline:
    1. Unescapes HTML entities (&amp;, &lt;, etc.)
    2. Removes HTML tags (<br />, <p>, etc.)
    3. Removes URLs and web links
    4. Removes email addresses and mentions (@username)
    5. Converts text to lowercase
    6. Removes punctuation and special characters
    7. Optionally filters stopwords
    8. Normalizes multiple spaces into a single space
    """
    if not isinstance(text, str):
        return ""

    # Unescape HTML entities
    cleaned = html.unescape(text)

    # Remove HTML tags
    cleaned = re.sub(r"<[^>]+>", " ", cleaned)

    # Remove URLs
    cleaned = re.sub(r"https?://\S+|www\.\S+", " ", cleaned)

    # Remove email addresses and user mentions
    cleaned = re.sub(r"\S+@\S+", " ", cleaned)
    cleaned = re.sub(r"@\w+", " ", cleaned)

    # Lowercase
    cleaned = cleaned.lower()

    # Remove punctuation & numbers (replace with space to prevent glued words)
    cleaned = re.sub(r"[^a-z\s]", " ", cleaned)

    # Tokenize by whitespace
    tokens = cleaned.split()

    # Stopwords filtering if enabled
    if remove_stopwords:
        sw = SENTIMENT_STOPWORDS if keep_negations else STOPWORDS
        tokens = [t for t in tokens if t not in sw and len(t) > 1]

    # Normalize whitespace
    return " ".join(tokens).strip()
