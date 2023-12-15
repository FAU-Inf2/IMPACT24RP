#!/usr/bin/env python3.8

from test_search_tile import SEARCH_TILE_TESTS
from test_isl_parser import ISL_PARSER_TESTS
from test_common import COMMON_TESTS
from test_align import ALIGN_TESTS
from test_card_parsing import CARD_TESTS
from test_valid_schedule import VALID_SCHEDULE_TESTS

import test_read_box_analysis as trba
import test_overlap_graph as ograph

if __name__ == '__main__':
    #for t in ISL_PARSER_TESTS: t()
    #for t in COMMON_TESTS: t()
    for t in SEARCH_TILE_TESTS: t()
    #for t in ALIGN_TESTS: t()
    #for t in CARD_TESTS: t()
    #for t in VALID_SCHEDULE_TESTS: t()
    #for t in trba.TESTS: t()
    #for t in ograph.TESTS: t()
