from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen

from konlpy.tag import Twitter
from collections import Counter

import pytagcloud

############################################################ 책 검색 부분
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
        print(f"=============={index}번===============")
        print(title)
        print(book_code)
        user_dic[index] = int(book_code)    #dict에 넣기
        index = index+1
        print()
        if (index ==6):
            break
book_num = int(input("몇 번 책을 선택하시겠습니까? (숫자만 입력) "))
book_num = user_dic[book_num]

############################################################리뷰 크롤링
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

############################################################형태소 분석
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
    global text_file_name 
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

############################################################긍정/부정 단어 비교
def open_review(title):
    doc = ''
    file = open('%s_count.txt'%title, 'r', encoding='utf-8')
    lines = file.readlines()
    for line in lines:
        doc += line
    file.close()

    # 빈도수를 2차원 배열로 저장
    doc = doc.split('\n')
    list = []
    doc_len = range(0, len(doc) - 1)
    for i in doc_len:
        list.append(doc[i].split(' '))
    
    return list

def open_pos(): #긍정사전 불러오기
    file_pos = open('긍정단어.txt','r', -1, "utf-8")
    positive = []
    lines1 = file_pos.readlines()
    for line in lines1:
        positive.append(line.replace("\n", ""))
    file_pos.close()
    return positive

def open_neg(): #부정사전 불러오기
    file_neg = open('부정단어.txt','r', -1, "utf-8")
    negative = []
    lines2 = file_neg.readlines()
    for line in lines2:
        negative.append(line.replace("\n", ""))
    file_neg.close()
    return negative

def print_senti(title):
    list = open_review(title)
    positive = open_pos()
    negative = open_neg()
    pos = 0
    neg = 0
    list_len = len(list)
    for i in range(0, list_len):
        if list[i][0] in positive:
            pos += int(list[i][1])
        elif list[i][0] in negative:
            neg += int(list[i][1])


print_senti(str(book_num)+"_yes24_book")


############################################################ word cloud 생성
def cloud(title):
    list = open_review("%s"%title)

    try:
        positive = open_pos()
        negative = open_neg()
    except:
        print("wrong")
    taglist = []


    list_len = len(list)
    pos_word_l=[]
    pos_word_n=[]
    neg_word_l = []
    neg_word_n = []
    #neg_list=[]
    size=float(0)
    for i in range(0, list_len):
        if list[i][0] in positive:
            pos_word_l.append(list[i][0])
            pos_word_n.append(list[i][1])
            size+=float(list[i][1])
        if list[i][0] in negative:
            neg_word_l.append(list[i][0])
            neg_word_n.append(list[i][1])
            size += float(list[i][1])

    size=183/size
    list_len = len(pos_word_l)
    for i in range(0, list_len):
        taglist.append({'color': (70, 65, 217), 'size': int(float(int(pos_word_n[i])*4*size) + 20), 'tag': '%s' % pos_word_l[i]})
    list_len = len(neg_word_l)
    for i in range(0, list_len):
        taglist.append({'color': (255, 0, 0), 'size': int(float(int(neg_word_n[i])*4 * size) + 20), 'tag': '%s' % neg_word_l[i]})
    pytagcloud.create_tag_image(taglist,'wordcloud.jpg', size=(1000,500), fontname='malgunbd', rectangular=False)

    
cloud(str(book_num)+"_yes24_book")
