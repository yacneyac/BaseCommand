#!/usr/bin/env python
# -*- encoding: UTF-8 -*-
"""
Propose: Unit test for find
Author: 'yac'
Date: 07.05.2014
"""

import unittest
import os
import subprocess
from time import localtime

from pfind import Find, FException

TEST_PATH = '/tmp/test_yac'

def create_test():
    subprocess.call(("mkdir -p %s" % os.path.join(TEST_PATH, "test_folder1")).split())
    subprocess.call(("mkdir -p %s" % os.path.join(TEST_PATH, "test_folder2")).split())
    #file: size 100k
    subprocess.call(("dd if=/dev/zero of=%s bs=1k count=100" % os.path.join(TEST_PATH, "test_folder1", "test1.txt")).split())
    #file: size 200k
    subprocess.call(("dd if=/dev/zero of=%s bs=1k count=200" % os.path.join(TEST_PATH, "test_folder2", "test2.txt")).split())

    now = localtime()
    mod_date = "".join([str(now.tm_year), "%02d" % now.tm_mon, "%02d" % now.tm_mday,
                        "%02d" % (now.tm_hour - 1), "%02d" % now.tm_min])
    #file: md 1 hour
    subprocess.call(("touch -m -t %s %s" % (mod_date, os.path.join(TEST_PATH, "test_folder1", "test3.txt"))).split())

    mod_date = "".join([str(now.tm_year), "%02d" % now.tm_mon, "%02d" % now.tm_mday,
                        "%02d" % (now.tm_hour - 2), "%02d" % now.tm_min])
    #file: md 2 hour
    subprocess.call(("touch -m -t %s %s" % (mod_date, os.path.join(TEST_PATH, "test_folder2", "test4.doc"))).split())


class TestFind(unittest.TestCase):


    def test_01_find_files(self):
        p_find = Find()

        #find by name
        check = ['%s/test_folder1/test1.txt' % TEST_PATH,
                 '%s/test_folder1/test3.txt' % TEST_PATH,
                 '%s/test_folder2/test2.txt' % TEST_PATH]
        self.assertEqual(check, p_find.search_file(TEST_PATH, '*.txt'))

        #find by size
        check = ['%s/test_folder2/test2.txt' % TEST_PATH]
        self.assertEqual(check, p_find.search_file(TEST_PATH, '*', fsize='+100k'))

        check = ['%s/test_folder1/test1.txt' % TEST_PATH,
                 '%s/test_folder1/test3.txt' % TEST_PATH,
                 '%s/test_folder2/test4.doc' % TEST_PATH,
                 '%s/test_folder2/test2.txt' % TEST_PATH]
        self.assertEqual(check, p_find.search_file(TEST_PATH, '*', fsize='-1M'))

        #find by date. not modify
        check = ['%s/test_folder1/test3.txt' % TEST_PATH,
                 '%s/test_folder2/test4.doc' % TEST_PATH]
        self.assertEqual(check, p_find.search_file(TEST_PATH, '*', fmtime='-1H'))
        #find by date. modify
        check = ['%s/test_folder1/test1.txt' % TEST_PATH,
                 '%s/test_folder2/test2.txt' % TEST_PATH]
        self.assertEqual(check, p_find.search_file(TEST_PATH, '*', fmtime='+1m'))

        # check error
        self.assertRaises(FException, p_find.search_file, None, '*', fmtime='+1m')

        if os.path.exists(TEST_PATH):
            subprocess.call(("rm -rf %s" % TEST_PATH).split())

if __name__ == '__main__':
    create_test()
    unittest.main()
