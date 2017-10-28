import re

def checkKatakana(str):
    regexp = u'([^ァ-ンヴー・\s-])'
    if re.search(regexp, str) is None:
        return True
    else:
        return False
