from settings import *

def getUniformBlockSizes(dimlist, blockSize):
    return { d : blockSize for d in dimlist }

def getIndivBlockSizes(dimlist, l):
    assert(len(dimlist) == len(l))
    return { d : bs for (d, bs) in zip(dimlist, l) }

def getBlockSizes(dimlist):
    if Settings.config("useUniformBlockSize"):
        ubs = Settings.config("uniformBlockSize")
        return getUniformBlockSizes(dimlist, ubs)
    else:
        bs = Settings.config("blockSizes")
        assert(len(dimlist) == len(bs))
        return getIndivBlockSizes(dimlist, bs)

def getLsdBlockSize(dimlist):
    bs = getBlockSizes(dimlist)
    return bs[dimlist[-1]]
