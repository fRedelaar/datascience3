from spellchecker import SpellChecker
import datetime
import pandas as pd
import string

spell = SpellChecker()
spell.word_frequency.load_text_file('./brandnames.txt')

begin_time = datetime.datetime.now()

traindata = pd.read_csv('../home-depot-data/test.csv', encoding="ISO-8859-1")
searchQueries = traindata["search_term"]

df = pd.DataFrame(searchQueries)
df.to_csv('test-original-search-queries.csv', index=False, header=False)

def containsNumber(value):
    for character in value:
        if character.isdigit():
            return True
    return False


def repairWordsAutomatically(wordlist):
    wordsCheckedOrCorrected = []

    for word in wordlist:
        print(word)

        if len(word.split()) > 1:
            TempStr = ''
            for x in word.split():
                if containsNumber(x):
                    TempStr = TempStr + ' ' + x
                else:
                    TempStr = TempStr + ' ' + spell.correction(x)
        else:
            TempStr = spell.correction(word)

        TempStr = TempStr.strip()
        wordsCheckedOrCorrected.append(TempStr)
    print(wordsCheckedOrCorrected)

    df = pd.DataFrame(wordsCheckedOrCorrected)
    df.to_csv('pyspellchecker-test.csv', index=False, header=False)


# repairWordsAutomatically(
#     ['lawn sprkinler', 'basemetnt window', 'basemetnt', 'wrrong ', 'handy cap', 'tolet', 'sprkinler',
#      'hampton bay eve'])
repairWordsAutomatically(searchQueries)
print(datetime.datetime.now() - begin_time)


# time to get train.csv converted: 0:42:31.059143
# time to get test.csv converted: 1:33:51.852624