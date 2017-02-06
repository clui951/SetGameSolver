""" 
Usage:
$ python SetGame.py < setsample1.txt
$ cat setsample2.txt | python SetGame.py
"""

import sys


### MAIN ###

def main():
    cards = parseInputToCards()

    # number of possible sets
    allSets = findAllSets(cards)
    print(len(allSets))

    # number of sets in disjoint set
    resultSets = findLargestDisjointSet(set(), allSets)
    print(len(resultSets))

    # sets in disjoint set
    for sett in resultSets:
        print("")
        printSet(sett)



### CONSTANTS ###

COLOR_FEATURES = {
    "blue" : 0,
    "yellow" : 1,
    "green" : 2,
}

SYMBOL_SHADE_FEATURES = {
    "a" : (0, 0),
    "s" : (1, 0),
    "h" : (2, 0),
    "A" : (0, 1),
    "S" : (1, 1),
    "H" : (2, 1),
    "@" : (0, 2),
    "$" : (1, 2),
    "#" : (2, 2)
}



### MODEL ###

class Card:
    class_counter = 1

    def __init__(self, cardString):
        cardToks = cardString.split(" ")
        self.color = cardToks[0]
        self.symbol = cardToks[1][0]
        self.count = len(cardToks[1])

        # features as numerics to simplify set checking
        self.val0 = COLOR_FEATURES[self.color]
        self.val1, self.val2  = SYMBOL_SHADE_FEATURES[self.symbol]
        self.val3 = self.count - 1

        # used to find disjoint sets
        self.id = Card.class_counter
        Card.class_counter += 1

    def __str__(self):
        return self.color + " " + self.symbol * self.count

    # str representation including features as numerics
    def detailedstr(self):
        return "Card: " + self.color + " " + self.symbol * self.count + " : " + str(self.val0) + " " + str(self.val1) + " " + str(self.val2) + " " + str(self.val3)



### FUNCTIONS ###

def parseInputToCards():
    first = True
    cards = []
    numCards = int(sys.stdin.readline())
    for i in range(numCards):
        line = sys.stdin.readline()
        cards.append(Card(line.rstrip()))
    return cards


def isSet(card1, card2, card3):
    if ((card1.val0 + card2.val0 + card3.val0) % 3 != 0 or
        (card1.val1 + card2.val1 + card3.val1) % 3 != 0 or
        (card1.val2 + card2.val2 + card3.val2) % 3 != 0 or
        (card1.val3 + card2.val3 + card3.val3) % 3 != 0 ):
        return False
    return True


def findAllSets(cards):
    size = len(cards)
    if size < 3:
        return None, 0
    allSets = []
    for i in range(0, size):
        for j in range(i+1, size):
            for k in range(j+1, size):
                card1 = cards[i]
                card2 = cards[j]
                card3 = cards[k]
                if isSet(card1, card2, card3):
                    allSets.append((card1, card2, card3))
    return allSets


def findLargestDisjointSet( setIDsUsed, setsLeft):
    if len(setsLeft) == 0:
        return []
    newSet = setsLeft[-1]
    newSetsLeft = setsLeft[:-1]
    canBeUsed = True
    for card in newSet:
        if card.id in setIDsUsed:
            canBeUsed = False
    # not using current set
    unused = findLargestDisjointSet(setIDsUsed, newSetsLeft)

    if canBeUsed:
        # using current set
        newSetIDsUsed = setIDsUsed.copy()
        for card in newSet:
            newSetIDsUsed.add(card.id)
        used = [newSet] + findLargestDisjointSet(newSetIDsUsed, newSetsLeft)
        if len(used) > len(unused):
            return used
    return unused


def printSetDetailed(sett):
    for card in sett:
        print(card.detailedstr())


def printSet(sett):
    for card in sett:
        print(card)



### RUN MAIN ###
if __name__ == '__main__':
    main()

