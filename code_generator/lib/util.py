import functools
import subprocess

def flatten(L):
    return [ v for pair in L for v in pair ]

def wrapInListIfNotList(e):
    if isinstance(e, list): return e
    else: return [e]

def allEq(L):
    return all([ L[0] == l for l in L ])

def allIntConvertible(L):
    return all([ l.isnumeric() for l in L ])

def paren(s):
    return "(" + s + ")"

def brace(s):
    return "{" + s + "}"

def brackWrap(l):
    return [ "[%s]" % (e) for e in l ]

def eJoin(l):
    return "".join(l)

def nlJoin(L):
    return "\n".join(L)

def cmJoin(L):
    return ", ".join(L)

def scJoin(L):
    return "; ".join(L)

def andJoin(L):
    return " and ".join(L)

def rmTick(s):
    return s.replace("'", "")

def sanitizeForPath(s):
    return (s.replace("'", "").replace(" ", "_")
            .replace("[", "_").replace(":", "_")
            .replace(",", "_").replace("]", "_"))

def setUnion(S):
    SetUnion = lambda a, b: set.union(a, b)
    return functools.reduce(SetUnion, S)

def logAnd(*argv):
    return lambda x: functools.reduce(
        lambda l, r: l and r, map(lambda f: f(x), argv))

def mapReverse(m):
    return { m[k] : k for k in m }

def clangFormat(inp):
    output = subprocess.run(["clang-format"],
                            input = inp.encode(),
                            capture_output = True)

    if output.returncode == 0:
        return output.stdout.decode()
    else:
        print("Output: {}".format(output.stderr.decode()))
        raise Exception("Reformat failed")

NL = "\n"

