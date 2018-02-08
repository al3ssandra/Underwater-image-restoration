#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 12:30:20 2017

@author: alessandra
"""
import os
import glob

SRC_DIR = 'img'
DEST_DIR = 'result'

def get_filenames():
    file_dir = os.path.dirname(os.path.realpath(__file__))
    src_path = os.path.join(file_dir, SRC_DIR)
    img_files = glob.glob(src_path + '/*.jpg')
    filenames = []
    for file in img_files:
        drive, tail = os.path.split(file)
        filenames.append((os.path.join(SRC_DIR, tail),os.path.join(DEST_DIR, tail)))
    return filenames