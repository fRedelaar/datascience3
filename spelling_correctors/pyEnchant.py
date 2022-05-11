import enchant
import re
import pandas as pd
from enchant.checker import SpellChecker

d = enchant.Dict("en_US")

traindata = pd.read_csv('../home-depot-data/train.csv', encoding="ISO-8859-1")
searchQueries = traindata["search_term"]

# The suggestions are returned in a list, ordered from most likely replacement to least likely. source:
# https://pyenchant.github.io/pyenchant/tutorial.html

def repairWordsAutomatically(wordlist):
    """
    Function that will repair words automatically. Correct words will be skipped, faulty words repaired with the best
    PyEnchant suggestion. :param wordlist:
    """
    """" TO DO: Only lists single words are working now. We also have search queries consisting of multiple words.
         Method: Check for each search_Term whether there is more than 1 word. If so, check the entire block of text.
         Then, when errored words come up, repair those and put all words back in as 1 search term query."""


    wordsCheckedOrCorrected = []
    for word in wordlist:
        if len(word.split()) > 1:
            for x in word.split():
                TempStr = ''
                if not d.check(x):
                    sug = d.suggest(x)
                    sug = sug[0]
                    TempStr = TempStr + ' ' + sug
                else:
                    TempStr = TempStr + ' ' + word
            wordsCheckedOrCorrected.append(TempStr)
        else:
            if not d.check(word):
                sug = d.suggest(word)
                sug = sug[0]
                wordsCheckedOrCorrected.append(sug)
            else:
                wordsCheckedOrCorrected.append(word)
    print(wordsCheckedOrCorrected)


repairWordsAutomatically(['dog', 'cat', 'cat hello omg', 'dog', 'gud', 'good dog', 'sprinkelr'])
# repairWordsAutomatically(searchQueries)
