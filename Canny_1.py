# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 17:56:47 2018

@author: 송시차니
"""

import sys
sys.path.append("D:\Lib\site-packages")
import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('D:\Clothes image\Minimal_1.png', cv2.IMREAD_GRAYSCALE)
def canny():
    edge1 = cv2.Canny(img, 100, 100) # 강한 외곽만을 검출
    edge2 = cv2.Canny(img, 100, 130)
    edge3 = cv2.Canny(img, 100, 120)

    cv2.imshow('Original', img)
    cv2.imshow('Canny Edge1', edge1)
    cv2.imshow('Canny Edge2', edge2)
    cv2.imshow('Canny Edge3', edge3)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
canny()
