from langdetect import detect, DetectorFactory
import re
from nltk.corpus import words

# Checking if gibberish like asdsacaewefhj
def is_nonsensical_input(user_input):
    DetectorFactory.seed = 0  # For consistent results

    # Check if the input is a single "word" of random letters longer than 10 chars
    if re.match(r'^[a-zA-Z]+$', user_input) and len(user_input) > 10:
        return True

    # Check for too many consecutive consonants or vowels (threshold raised to 5)
    if re.search(r'(?i)([bcdfghjklmnpqrstvwxyz]{5,}|[aeiou]{5,})', user_input):
        return True

    # Load valid words
    valid_words = set(words.words())
    input_words = user_input.split()

    # Allow for some non-dictionary words; flag if more than 50% of the words are invalid
    invalid_word_count = sum(1 for word in input_words if word not in valid_words)
    if invalid_word_count > len(input_words) / 2:
        return True

    # Language detection - allow for short queries and names
    if len(user_input) > 20:  # Only check longer inputs
        try:
            lang = detect(user_input)
            if lang != 'en':  # Flag only non-English
                return True
        except:
            pass  # Handle detection failures silently

    return False
