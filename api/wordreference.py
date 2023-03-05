from wrpy import WordReference, get_available_dicts

def get_dicts():
    dicts = get_available_dicts()

    for el in list(dicts):
        if dicts[el]['to'] != "English":
            dicts.pop(el)

    return dicts 

def check_dict(dict_lang: str):
    dicts = get_dicts()
    for el in dicts:
        if dict_lang == el[:2]:
            return True
    
    return False

def get_translation(dict_code: str, word: str):
    wr = WordReference(dict_code)

    try:
        translation = wr.translate(word)
    except NameError:
        translation = False

    return translation