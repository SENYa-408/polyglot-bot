import requests

def translate(words):
    if(isinstance(words, str)):
        words = [words]

    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'
    }
    
    for index, word in enumerate(words):
        if('_' in word):
            word = word.replace('_',' ')
        
        url = 'https://clients5.google.com/translate_a/t?client=dict-chrome-ex&sl=auto&tl=ru&q=' + word

        res = requests.get(url, headers=headers).json()

        words[index] = res['sentences'][0]['trans']
    
    if(len(words) == 1):
        words = words[0]

    return words