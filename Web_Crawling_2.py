# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 22:30:08 2018
웹크롤링2 버전
@author: user
"""

# 인스타그램 사진 저장하기(원하는 사진이 있는 주소 복사하여 사용)
# 게시글 선택해서 있는 최초 사진 하나만 가능. 한 게시글에 있는 여러 사진 불가
# requests, beautifulsoup4, lxml 설치 필요    >>> pip install ~

import requests, os
from bs4 import BeautifulSoup
import lxml

def insta_save():
    while True:
        url = input("\n** 원하는 사진이 있는 인스타그램 주소를 복사하여 붙여넣은 후 ENTER를 눌려주세요.\n"
        "끝내시려면 언제든지 0을 입력해주세요: \n>>> ")
        if url == "0":
            break
        
        while url != "0":
            print()
            question = input("** 입력하신 주소는 (%s) 입니다. \n맞으면 Y, "
            "틀리면 N을 입력해주세요: \n>>> " % url)
            if question.upper() == 'Y':
                response = requests.get(url).text
                soup = BeautifulSoup(response, 'lxml')
                # 사진 태그 주소 찾기
                for tag in soup.select('meta[property*=image]'):
                    image_url = tag['content']
                # 사진 raw 파일과 파일명 받기
                pic_response = requests.get(image_url).content
                file_name = os.path.basename(image_url)
                # 사진 저장하기
                with open(file_name, 'wb') as f:
                    f.write(pic_response)
                break
            elif question.upper() == "N":
                print()
                break    
            elif question == "0":
                return None
            else:
                continue

if __name__ == "__main__":
    insta_save()