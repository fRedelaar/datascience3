import enchant
import re
import pandas as pd
import string
from enchant.checker import SpellChecker
import datetime
import csv

begin_time = datetime.datetime.now()

d = enchant.DictWithPWL("en_US", "brandnames.txt")

traindata = pd.read_csv('../home-depot-data/test.csv', encoding="ISO-8859-1")
searchQueries = traindata["search_term"]


# The suggestions are returned in a list, ordered from most likely replacement to least likely. source:
# https://pyenchant.github.io/pyenchant/tutorial.html

def containsNumber(value):
    for character in value:
        if character.isdigit():
            return True
    return False


def repairWordsAutomatically(wordlist):
    """
    Function that will repair words automatically. Correct words will be skipped, faulty words repaired with the best
    PyEnchant suggestion. :param wordlist:
    """

    wordsCheckedOrCorrected = []
    for word in wordlist:
        print(word)
        word = word.translate(str.maketrans('', '', string.punctuation))

        if len(word.split()) > 1:
            TempStr = ''
            for x in word.split():
                if containsNumber(x):
                    TempStr = TempStr + ' ' + x
                elif not d.check(x):
                    sug = d.suggest(x.lower())
                    try:
                        sug = sug[0]
                        TempStr = TempStr + ' ' + sug
                    except:
                        print('no better suggestion found')
                else:
                    TempStr = TempStr + ' ' + x
            TempStr = TempStr.strip()
            wordsCheckedOrCorrected.append(TempStr)
        else:  # search query is one word
            if containsNumber(word):
                wordsCheckedOrCorrected.append(word)
            elif not d.check(word):
                sug = d.suggest(word.lower())
                try:
                    sug = sug[0]
                    wordsCheckedOrCorrected.append(sug)
                except:
                    print('no better suggestion found')
            else:
                wordsCheckedOrCorrected.append(word)
    print(wordsCheckedOrCorrected)
    df = pd.DataFrame(wordsCheckedOrCorrected)
    df.to_csv('PyEnchant-test-newest.csv', index=False, header=False)

repairWordsAutomatically(searchQueries)

print(datetime.datetime.now() - begin_time)
# Original: RMSE:  0.48270497676608215

# 0:21:05.866842  21 minutes for training data to be processed.
# when using pyEnchant RMSE becomes RMSE:  0.48853256912260096.

# when using pyEnchant with brandnames RMSE becomes RMSE:  0.48856219825774977
# probably worked shitty due caps :(

# spelling corrected with brand names, using all lowercases: RMSE: 0.48325103006033926  <-- finally some result!
