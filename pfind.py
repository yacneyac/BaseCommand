#!/usr/bin/env python
# -*- encoding: UTF-8 -*-
"""
Propose: Implemented simple searching files on python
Author: 'yac'
Date: 06.05.2014
"""

import os, sys
import fnmatch
from re import compile
import optparse
from time import time

from commands import BaseFind
from logger import find_logger
from f_exception import FException

B = 1
KB = 1024
MB = 1024**2  # 1048576
GB = 1024**3  # 1073741824
SIZE_MAP = {'b': B, 'k': KB, 'M': MB, 'G': GB}
SIZE_PATTERN = ur'^(?P<PREFIX>[+-]?)(?P<SIZE>\d+)(?P<SUFFIX>[bkMG]?)$'

SEC = 0
MIN = 60
HOUR = 60 * 60  # 3600
DAY = 60 * 60 * 24  # 86400
DATE_MAPPING = {'s': SEC, 'm': MIN, 'H': HOUR, 'D': DAY}
DATE_PATTERN = ur'^(?P<PREFIX>[+-]?)(?P<DATE>\d+)(?P<SUFFIX>[smHD]?)$'

class Find(BaseFind):
    """ Implemented find on python """
    def __init__(self):
        self.log = find_logger('PFIND')

    def initial(self):
        """ Parse input options """
        usage = 'search for files in a directory hierarchy \n '\
                'SYNOPSIS find [path...] [expression]'

        p = optparse.OptionParser(usage=usage)
        p.add_option('-n', '--name', action='store', dest='fname', help = 'Find files by name')
        p.add_option('-s', '--size', action='store', dest='fsize', help = 'Find files by size.'
                                                                          'Use prefix "+" - more than, "-" - less than.'
                                                                          'Use suffix "b", "k", "M", "G". Default "b"')
        p.add_option('-m', '--mtime', action='store', dest='fmtime', help = 'Find files by last modify date.'
                                                                            'Use prefix "+" or "-".'
                                                                            'Use suffix "s", "m", "H", "D". Default "D"')

        opts, args = p.parse_args()

        if len(sys.argv) < 2 or not args:
            p.error('Input correct number of arguments! Use -h or --help to call help')

        self.search_path = ''
        if len(args) != 0:
            self.search_path = args[0]
            if not os.path.exists(self.search_path):
                self.log.info('Path <%s> not found!' % self.search_path)
                print 'Path <%s> not found!' % self.search_path
                return

        self.fname = opts.fname
        if not self.fname:
            self.fname = '*'
            opts.fname = '*'

        self.log.info('Searching files in <%s> by filter <%s>' % (self.search_path, opts))
        self.search_file(self.search_path, self.fname, opts.fsize, opts.fmtime)

    def search_file(self, search_path, fname, fsize=None, fmtime=None):
        """ Find files by filter
        @param search_path: Path for found files
        @param fsize: file's size
        @param fmtime: file's modify date

        return list of files
        """
        try:
            file_list = []
            for root, dirs, files in os.walk(search_path):
                for filename in fnmatch.filter(files, fname):
                    self.full_path_file = os.path.join(root, filename)

                    try:
                        if self.check_file_attributes(self.full_path_file, fsize=fsize, fmtime=fmtime):
                            self.log.info('Found: %s' % self.full_path_file)
                            file_list.append(self.full_path_file)
                            print self.full_path_file

                    except OSError, err:
                        if err.errno == 13:
                            self.log.info('%s: %s' %(err.filename, err.strerror))
                            print err.filename, ':', err.strerror
                        else:
                            self.log.error('%s', str(err))
                            raise

            return file_list
        except Exception, err:
            self.log.error('Error while searching files! <%s>' % str(err))
            raise FException('Error while searching files! See log.')

    def check_file_attributes(self, full_path_file, fsize=None, fmtime=None):
        """ Check files attributes
        @param full_path_file: Full path to file
        @param fsize: file's size
        @param fmtime: file's modify date

        return True if search criteria match otherwise False
        """
        try:
            if fsize:
                regex = compile(SIZE_PATTERN)
                matched = regex.match(fsize)
                if matched:
                    prefix = matched.group('PREFIX')
                    data = int(matched.group('SIZE'))  * SIZE_MAP.get(matched.group('SUFFIX'), B)

                    if prefix == '-':
                        if os.path.getsize(full_path_file) < data:
                            return True
                    elif prefix == '+':
                        if os.path.getsize(full_path_file) > data:
                            return True
                    elif prefix == '':
                        if os.path.getsize(full_path_file) == data:
                            return True

                self.log.info('File <%s> is not meeting the search criteria' % full_path_file)
                return False
            elif fmtime:
                regex = compile(DATE_PATTERN)
                matched = regex.match(fmtime)
                if matched:
                    syf = matched.group('SUFFIX')
                    data = (time() - int(matched.group('DATE')) * DATE_MAPPING.get(syf, DAY))
                    prefix = matched.group('PREFIX')

                    if prefix == '-':
                        if os.path.getmtime(full_path_file) < data:
                            return True
                    elif prefix == '+':
                        if os.path.getmtime(full_path_file) > data:
                            return True
                    elif prefix == '':
                        if os.path.getmtime(full_path_file) == data:
                            return True

                self.log.info('File <%s> is not meeting the search criteria' % full_path_file)
                return False
            elif full_path_file:
                return True

            self.log.info('File <%s> is not meeting the search criteria' % full_path_file)
            return False
        except Exception, err:
            self.log.error('Error while checking file <%s> attributes! <%s>' % (full_path_file, str(err)))
            raise

if __name__ == '__main__':
    f = Find()
    f.initial()