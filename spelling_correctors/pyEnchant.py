import enchant

d = enchant.Dict("en_US")

# The suggestions are returned in a list, ordered from most likely replacement to least likely. source:
# https://pyenchant.github.io/pyenchant/tutorial.html


def repairWordsAutomatically(wordlist):
    wordsCheckedOrCorrected = []

    for word in wordlist:
        if not d.check(word):
            sug = d.suggest(word)
            sug = sug[0]
            wordsCheckedOrCorrected.append(sug)
        else:
            wordsCheckedOrCorrected.append(word)
    print(wordsCheckedOrCorrected)


repairWordsAutomatically(['cat','dog', 'gud', 'good', 'sprinkelr'])
