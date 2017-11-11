#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 11:31:37 2017

@author: alessandra
"""
import argparse
from functools import partial
import cv2
from util import get_filenames
from BGDehaze import adaptiveExp_map

def generate_results(src, dest, generator):
    print('processing', src + '...')
    I = cv2.imread(src)
    normI = (I - I.min()) / (I.max() - I.min())
    restored = generator(normI)
    cv2.imwrite(dest, restored*255)
    print('saved', dest)

def main():
    filenames = get_filenames()
    parser = argparse.ArgumentParser(description = 'Underwater Image Restoration by Blue-Green Channels Dehazing and Red Channel Correction')
    parser.add_argument("-i", "--input", type=int,
                        choices=range(len(filenames)),
                        help="index for single input image: {} corresponds to indexes {}".format(filenames[0][0],list(range(len(filenames)))))
    parser.add_argument("-w", "--window", type=int, default=15,
                        help="window size of dark channel")
    args = parser.parse_args()
    
    src,dest = filenames[args.input]
    generate_results(src, dest, partial(adaptiveExp_map, w=args.window))

if __name__ == '__main__':
    main()