from spellchecker import SpellChecker
import datetime
import pandas as pd
from textblob import TextBlob
import string

spell = SpellChecker()
spell.word_frequency.load_text_file('./brandnames.txt')

begin_time = datetime.datetime.now()

traindata = pd.read_csv('../home-depot-data/test.csv', encoding="ISO-8859-1")
searchQueries = traindata["search_term"]

df = pd.DataFrame(searchQueries)
df.to_csv('test-textblob.csv', index=False, header=False)


def containsNumber(value):
    for character in value:
        if character.isdigit():
            return True
    return False


def repairWordsAutomatically(wordlist):
    wordsCheckedOrCorrected = []
    b = ''

    for word in wordlist:
        print(word)

        if len(word.split()) > 1:
            TempStr = ''
            for x in word.split():
                if containsNumber(x):
                    TempStr = TempStr + ' ' + x
                else:
                    b = TextBlob(x)
                    TempStr = TempStr + ' ' + str(b.correct())
        else:
            b = TextBlob(word)
            TempStr = str(b.correct())

        TempStr = TempStr.strip()
        wordsCheckedOrCorrected.append(TempStr)
    print(wordsCheckedOrCorrected)

    df = pd.DataFrame(wordsCheckedOrCorrected)
    df.to_csv('textblob-test.csv', index=False, header=False)




# time to get train.csv converted: 1:21:32.076782
# time to get test.csv converted: 2:41:46.742523

# wordsToRepair = ['lawn sprkinler', 'basemetnt window', 'basemetnt', 'wrrong ', 'handy cap', 'tolet', 'sprkinler',
#                  'hampton bay eve']
# sentences = 'Hello I am Felicia, still kkickin it! Gutars are cool'

repairWordsAutomatically(searchQueries)
print(datetime.datetime.now() - begin_time)