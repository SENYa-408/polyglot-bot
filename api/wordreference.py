from wrpy import WordReference, get_available_dicts

def get_dicts():
    return get_available_dicts()

def get_translation(lang: str, word: str):
    wr = WordReference(lang)
    return wr.translate(word)