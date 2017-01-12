import readline
import re
import itertools
import collections

import enchant

#init english dictionary
dictionary = enchant.Dict("en_US")

# Upper limit of the word length
minWordLength = 3
maxWordLength = 8
maxCharIndex = maxWordLength - 1
#readline options
readline.parse_and_bind('tab: complete')
readline.parse_and_bind('set editing-mode vi')

#setup regex
reCompPosChar = re.compile("^([a-z]{1})([0-9]{1})$",re.DOTALL)
reCompPreChars = re.compile("^([a-z]{1,8})$", re.DOTALL)
reCompContains = re.compile("^\*([a-z])$", re.DOTALL)

class PositionalChar:
    charValue = '\0'
    position = -1

    def __init__(self, inCharValue, inPosition):
        self.charValue = inCharValue
        self.position = inPosition

def main():
    print "Prompt: (STOP to quit)\n"
    print "1. Max word length : ", maxWordLength, "\n"
    print "2. \"CharacterPostion\" e.g. f4 to indicate fixed char in word, index at 0\n"
    print "3. \"CharCharChar\" e.g. fybn to indicate available chars to construct the word\n"
    print "4. \"*Char\" e.g. *f contains f in the substring"

    availableChars = []
    positionMap = {}
    containsChar = None
    while True:
        line = raw_input("")
        if line == "STOP":
            break;
        else:
            posChar = reCompPosChar.search(line)
            # positional character search
            if posChar:
                char = posChar.group(1)
                position = int(posChar.group(2))
                positionMap[position] = char
                continue
            # available character search
            preChars = reCompPreChars.search(line)
            if preChars:
                availableChars = preChars.group(1)
                continue
            containsCharRe = reCompContains.search(line)
            if containsCharRe:
                containsChar = str(containsCharRe.group(1))
    words = generateWords(availableChars, positionMap, containsChar)
    print "\n".join(words)

def generateWords(availableChars, positionMap, containsChar):
    validWords = []
    # sort position map
    minWordLength = 3
    if positionMap and len(positionMap) > 0:
        sortedDict = collections.OrderedDict(sorted(positionMap.items()))
        maxIndex = int(sortedDict.keys()[-1])
        minWordLength = max(minWordLength, maxIndex)
    print "minword: ", minWordLength

    combinationArr = []
    if containsChar:
        availableChars = availableChars + containsChar
    for localLen in range(minWordLength, maxWordLength + 1): #index 0
        combinationArr = combinationArr + [seq for seq in itertools.permutations(availableChars, localLen)]

    for combinationTuple in combinationArr:
        word = ''.join(combinationTuple)
        # add the positional characters
        for position in positionMap:
            insertTuple = (positionMap[position], )
            combinationTuple = combinationTuple[:position] + insertTuple + combinationTuple[position:]
        # form the final word and check validity
        word = str(''.join(combinationTuple))
        if checkWordValidity(word):
            if not containsChar or containsChar in word:
                validWords.append(word)
    return validWords


def checkWordValidity(word):
    return dictionary.check(word)

main()