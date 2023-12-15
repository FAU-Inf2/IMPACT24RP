from isl_parser import *
from returns import result

def runParser(parser, string):
    res = parser.parse(string)
    if isinstance(res, result.Failure):
        print(res)
        raise Exception("Parsing Failure")
    else:
        print(res.unwrap())

def testIslSet():
    TS0 = "[SIZE] -> { S1[i, j] : 0<=i<SIZE and 0<=j<SIZE }"
    TS1 = "[SIZE] -> { S1[i, j, k] : 0<=i<SIZE and 0<=j<SIZE }"
    TS2 = "[SIZE] -> { [i, j, k] : 0<=i<SIZE and 0<=j<SIZE }"

    try:
        for i in [TS0, TS1, TS2]:
            runParser(IslSetParser.grammar, i)
    except Exception as e:
        print(e)
        exit(1)

def testIslUnionSet():
    TS0 = "[SIZE] -> { S1[i, j] : 0<=i<SIZE and 0<=j<SIZE }"
    TS1 = "[SIZE] -> { S1[i, j, k] : 0<=i<SIZE and 0<=j<SIZE }"
    TS2 = "[SIZE] -> { S1[i, j, k] : 0<=i<SIZE and 0<=j<SIZE; S2[i, k, 5] }"
    TS3 = "[SIZE] -> { S1[i, j - 1, k + 1] : 0<=i<SIZE and 0<=j<SIZE; S2[i, k, 5] }"
    Inputs = [TS0, TS1, TS2, TS3]

    try:
        for i in Inputs:
            runParser(IslUnionSetParser.grammar, i)

    except Exception as e:
        print(e)
        exit(1)

def testDeconstruct():
    TS0 = "[SIZE] -> { S1[i, j] : 0<=i<SIZE and 0<=j<SIZE }"
    TS1 = "[SIZE] -> { S1[i, j, k] : 0<=i<SIZE and 0<=j<SIZE }"
    TS2 = "[SIZE] -> { S1[i, j, k] : 0<=i<SIZE and 0<=j<SIZE; S2[i, k, 5] }"
    TS3 = "[SIZE] -> { S1[i, j - 1, k + 1] : 0<=i<SIZE and 0<=j<SIZE; S2[i, k, 5] }"

def testCard():
    TS0 = """ 
    [SIZE, tk] -> { 68 : (-1 + tk) mod 64 = 0 and 0 < tk <= -66 + SIZE; ((1 - tk) + 4 * floor((192 + 64SIZE)/256)) : (-1 + tk) mod 64 = 0 and -64 + SIZE <= tk <= SIZE; 68 : tk = -65 + SIZE and (-
2 + SIZE) mod 64 = 0 }
    """
    uq = isl.union_pw_qpolynomial(TS0)
    print(uq)

    parsed = parseCard(uq)
    print(parsed)

ISL_PARSER_TESTS = [testIslSet, testIslUnionSet, testCard]
