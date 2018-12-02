# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 20:29:44 2018
"""

import sys
sys.path.append("D:\Lib\site-packages")
import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('D:\Clothes image\Minimal_1.png', cv2.IMREAD_COLOR)
"""
def showImage(): # 화면에 나타내는 함수
    cv2.imshow('Minimal_Look', img)
    cv2.imshow('Shrinked_Look', shrink)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
"""
# 그레이 스케일로 변환
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#노이즈 제거
img2 = cv2.GaussianBlur(gray, (3,3), 0)

laplacian = cv2.Laplacian(img2, cv2.CV_64F, 1, 0, ksize=3)
sobelx = cv2.Sobel(img2, cv2.CV_64F, 1, 0, ksize=3)
sobely = cv2.Sobel(img2, cv2.CV_64F, 0, 1, ksize=3)
    
plt.subplot(2,2,1),plt.imshow(img2,cmap = 'gray')
plt.title('Original'), plt.xticks([]), plt.yticks([])
plt.subplot(2,2,2),plt.imshow(laplacian,cmap = 'gray')
plt.title('Laplacian'), plt.xticks([]), plt.yticks([])
plt.subplot(2,2,3),plt.imshow(sobelx,cmap = 'gray')
plt.title('Sobel X'), plt.xticks([]), plt.yticks([])
plt.subplot(2,2,4),plt.imshow(sobely,cmap = 'gray')
plt.title('Sobel Y'), plt.xticks([]), plt.yticks([])

plt.show()


'''
# 행과 열
height, width = img.shape[:2]
# 이미지 축소
shrink = cv2.resize(img, (200, 200), interpolation=cv2.INTER_AREA)
# 변환된 이미지 창 출력
showImage()

# 변환된 이미지 저장
if k = 27: # esc키 누를 시 종료
    cv2.destroyAllWindow()
elif k = ord('s'): # s키 누를 시 저장 후 종료
    cv2.imwrite('Shrinked_Minimal_1.png', img)
    cv2.destroyAllWindow()    
'''
