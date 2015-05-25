#!/usr/bin/env python
# -*- encoding: UTF-8 -*-
"""
Propose: Base command
Author: 'yac'
Date: 
"""


class BaseFind(object):
    """ Base class for searching files """

    def search_file(self, search_path, fname, fsize=None, fmtime=None):
        """ Implement in inheritance class """
        pass

    def check_file_attributes(self, filename, fsize=None, fmtime=None):
        """ Implement in inheritance class """
        pass