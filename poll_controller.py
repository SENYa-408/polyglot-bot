from nltk.corpus import wordnet, words
import random
import requests

user_wordlist = []
user_learned_words = []

def create_quiz():
    # get word from the wordlist if its not empty or from the wordnet
    # word have to be without _ and have 2 or more synonyms

    if(user_wordlist):
        test_word = random.choice(user_wordlist)
    else:
        test_word = words.words()
        random.shuffle(test_word)
        for el in test_word:
            if(len(get_options(el)) >= 2 and not(el in user_learned_words)): 
                test_word = el
                break

    # get synonyms for the word with synonyms function
    # synonyms translations have to be unique

    options = get_options(test_word)

    # get 2 synonyms and add word to them
    # translate options
    # find index of the word

    del options[2:]

    options.append(translate(test_word)[0])

    random.shuffle(options)

    correct_option_index = options.index(translate(test_word)[0])

    return test_word, options, correct_option_index

def get_options(test_word):

    if(not isinstance(test_word, str)):
        return False

    options = []

    for syn in wordnet.synsets(test_word):
        for l in syn.lemmas():
            translates = translate(l.name().lower())
            if(len(options) == 2):
                break

            for option in translates:
                if option not in options and not ' ' in option:
                    options.append(option)

    return options

def translate(word):
    # if isinstance(words, str):
    #         words = [words]

    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'
        }
    
    url = 'https://clients5.google.com/translate_a/t?client=dict-chrome-ex&sl=auto&tl=ru&q=' + word

    res = requests.get(url, headers=headers).json()

    if(res.get('dict')):
        print(res['dict'][0]['terms'])
        word = res['dict'][0]['terms']
    else:
        print(res['sentences'][0]['trans'])
        word = res['sentences'][0]['trans']

    # for index, word in enumerate(words):
    #     url = 'https://clients5.google.com/translate_a/t?client=dict-chrome-ex&sl=auto&tl=ru&q=' + word

    #     res = requests.get(url, headers=headers).json()

    #     if(res.get('dict')):
    #         for el  in res['dict'][0]['terms']:
    #             if(el.lower() not in words):
    #                 # print(words[index], el.lower())
    #                 words[index] = el.lower()
    #                 break
    #     else:
    #         # print(words[index], res['sentences'][0]['trans'])
    #         words[index] = res['sentences'][0]['trans']

    return word