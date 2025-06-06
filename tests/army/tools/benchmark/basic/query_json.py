###################################################################
#           Copyright (c) 2016 by TAOS Technologies, Inc.
#                     All rights reserved.
#
#  This file is proprietary and confidential to TAOS Technologies.
#  No part of this file may be reproduced, stored, transmitted,
#  disclosed or used in any form or by any means other than as
#  expressly provided by the written permission from Jianhui Tao
#
###################################################################

# -*- coding: utf-8 -*-
import ast
import os
import re

import frame
import frame.etool
from frame.log import *
from frame.cases import *
from frame.sql import *
from frame.caseBase import *
from frame import *


class TDTestCase(TBase):
    def caseDescription(self):
        """
        taosBenchmark query test cases
        """
    def run(self):
        binPath = etool.benchMarkFile()
        os.system(
            "rm -f rest_query_specified-0 rest_query_super-0 taosc_query_specified-0 taosc_query_super-0"
        )
        tdSql.execute("drop database if exists db")
        tdSql.execute("create database if not exists db")
        tdSql.execute("use db")
        tdSql.execute("create table stb (ts timestamp, c0 int)  tags (t0 int)")
        tdSql.execute("insert into stb_0 using stb tags (0) values (now, 0)")
        tdSql.execute("insert into stb_1 using stb tags (1) values (now, 1)")
        tdSql.execute("insert into stb_2 using stb tags (2) values (now, 2)")
        cmd = "%s -f ./tools/benchmark/basic/json/taosc_query.json" % binPath
        tdLog.info("%s" % cmd)
        os.system("%s" % cmd)
        cmd = "%s -f ./tools/benchmark/basic/json/taosc_query1.json" % binPath
        tdLog.info("%s" % cmd)
        os.system("%s" % cmd)

        with open("%s" % "taosc_query_specified-0", "r+") as f1:
            for line in f1.readlines():
                queryTaosc = line.strip().split()[0]
                assert queryTaosc == "3", "result is %s != expect: 3" % queryTaosc

        with open("%s" % "taosc_query_super-0", "r+") as f1:
            for line in f1.readlines():
                queryTaosc = line.strip().split()[0]
                assert queryTaosc == "1", "result is %s != expect: 1" % queryTaosc

        # split two
        cmd = "%s -f ./tools/benchmark/basic/json/rest_query.json" % binPath
        tdLog.info("%s" % cmd)
        os.system("%s" % cmd)
        cmd = "%s -f ./tools/benchmark/basic/json/rest_query1.json" % binPath
        tdLog.info("%s" % cmd)
        os.system("%s" % cmd)

        times = 0
        with open("rest_query_super-0", "r+") as f1:
            for line in f1.readlines():
                contents = line.strip()
                if contents.find("data") != -1:
                    pattern = re.compile("{.*}")
                    contents = pattern.search(contents).group()
                    contentsDict = ast.literal_eval(contents)
                    queryResultRest = contentsDict["data"][0][0]
                    assert queryResultRest == 1, (
                        "result is %s != expect: 1" % queryResultRest
                    )
                    times += 1

        assert times == 3, "result is %s != expect: 3" % times

        times = 0
        with open("rest_query_specified-0", "r+") as f1:
            for line in f1.readlines():
                contents = line.strip()
                if contents.find("data") != -1:
                    pattern = re.compile("{.*}")
                    contents = pattern.search(contents).group()
                    contentsDict = ast.literal_eval(contents)
                    queryResultRest = contentsDict["data"][0][0]
                    assert queryResultRest == 3, (
                        "result is %s != expect: 3" % queryResultRest
                    )
                    times += 1

        assert times == 1, "result is %s != expect: 1" % times

    def stop(self):
        tdSql.close()
        tdLog.success("%s successfully executed" % __file__)


tdCases.addWindows(__file__, TDTestCase())
tdCases.addLinux(__file__, TDTestCase())
