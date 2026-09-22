import re
import unicodedata

from bot.data.bad_words import BAD_WORDS


CHARACTER_REPLACEMENTS = {
    "0": "о",
    "1": "и",
    "3": "з",
    "4": "ч",
    "6": "б",
    "7": "т",
    "@": "а",
    "$": "с",
    "€": "е",
}


HOMOGLYPHS = {
    "a": "а",
    "c": "с",
    "e": "е",
    "o": "о",
    "p": "р",
    "x": "х",
    "y": "у",
    "k": "к",
    "m": "м",
    "t": "т",
    "b": "в",
}


def normalize_unicode(text):
    text = unicodedata.normalize("NFKC", text)

    return text.lower()


def replace_special_characters(text):
    for old, new in CHARACTER_REPLACEMENTS.items():
        text = text.replace(old, new)

    return text


def replace_homoglyphs(text):
    result = []

    for char in text:
        result.append(HOMOGLYPHS.get(char, char))

    return "".join(result)


def remove_noise(text):
    result = []

    for char in text:
        if char.isalpha() or char.isdigit():
            result.append(char)

        elif char.isspace():
            result.append(" ")

    return "".join(result)


def collapse_repeated_characters(text):
    return re.sub(r"(.)\1+", r"\1", text)


def merge_spaced_letters(text):
    words = text.split()

    result = []
    buffer = []

    for word in words:
        if len(word) == 1 and word.isalpha():
            buffer.append(word)
            continue

        if buffer:
            result.append("".join(buffer))
            buffer.clear()

        result.append(word)

    if buffer:
        result.append("".join(buffer))

    return " ".join(result)


def normalize_text(text):
    text = normalize_unicode(text)
    text = replace_special_characters(text)
    text = replace_homoglyphs(text)
    text = remove_noise(text)
    text = collapse_repeated_characters(text)
    text = merge_spaced_letters(text)

    return text


def levenshtein_distance(first, second):
    if first == second:
        return 0

    if not first:
        return len(second)

    if not second:
        return len(first)

    previous_row = list(range(len(second) + 1))

    for i, first_char in enumerate(first, start=1):
        current_row = [i]

        for j, second_char in enumerate(second, start=1):
            insertion = current_row[j - 1] + 1
            deletion = previous_row[j] + 1

            replacement = previous_row[j - 1]

            if first_char != second_char:
                replacement += 1

            current_row.append(
                min(
                    insertion,
                    deletion,
                    replacement
                )
            )

        previous_row = current_row

    return previous_row[-1]


def is_similar_word(word, bad_word):
    if word == bad_word:
        return True

    if len(bad_word) <= 4:
        return False

    distance = levenshtein_distance(word, bad_word)

    if len(bad_word) <= 6:
        return distance <= 1

    return distance <= 2


def is_profanity_word(word):
    if word in BAD_WORDS:
        return True

    for bad_word in BAD_WORDS:
        if is_similar_word(word, bad_word):
            return True

    return False


def count_profanity(text):
    normalized_text = normalize_text(text)

    words = normalized_text.split()

    count = 0

    for word in words:
        if is_profanity_word(word):
            count += 1

    return count