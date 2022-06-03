########book_name
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
book_name = input("어떤 책을 검색하시겠습니까? ")
url = f'http://www.yes24.com/Product/Search?domain=BOOK&query={book_name}'

res = requests.get(url)
index = 1
user_dic = {}
if res.status_code == 200:
    soup=BeautifulSoup(res.text,'lxml')
    links = soup.select(".gd_name")
    #print(links)

    for link in links:
        title=link.text #태그 안 텍스트
        specific_url = link.attrs['href']   #href 속성값
        book_code = specific_url[15:]
        print(f"{index}번")
        print(title)
        print(book_code)
        user_dic[index] = int(book_code)    #dict에 넣기
        index = index+1
        print()
        if (index ==6): 
            break
book_num = int(input("몇 번 책을 선택하시겠습니까? (숫자만 입력) "))
book_num = user_dic[book_num]

###########book_review
from urllib.request import urlopen
#from bs4 import BeautifulSoup

book_num = 74419916  #책 고유 숫자 입력

review_list = []   
try:
    for page in range(1,11):    #page를 순환하며 리뷰 크롤링 : p1~p10
        url = f'https://www.yes24.com/Product/communityModules/GoodsReviewList/{book_num}?Type=ALL&Sort=1&PageNumber={page}'
        html = urlopen(url)
        soup = BeautifulSoup(html,'html.parser')
        links = soup.select(".review_cont")
        #print(links)
        for link in links:
            review = link.text
            #print(review)
            if "더보기" in review:
                pass
            else:
                review_list.append(review)
        
    #print(review_list)    
except:
    pass

with open(f'{book_num}_yes24_book.txt','w',encoding='utf-8') as f:    
    for single_review in review_list:
        f.write(single_review+'\n')

del review_list # 메모리 절약을 위한 리스트 삭제

############book_frequency
from konlpy.tag import Twitter
from collections import Counter

def get_tags(text, ntags=500):
    spliter = Twitter()
    pos = spliter.pos(text)
    words=[]
    for li in pos:
        if li[1]=='Noun' or li[1] == 'Adjective':
            words.append(li[0])
    count = Counter(words)
    return_list = []

    for n, c in count.most_common(ntags):
        temp = {'tag': n, 'count': c}
        return_list.append(temp)

    return return_list

def frequency(title):
    global text_file_name #
    text_file_name = "%s.txt"%title
    noun_count = 500
    output_file_name = "%s_count.txt"%title
    try: 
        open_text_file = open(text_file_name, 'r', -1, "utf-8")
        text = open_text_file.read()
    except:
        print("리뷰 파일이 없습니다")
        return
    tags = get_tags(text, noun_count)
    open_text_file.close()
    open_output_file = open(output_file_name, 'w', -1, "utf-8")

    for tag in tags:
        noun = tag['tag']
        count = tag['count']
        open_output_file.write('{} {}\n'.format(noun, count))

    open_output_file.close()


frequency(str(book_num)+"_yes24_book")
print(text_file_name)
################cloud
import pytagcloud
import random
import math

file_pos = open(str(book_num)+"_yes24_book_count.txt",'r', -1, "utf-8")
word_1 = []
word_n = []
lines1 = file_pos.readlines()
for line in lines1:
    splited = line.split(' ')
    word_1.append(splited[0])
    word_n.append(int(splited[1]))
file_pos.close()

#print(word_1)

taglist = []

r = lambda: random.randint(0,255)
# 글씨의 랜덤색깔
color = lambda: (int(r()), int(r()), int(r()))
#print(color())
list_len = len(word_1)
size=183/list_len
for i in range(0, list_len):
    taglist.append({'color': color(), 'size': int(float(int(word_n[i])*4*size) + 20), 'tag': '%s' % word_1[i]}) 
    #크기가 많은순으로 지수함수적으로? 작아졌으면 좋겠음

#print(taglist)  #
pytagcloud.create_tag_image(taglist,'wordcloud.jpg', size=(1000,500), fontname='malgunbd', rectangular=False)
