print('feel')

import jamspell
print('feel2')
corrector = jamspell.TSpellCorrector()
print('feel3')
corrector.LoadLangModel('en.bin')
print('feel4')
corrector.FixFragment('I am the begt spell cherken!')
# u'I am the best spell checker!'
print(corrector.FixFragment('I am the begt spell cherken!'))
# corrector.GetCandidates(['i', 'am', 'the', 'begt', 'spell', 'cherken'], 3)
# # (u'best', u'beat', u'belt', u'bet', u'bent', ... )
#
# corrector.GetCandidates(['i', 'am', 'the', 'begt', 'spell', 'cherken'], 5)
# # (u'checker', u'chicken', u'checked', u'wherein', u'coherent', ...)

print('helo')
print('helo21')