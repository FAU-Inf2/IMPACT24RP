
class Settings():
    conf = {
        "useDefaultSched": False,
        "scopFile": "",
        "noReformat": False,
        "onlyLoopSplitting": False,
        "defaultAxiWidth": 4,
        "generateCode": False,
        "codegen": None,
        "portMap": None,
        "outFile": None,
        "emitDebugCode": False,
        "emitBurstVerify": False,
        "onlyCalcFusedOverlapGraph": False,
        "findTilingScheme": False,
        "testTilingScheme": None,
        "useUniformBlockSize": None,
        "uniformBlockSize": None,
        "blockSizes": None,
        "tileDims": None,
        "elemDims": None,
        "generateTestBench": None
    }

    settable = ["useDefaultSched", "uniformBlockSize", "scopFile", "noReformat",
                "onlyLoopSplitting", "generateCode", "portMap", "codegen",
                "outFile", "defaultAxiWidth", "emitDebugCode",
                "emitBurstVerify", "onlyCalcFusedOverlapGraph",
                "findTilingScheme", "testTilingScheme", "blockSizes",
                "tileDims", "elemDims",
                "useUniformBlockSize",
                "generateTestBench"
            ]

    @staticmethod
    def config(name):
        return Settings.conf[name]

    @staticmethod
    def set(name, value):
        if name in Settings.settable:
            Settings.conf[name] = value
        else:
            raise Exception("Not writable!")

