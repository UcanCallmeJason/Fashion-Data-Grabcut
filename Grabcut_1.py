# -*- coding: utf-8 -*-
"""
Created on Sun Nov 18 17:02:28 2018
Grabcut을 이용한 배경제거
@author: 송시찬
"""

import numpy as np
import sys
sys.path.append("D:\Lib\site-packages")
import cv2

#픽셀 컬러 임계값 설정
BLUE, GREEN, RED, BLACK, WHITE = (255,0,0), (0,255,0), (0,0,255), (0,0,0), (255,255,255)
DRAW_BG = {'color':BLACK, 'val':0} #배경 검은선으로 그리기
DRAW_FG = {'color':WHITE, 'val':1} #전경 하얀선으로 그리기

rect = (0, 0, 1, 1) #전경객체의 직사각형의 좌표
drawing = False
rectangle = False
rect_over = False
rect_or_mask = 100 # 배경 / 전경의 영역을 지정하는 마스크
value = DRAW_FG
thickness = 3

# 마우스로 추출 설정하는 함수
def onMouse(event, x, y, flags, param):
    # 전역 변수 선언
    global ix, iy, img, img2, drawing, value, mask, rectangle
    global rect, rect_or_mask, rect_over
    
    # R키를 누르면 모든 작업을 리셋하고 처음으로 돌아감.
    if event == cv2.EVENT_RBUTTONDOWN:
        rectangle = True
        ix, iy = x, y
        
    elif event == cv2.EVENT_MOUSEMOVE:
        if rectangle:
            img = img2.copy()
            cv2.rectangle(img, (ix, iy), (x, y), RED, 2)
            rect = (min(ix, x), min(iy, y), abs(ix-x), abs(iy-y))
            rect_or_mask = 0
            
    elif event == cv2.EVENT_RBUTTONUP:
        rectangle = False
        rect_over = True
        
        cv2.rectangle(img, (ix, iy), (x, y), RED, 2)
        rect = (min(ix, x), min(iy, y), abs(ix-x), abs(iy-y))
        rect_or_mask = 0
        print("n:적용하기")
        
    if event == cv2.EVENT_LBUTTONDOWN:
        if not rect_over:
            print('마우스 왼쪽 버튼을 누른채로 전경이 되는 부분을 선택하세요.')
        else:
            drawing = True
            cv2.circle(img, (x, y), thickness, value['color'], -1)
            cv2.circle(mask, (x, y), thickness, value['val'], -1)
            
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            cv2.circle(img, (x, y), thickness, value['color'], -1)
            cv2.circle(mask, (x, y), thickness, value['val'], -1)
            
    elif event == cv2.EVENT_LBUTTONUP:
        if drawing:
            drawing = False
            cv2.circle(img, (x, y), thickness, value['color'], -1)
            cv2.circle(mask, (x, y), thickness, value['val'], -1)
            
    return

# grabcut 알고리즘
def grabcut():
    
    # 전역변수 선언
    global ix, iy, img, img2, drawing, value, mask, rectangle
    global rect, rect_or_mask, rect_over
    
    # 입력이미지 읽어오기
    img = cv2.imread('D:\Clothes image\Minimal_1.png')
    img2 = img.copy() # mask를 만들기 위해 복사본 만듬.
    
    mask = np.zeros(img.shape[:2], dtype=np.uint8)
    output = np.zeros(img.shape, np.uint8)
    
    cv2.namedWindow('input')
    cv2.namedWindow('output')
    cv2.setMouseCallback('input', onMouse, param=(img, img2))
    cv2.moveWindow('input', img.shape[1]+10, 90)
    
    print('오른쪽 마우스 버튼을 누르고 영역을 지정한 후 n을 누르세요.')
    
    while True:
        cv2.imshow('output', output)
        cv2.imshow('input', img)
        
        # '1'버튼을 누르면 전경 객체로 살리고 싶은 부분 흰색 마킹 가능. 
        k = cv2.waitKey(1) & 0xFF
        
        if k == 27:
            break
        
        # '0'버튼을 누르면 지우고 싶은 배경 부분에 검은색 마킹 가능.
        if k == ord('0'):
            print('왼쪽 마우스로 제거할 부분을 표시한 후 n을 누르세요.')
            value = DRAW_BG # 검은 마킹 값
        
        # 'r'버튼을 누르면 모든 작업이 리셋됨. (변수들 맨처음으로 초기화) 
        elif k == ord('r'):
            print('리셋합니다.')
            rect = (0, 0, 1, 1)
            drawing = False
            rectangle = False
            rect_or_mask =100
            rect_over = False
            value = DRAW_FG
            img = img2.copy()
            mask = np.zeros(img.shape[:2], dtype=np.uint8)
            output = np.zeros(img.shape, np.uint8)
            print('0:제거배경선택, 1:복원전경선택, n:적용하기, r:리셋')
        
        # n키 누를시 그랩컷 알고리즘 실행 후 출력창에 디스플레이함.
        elif k == ord('n'):
            bgdModel = np.zeros((1, 65), np.float64) #알고리즘에 의해 내부적으로 사용되는 배열.
            fgdModel = np.zeros((1, 65), np.float64)
            
            # GC_INIT 인자는 상자와 터치업 스트로크 방식을 결정하는 모드.
            if rect_or_mask == 0:
                cv2.grabCut(img2, mask, rect, bgdModel, fgdModel, 1, cv2.GC_INIT_WITH_RECT)
                rect_or_mask = 1
            
            elif rect_or_mask == 1:
                cv2.grabCut(img2, mask, rect, bgdModel, fgdModel, 1, cv2.GC_INIT_WITH_MASK)
            
            print('0:제거배경선택, 1:복원전경선택, n:적용하기, r:리셋')
        
        mask2 = np.where((mask==1) + (mask==3), 255, 0).astype('uint8')
        
        # cv2.bitwise_and 연산자는 둘다 0이 아닌 경우만 값을 통과 시킴.
        # 즉 mask영역 이외는 모두 제거됨.
        output = cv2.bitwise_and(img2, img2, mask=mask2)
    cv2.destroyAllWindows()
    
grabcut()
    
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            