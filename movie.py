#https://haystar.tistory.com/9
#pip install lxml
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen

from konlpy.tag import Twitter
from collections import Counter

movie = input("어떤 영화를 검색하시겠습니까? ")
url = f'https://movie.naver.com/movie/search/result.naver?query={movie}&section=all&ie=utf8'

res = requests.get(url)
index = 1
user_dic = {}
if res.status_code == 200:
    soup=BeautifulSoup(res.text,'lxml')
    for href in soup.find("ul", class_="search_list_1").find_all("li"): 
        print(f"=============={index}번 영화===============")
        print(href.dl.text[:-2])
        user_dic[index] = int(href.dl.dt.a['href'][30:])
        index = index+1

movie_num = int(input("몇 번 영화를 선택하시겠습니까? (숫자만 입력) "))
code = user_dic[movie_num]
base_url = f'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code={code}&type=after&onlyActualPointYn=N&onlySpoilerPointYn=N&order=sympathyScore&page='

print(code)
#################################################################################
movie_num = code #영화 고유 숫자 입력

#https://velog.io/@changhtun1/%ED%8C%8C%EC%9D%B4%EC%8D%AC%EC%9D%84-%ED%99%9C%EC%9A%A9%ED%95%9C-%EC%9B%B9-%ED%81%AC%EB%A1%A4%EB%A7%81-3


review_list = []   
try:
    for page in range(1,11):    #page를 순환하며 리뷰 크롤링 : p1~p10
        url = f'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code={movie_num}&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page={page}'
        html = urlopen(url)
        soup = BeautifulSoup(html,'html.parser')
        for i in range(10): #page에 review 10개씩
            review = soup.find('span',{'id':f'_filtered_ment_{i}'})
            review = review.get_text().strip()
            review_list.append(review)
except:
    print("오류 발생")


with open(f'././{movie_num}_naver_movie.txt','w',encoding='utf-8') as f:
    #파일 저장 #위치 수정해야
    for single_review in review_list:
        f.write(single_review+'\n')

del review_list # 메모리 절약을 위한 리스트 삭제
################################################################
# knolpy랑 java 설치해야함


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


frequency(str(movie_num)+"_naver_movie")
print(text_file_name)

#############################################################
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
    '''
    print("positive : %d" % pos)
    print("negative : %d" % neg)

    rate = ((pos)/(pos + neg))*100
    print("positive rate of this movie : %.2f%%"%rate)'''


print_senti(str(movie_num)+"_naver_movie")


#################################################################################

#https://velog.io/@ruinak_4127/PytagCloud 설치
import pytagcloud
import sentiment

def cloud(title):
    list = sentiment.open_review("%s"%title)

    try:
        positive = sentiment.open_pos()
        negative = sentiment.open_neg()
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
    #print(taglist)  #
    pytagcloud.create_tag_image(taglist,'wordcloud.jpg', size=(1000,500), fontname='malgunbd', rectangular=False)
    #pytagcloud.create_tag_image(taglist,'wordcloud.jpg', size=(1000,500), rectangular=False)

    
cloud(str(movie_num)+"_naver_movie")

#개봉안한영화 -> 예외처리
