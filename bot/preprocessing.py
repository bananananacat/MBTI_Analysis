import re
import string
from nltk.stem import SnowballStemmer


def reg_handling(content: str) -> str:
    """
    deleting punctuation, links, etc from DataFrame
    """

    content = re.sub(r"http\S*", " ", content.lower().lstrip("'"))
    content = re.sub(r'\|{3,}', ' N ', content)
    content = content.translate(str.maketrans(' ', ' ', string.punctuation))
    content = re.sub(r'[^A-z]', ' ', content)

    return content


def applying_stemmer(text: str, stemmer: SnowballStemmer) -> str:
    new_text = [stemmer.stem(word) for word in text.split()]
    return " ".join(new_text)


def applying_vocab(text: str, vocab: list[str]) -> str:
    """
    reducing inappropriate words from DataFrame, 
    such as stop words and too rare words
    """
    new_text = [word for word in text.split() if word in vocab]
    return " ".join(new_text)
