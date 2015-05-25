#!/usr/bin/env python
# -*- encoding: UTF-8 -*-
"""
Propose: Simple logger
Author: 'yac'
Date: 06.05.2014
"""

import logging

LOG_DIR = '/tmp/pfind.log'

def find_logger(log_name='default'):
    logger = logging.getLogger(log_name)
    hdlr = logging.FileHandler(LOG_DIR)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%y-%m-%d %H:%M:%S')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)

    return logger

