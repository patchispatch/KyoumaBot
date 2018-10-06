from config import DEFAULT_LANGUAGE

from textblob import TextBlob

def transalate_message(message):
    return TextBlob(message).translate(to=DEFAULT_LANGUAGE)
