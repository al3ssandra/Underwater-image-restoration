#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 07:56:52 2017

@author: alessandra
"""

import numpy as np
import math
from guidedfilter import guided_filter
import cv2

def Background_light(normI,w=15):
    M, N, C = normI.shape #M are the rows, N are the columns, C is the bgr channel
    padwidth = math.floor(w/2)
    padded = np.pad(normI, ((padwidth, padwidth), (padwidth, padwidth),(0,0)), 'constant')
    D = np.zeros((M,N,2))
    for y, x in np.ndindex(M, N):
        D[y,x,0] = np.amax(padded[y : y+w , x : x+w , 2]) - np.amax(padded[y : y+w , x : x+w , 0])
        D[y,x,1] = np.amax(padded[y : y+w , x : x+w , 2]) - np.amax(padded[y : y+w , x : x+w , 1])
    flatD = D.reshape(M*N,2)  
    flatI = normI.reshape(M*N,3)
    searchidx = flatD.argsort(axis=0)[:1]
    searchidx = searchidx.ravel()
    return np.average(flatI.take(searchidx, axis=0), axis = 0)

def transmission_map(normI,w=15):
    M, N, C = normI.shape #M are the rows, N are the columns, C is the bgr channel
    B = Background_light(normI,w)
    padwidth = math.floor(w/2)
    padded = np.pad(normI/B, ((padwidth, padwidth), (padwidth, padwidth),(0,0)), 'constant')
    transmission = np.zeros((M,N,2))
    for y, x in np.ndindex(M, N):
        transmission[y,x,0] = 1 - np.min(padded[y : y+w , x : x+w , 0])
        transmission[y,x,1] = 1 - np.min(padded[y : y+w , x : x+w , 1])
    return transmission

def refined_t(normI,w=15):    
    tmin=0.2
    r=40
    eps=1e-3
    t = transmission_map(normI,w)
    refinedt_blue = np.maximum(t[:,:,0], tmin)
    refinedt_green = np.maximum(t[:,:,1], tmin)
    refinedt_blue = guided_filter(normI, refinedt_blue, r, eps) 
    refinedt_green = guided_filter(normI, refinedt_green, r, eps) 
    return refinedt_blue, refinedt_green

def dehazed_BG(normI,w=15):
    B = Background_light(normI,w)
    refinedt_blue,refinedt_green = refined_t(normI)
    J_blue = (normI[:,:,0] - B[0])/refinedt_blue + B[0]
    normJ_blue = (J_blue - J_blue.min()) / (J_blue.max() - J_blue.min())
    J_green = (normI[:,:,1] - B[1])/refinedt_green + B[1]
    normJ_green = (J_green - J_green.min()) / (J_green.max() - J_green.min())
    return normJ_blue, normJ_green

def RC_correction(normI,w=15):
    normJ_blue,normJ_green = dehazed_BG(normI,w)
    avgRr = 1.5 - np.average(normJ_blue.ravel()) - np.average(normJ_green.ravel())
    compCoeff = avgRr/np.average(normI[:,:,2].ravel())
    Rrec = normI[:,:,2]*compCoeff
    normRrec = (Rrec - Rrec.min()) / (Rrec.max() - Rrec.min())    
    restored = np.zeros(np.shape(normI))
    restored[:,:,0] = normJ_blue; 
    restored[:,:,1] = normJ_green; 
    restored[:,:,2] = normRrec; 
    return restored

def adaptiveExp_map(normI,w=15):   
    r=40
    eps=1e-3
    restored = RC_correction(normI,w)
    R = (restored*255).astype(np.uint8)
    I = (normI*255).astype(np.uint8)
    YjCrCb = cv2.cvtColor(R, cv2.COLOR_BGR2YCrCb)  
    YiCrCb = cv2.cvtColor(I, cv2.COLOR_BGR2YCrCb)   
    normYjCrCb = (YjCrCb - YjCrCb.min())/(YjCrCb.max() - YjCrCb.min())
    normYiCrCb = (YiCrCb - YiCrCb.min())/(YiCrCb.max() - YiCrCb.min())
    Yi = normYiCrCb[:,:,0]
    Yj = normYjCrCb[:,:,0]
    S = (Yj*Yi + 0.3*Yi**2)/(Yj**2 + 0.3*Yi**2)
    refinedS = guided_filter(normYiCrCb, S, r, eps) 
    M,N = S.shape
    rs = np.zeros((M,N,3))
    rs[:,:,0] = rs[:,:,1] = rs[:,:,2] = refinedS 
    OutputExp = restored*rs
    return (OutputExp - OutputExp.min())/(OutputExp.max() - OutputExp.min())