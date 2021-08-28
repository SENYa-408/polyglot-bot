from nltk.corpus import wordnet, words
import random
from translate import translate

user_wordlist = []
user_learned_words = []

def create_quiz():

    # 1. take word from the wordlist. If wordlist is empty use wordnet
    word = random_word()

    # 2. find at least two synonyms with unique translation for the word and translate them
    options = get_options(word)

    # 4. translate word
    translated_word = translate(word)

    # 5. add a word translation to the list of 2 synonyms
    options.append(translated_word)
    random.shuffle(options)

    # 6. get index of the translated word
    correct_option_index = options.index(translate(word))

    # 7. return created list
    print(word, options, correct_option_index)
    return word, options, correct_option_index

def random_word():
    if(user_wordlist):
        word = random.choice(user_wordlist)
    else:
        word = words.words()
        random.shuffle(word)

        for el in word:
            # word must have no underscores
            # word must have at least two unique translated synonyms
            # word must not be in the user_learned_words list
            if(len(get_options(el)) >= 2 and not '_' in el and not(el in user_learned_words)): 
                word = el
                break

    return word

# returns 2 unique translated synonyms of the given word
def get_options(word):
    translated_word = translate(word)
    synonyms = []

    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            if(len(synonyms) == 2):
                break
            
            translation = translate(l.name().lower())
            if translation not in synonyms and translation != translated_word:
                    synonyms.append(translation)

    return synonyms
