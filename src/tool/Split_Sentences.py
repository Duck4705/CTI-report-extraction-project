import re
import nltk

def split_sentences(text):
    # Tách tại dấu chấm, phía sau là khoảng trắng và chữ cái viết hoa
    pattern = r'(?<=\.)\s+(?=[A-Z])'
    return re.split(pattern, text)
