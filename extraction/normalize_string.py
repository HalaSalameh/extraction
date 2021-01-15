import re
import numpy as np
from mtranslate import translate
from extraction.utils.spell_correction import get_google_spelling


def normalize_arabic(text):

    text = re.sub("[إأٱا]", "ا", text)
    text = re.sub("[ىی]", "ي", text)
    text = re.sub("[إأٱآا]", "ا", text)
    # text = re.sub("ى", "ي", text)
    text = re.sub("[یییيىی]", "ي", text)
    text = re.sub("ؤ", "ء", text)
    text = re.sub("ئ", "ء", text)
    text = re.sub("ة", "ه", text)
    text = re.sub("ـ", "", text)
    text = re.sub("  ", " ", text)
    text = re.sub("َ", "", text)
    text = re.sub("ً", "", text)
    text = re.sub("ُ", "", text)
    text = re.sub("ٌ", "", text)
    text = re.sub("ِ", "", text)
    text = re.sub("ٍ", "", text)
    text = re.sub("ّ", "", text)
    text = re.sub("[ککککک]", "ك", text)
    text = re.sub("ھ", "ه", text)
    text = re.sub("چ", "ج", text)
    text = re.sub("ھ", "ه", text)
    return text


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def translate_and_fix(name, from_lang, to_lang):

    translation = translate(name, to_lang, from_lang)
    # print("translation ",translation)
    return get_google_spelling(translation)


def distance_words(seq1, seq2):
    seq1 = seq1.lower()
    seq2 = seq2.lower()
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros ((size_x, size_y))
    for x in range(size_x):
        matrix[x, 0] = x
    for y in range(size_y):
        matrix[0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x-1] == seq2[y-1]:
                matrix [x,y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 1
                )
            else:
                matrix [x,y] = min(
                    matrix[x-1,y] + 1,
                    matrix[x-1,y-1] + 1,
                    matrix[x, y-1] + 1
                )
    return matrix[size_x - 1, size_y - 1]
