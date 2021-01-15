import re

from mtranslate import translate

from extraction.utils.spell_correction import get_google_spelling


def normalize_arabic(text):

    # text = re.sub(" ال", " ", text)
    text = re.sub("[إأٱآا]", "ا", text)
    # text = re.sub("ى", "ي", text)
    text = re.sub("[يىی]", "ي", text)
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
    return text


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def translate_and_fix(name,from_lang,to_lang):

    translation = translate(name, to_lang, from_lang)
    # print("translation ",translation)
    return get_google_spelling(translation)

