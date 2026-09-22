import string
from bot.data.bad_words import BAD_WORDS

punctuation_table = str.maketrans("", "", string.punctuation)

def count_profanity(text):
    words = text.lower().translate(punctuation_table).split()

    count = 0

    for message in words:
        if message in BAD_WORDS:
            count += 1
    
    return count

