import re
import isl

from parsita import *

class IslCommon(ParserContext, whitespace=r'[ ]*'):
    param = reg(r'[a-zA-Z]+')
    dimId = reg(r'[a-z]+[a-z0-9]*')
    identif = reg(r'[A-Za-z]+[A-Za-z0-9]*')
    number = reg(r'-?[0-9]+')
    operator = lit("<=") | lit("<") | lit("+") | lit(">") | lit(">=")
    operand = number | dimId | param
    paramList = repsep(param, ',')
    params = '[' >> paramList << ']'
    dimList = repsep(dimExp, ',')

    func = lit("floor") | lit("ceil")
    logOp = lit("or") | lit("and")
    relOp = lit("<=") | lit(">=") | '>' | '<' | '='
    plusOp = lit("+") | lit("-")
    mulOp = lit("*") | lit("/") | lit("mod")
    powOp = lit("^")
    callExp = number | param | dimId | \
        func & '(' >> exp << ')' | '(' >> exp << ')'
    unSubExp = '-' & callExp | callExp
    powExp = unSubExp & powOp & powExp | unSubExp
    mulExp = powExp & mulOp & mulExp | powExp
    addExp = mulExp & plusOp & addExp | mulExp
    relExp = addExp & relOp & relExp | addExp
    twRelOp = addExp & relOp & addExp & relOp & addExp | relExp
    logExp = twRelOp & logOp & logExp | twRelOp

    exp = logExp
    dimExp = exp

    tuple = opt(identif) << '[' & dimList << ']'
    setEntry = tuple & opt(':' >> exp)
    mapEntry = tuple << lit("->") & tuple & opt(':' >> exp)
    polynomial = exp & opt(':' >> exp)
    constr = exp

class IslMapParser(ParserContext, whitespace=r'[ ]*'):
    grammar = opt(IslCommon.params << lit("->")) \
        << '{' >> IslCommon.mapEntry << '}'

class IslUnionMapParser(ParserContext, whitespace=r'[ ]*'):
    grammar = opt(IslCommon.params << lit("->")) \
        << '{' >> repsep(IslCommon.mapEntry, ';') << '}'

class IslSetParser(ParserContext, whitespace=r'[ ]*'):
    grammar = opt(IslCommon.params << lit("->")) & \
        '{' >> IslCommon.setEntry << '}'

class IslPointParser(ParserContext, whitespace=r'[ ]*'):
    grammar = opt(IslCommon.params << lit("->")) << \
        '{' >> IslCommon.setEntry << '}'

class IslUnionSetParser(ParserContext, whitespace=r'[ ]*'):
    grammar = opt(IslCommon.params << lit("->")) << '{' \
        >> repsep(IslCommon.setEntry, ';') << '}'

class IslCardParser(ParserContext, whitespace=r'[ ]*'):
    entry = IslCommon.polynomial
    entryList = repsep(entry, ";")
    grammar = opt(IslCommon.params >> lit("->")) \
        >> '{' >> entryList << '}'


def parseCard(card):
    assert(isinstance(card, isl.union_pw_qpolynomial) or \
           isinstance(card, isl.pw_qpolynomial))

    # ISL sometimes leaves out the * operator
    # For example ... 64 * SIZE ... will sometimes
    # be shortened to 64SIZE. We solve this with a hack
    cardStr = str(card)

    regex = r'(([0-9]+)([a-zA-Z][A-Za-z0-9]*))'
    p = re.compile(regex)
    patterns = p.findall(cardStr)
    for full, fst, snd in patterns:
        replacement = fst + " * " + snd
        print("WARNING: Will now replace %s to %s in this card: [%s]"%
              (full, replacement, cardStr))
        cardStr = cardStr.replace(full, replacement)

    res = IslCardParser.grammar.parse(cardStr).unwrap()
    return res
