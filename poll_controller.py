from nltk.corpus import wordnet, words
import random
import requests

user_wordlist = []
user_learned_words = []

def get_synonyms(word):

    if(not isinstance(word, str)):
        return False

    synonyms = []

    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            if l.name().lower() not in synonyms and l.name().lower() != word and not '_' in l.name():
                synonyms.append(l.name().lower())

    return synonyms

def create_options():
    if(user_wordlist):
        word = random.choice(user_wordlist)
    else:
        word = words.words()
        random.shuffle(word)
        for el in word:
            if(len(get_synonyms(el)) >= 2 and not(el in user_learned_words)): 
                word = el
                break

    options = get_synonyms(word)
    del options[2:]

    options.append(word)

    random.shuffle(options)

    correct_option_id = options.index(word)

    translated_options = translate_options(options)

    return [word, translated_options, correct_option_id]

def translate_options(options):
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'
        }

    for index, option in enumerate(options):
        url = 'https://clients5.google.com/translate_a/t?client=dict-chrome-ex&sl=auto&tl=ru&q=' + option

        res = requests.get(url, headers=headers).json()
        if(res.get('dict')):
            for el  in res['dict'][0]['terms']:
                if(el.lower() not in options):
                    options[index] = el.lower()
                    break
        else:
            options[index] = res['sentences'][0]['trans']

    return options