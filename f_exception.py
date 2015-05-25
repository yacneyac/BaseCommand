#!/usr/bin/env python
# -*- encoding: UTF-8 -*-
"""
Propose: Base exception for find
Author: 'yac'
Date: 06.05.2014
"""


class FException(Exception):
    """ Simple exception for find """
    def __str__(self):
        return '[PFind] %s' % Exception.__str__(self)
