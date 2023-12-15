from isl_util import *
from isl_parser import *

def islSetGetParams(parsedSet):
    return parsedSet[0][0]

def islSetGetTuple(parsedSet):
    return parsedSet[1][0:2]

def islSetGetTupleName(parsedSet):
    return parsedSet[1][0][0][0]

def islSetGetTupleDims(parsedSet):
    return parsedSet[1][0][1]

def islSetGetLsdTupleDim(parsedSet):
    return islSetGetTupleDims(parsedSet)[-1]

def islSetGetLexmin(parsedSet):
    return islSetGetTupleDims(parsedSet)[0]

def islPointGetTupleDims(parsedPoint):
    return parsedPoint[0][1]

def islMapGetDomTupleName(parsedMap):
    return parsedMap[1][0][0]

def islMapGetRangeTupleName(parsedMap):
    return parsedMap[1][0][0]

def islMapGetRangeTupleDims(parsedMap):
    return parsedMap[1][1]

def islCardHasOnlyOneEntry(parsedCard):
    return len(parsedCard) == 1

def islCardGetOnlyEntry(parsedCard):
    if not islCardHasOnlyOneEntry(parsedCard):
        raise Exception("No single entry")
    return parsedCard[0][0]

def islCardGetNumEntries(parsedCard):
    return len(parsedCard)

def islCardGetEntries(parsedCard):
    return [ entry[0] for entry in parsedCard ]

def checkIsSet(s):
    if not isSet(s):
        msg = "Cannot extract array dims from: " + str(s)
        raise Exception(msg)

def getLexmin(s):
    checkIsSet(s)
    setAsStr = str(s)
    parsedSet = IslSetParser.grammar.parse(setAsStr).unwrap()
    return islSetGetLexmin(parsedSet)

def getParams(s):
    checkIsSet(s)
    setAsStr = str(s)
    print(setAsStr)
    parsedSet = IslSetParser.grammar.parse(setAsStr).unwrap()
    print("parsedSet", parsedSet)
    params = islSetGetParams(parsedSet)
    print("params: ", params)
    return set(params)

def getDims(s):
    ## There is a way to obtain this using ISLs C
    ## API, but sadly there is no binding for us here.
    # print ("Obtain dims from: ", self.getName())
    checkIsSet(s)
    setAsStr = str(s)
    parsedSet = IslSetParser.grammar.parse(setAsStr).unwrap()
    #print(parsedSet)
    dims = islSetGetTupleDims(parsedSet)
    return dims

def getMapRangeTupleDims(m):
    assureMap(m)
    mapAsStr = str(m)
    parsedMap = IslMapParser.grammar.parse(mapAsStr).unwrap()
    assert(len(parsedMap) == 3)
    dims = islMapGetRangeTupleDims(parsedMap)
    return dims
