from accesses import *

def cacheDecide(accesses):
    mnc = accesses.isMustNotCache()
    fus = accesses.isFused()
    ali = accesses.isAlignedToLoop()

    if mnc:
        return "noCache"
    if mnc == False and fus == True and ali == True:
        return "readSlab"
    if mnc == False and fus == True and ali == False:
        return "fullSlab"
    if mnc == False and fus == False and ali == True:
        return "lineSlab"
    if mnc == False and fus == False and ali == False:
        return "fullSlab"

    raise Exception("Invalid path")

def slabDecide(slabs, accs):
    cacheStrat = cacheDecide(accs)
    if cacheStrat == "readSlab":
        return slabs.getReadCacheSlab()
    if cacheStrat == "fullSlab":
        return slabs.getFullTileSlabNoDi()
    if cacheStrat == "lineSlab":
        return slabs.getWriteCacheSlab()

    return None

def writeSlabDecide(slabs, accs):
    cacheStrat = cacheDecide(accs)
    if cacheStrat == "readSlab":
        return slabs.getWriteCacheSlab()
    if cacheStrat == "lineSlab":
        return slabs.getWriteCacheSlab()
    if cacheStrat == "fullSlab":
        return slabs.getFullTileSlabNoDi()

    return None
