# -*- coding: utf-8 -*-
"""
Created on Sun Nov 18 17:02:28 2018
Grabcut을 이용한 배경제거
@author: 송시찬
"""
# 해당 소스의 사용방법은 github에 기재해두었음.

import numpy as np
import sys
sys.path.append("D:\Lib\site-packages")
import cv2
import os

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

import glob

# grabcut 알고리즘
def grabcut():
    
    # 전역변수 선언
    global ix, iy, img, img2, drawing, value, mask, rectangle
    global rect, rect_or_mask, rect_over
    number = 1 # 최종 저장된 사진의 순번을 위해
    
    # 폴더의 파일 리스트 읽어오기(jpg 파일을 읽어옴)
    path_dir = 'D:\Clothes image\Minimal_Look\Train/*.jpg'
    file_list = glob.glob(path_dir)
    for file in file_list:
        # 입력이미지 읽어오기
        img = cv2.imread(file)
        if img is None: # 사진이 없을경우 종료 / 외부 루프는 종료하지 않으므로 다음 디렉토리로 넘아감
            break
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
        
            # 키보드 입력을 1밀리세컨드 기다림. 
            k = cv2.waitKey(1) & 0xFF
            
            #esc 누를 시 다음 사진으로 작업이 넘어감.
            if k == 27:
                cv2.destroyAllWindows()
                break
            
            # '0'버튼을 누르면 지우고 싶은 배경 부분에 검은색 마킹 가능.
            if k == ord('0'):
                print('왼쪽 마우스로 제거할 부분을 표시한 후 n을 누르세요.')
                value = DRAW_BG # 검은 마킹 값
            
            # '1'버튼을 누르면 살리고 싶은 전경 부분에 하얀 마킹 가능.
            if k == ord('1'):
                print('왼쪽 마우스로 제거할 부분을 표시한 후 n을 누르세요.')
                value = DRAW_FG # 하얀 마킹 값
        
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
            
            # 배경이 제거된 사진을 Grabcuted 폴더에 저장
            if k == ord('s'): # 's' key
                print('s키를 입력하면 배경제거된 사진을 저장합니다.')
                #save_path의 경로는 자신이 원하는 곳으로 바꾸어준다.
                save_path = 'D:\Clothes image\Minimal_Look\Grabcuted'
                cv2.imwrite(os.path.join(save_path, 'Grabcuted'+ str(number) +'.jpg'),output)
                number += 1 #사진 하나를 저장하면 그다음부터 하나씩 카운트.
                
grabcut()
    
