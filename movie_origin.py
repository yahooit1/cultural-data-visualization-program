from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen

from konlpy.tag import Okt
from collections import Counter

import pytagcloud

import sqlite3

con, cur = None, None

def insertData() :
    con = sqlite3.connect("D:/sqlite/Test")##개인설정으로 바꿔야함.
    cur = con.cursor()
    data1 = DB_dic['name']
    data2 = str(DB_dic['score'])
    data3 = str(DB_dic['number'])
    print(type(data1), type(data2), type(data3))
    sql = "INSERT INTO t4 VALUES('"+data1+"','"+data2+"','"+data3+"');"
    cur.execute(sql)
    con.commit()
    con.close()

def printData() :
    con = sqlite3.connect("D:/sqlite/Test")##개인설정으로 바꿔야함.
    cur = con.cursor()
    sql = "SELECT * FROM t4 ORDER BY score DESC;"
    cur.execute(sql)
    result = cur.fetchall()
    i=0
    for data in result:
        da_li = str(data).split(', ')
        print("%s %s" % (str(da_li[0])[1:], da_li[1]))
        i+=1
        if i>5: break

    con.close()

############################################################영화 검색 부분
movie = input("어떤 영화를 검색하시겠습니까? ")
url = f'https://movie.naver.com/movie/search/result.naver?query={movie}&section=all&ie=utf8'
if movie == '0' :
    printData()
    exit()
res = requests.get(url)
index = 1
user_dic = {}
point_dic = []
name_list = ['', ]
score_list = ['', ]
DB_dic={}

if res.status_code == 200:  #HTTP status code가 OK일 때
    soup=BeautifulSoup(res.text,'lxml')
    
    
    for href in soup.find("ul", class_="search_list_1").find_all("li"):
        print(f"=============={index}번 영화===============")
        print(href.dl.text[:-2])    #영화 정보 출력

        name_list.append(href.dl.text.split('\n')[1])
        try :
            score_list.append(float(href.dl.text.split('\n')[3][:4]))
        except :
            ##0으로 할지, 뭐 NULL로 할지는 보류
            score_list.append(0.0)
        # 영화 평점

        user_dic[index] = int(href.dl.dt.a['href'][30:])    #index에 따른 영화 고유 코드 dictionary에 저장
        index = index+1

num = int(input("몇 번 영화를 선택하시겠습니까? (숫자만 입력) "))
movie_num = user_dic[num]   #영화 고유 숫자
DB_dic['name'] = name_list[num]
DB_dic['number'] = movie_num
DB_dic['score'] = score_list[num]
#print(DB_dic)
base_url = f'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code={num}&type=after&onlyActualPointYn=N&onlySpoilerPointYn=N&order=sympathyScore&page='

############################################################리뷰 크롤링
review_list = []   #review 목록을 list에 저장
try:
    for page in range(1,11):    #page를 순환하며 리뷰 크롤링 : p1~p10
        url = f'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code={movie_num}&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page={page}'
        html = urlopen(url)
        soup = BeautifulSoup(html,'html.parser')
        for i in range(10): #page에 review 10개씩 가져오기
            review = soup.find('span',{'id':f'_filtered_ment_{i}'})
            review = review.get_text().strip()
            review_list.append(review)  #review를 review_list에 append
except:
    print("오류 발생")


with open(f'{movie_num}.txt','w',encoding='utf-8') as f:    #파일 저장
    for single_review in review_list:
        f.write(single_review+'\n')

del review_list # 메모리 절약을 위한 리스트 삭제

############################################################형태소 분석
def get_tags(text, ntags=500):
    spliter = Okt()
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


frequency(str(movie_num))
print(text_file_name)

############################################################긍정/부정 단어 비교
def open_review(title):
    doc = ''
    file = open('%s_count.txt'%title, 'r', encoding='utf-8')
    lines = file.readlines()
    for line in lines:
        doc += line
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


print_senti("%s" % str(movie_num))


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
    print(pos_word_l)
    print(pos_word_n)
    size=183/size
    list_len = len(pos_word_l)
    for i in range(0, list_len):
        taglist.append({'color': (70, 65, 217), 'size': int(float(int(pos_word_n[i])*4*size) + 20), 'tag': '%s' % pos_word_l[i]})
    list_len = len(neg_word_l)
    for i in range(0, list_len):
        taglist.append({'color': (255, 0, 0), 'size': int(float(int(neg_word_n[i])*4 * size) + 20), 'tag': '%s' % neg_word_l[i]})
    pytagcloud.create_tag_image(taglist,'%s.jpg' % title, size=(1000,500), fontname='malgunbd', rectangular=False)

    
cloud(str(movie_num))

insertData()
printData()
#개봉안한영화 -> 예외처리
