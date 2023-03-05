from wrpy import WordReference, get_available_dicts

def get_dicts():
    return get_available_dicts()

def check_dict(dict_lang: str):
    dicts = get_dicts()
    for el in dicts:
        if dict_lang == el:
            return True
    
    return False

def get_translation(lang: str, word: str):
    wr = WordReference(lang)
    return wr.translate(word)