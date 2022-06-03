from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen

from konlpy.tag import Twitter
from collections import Counter
import sys
import pytagcloud

import pandas as pd
import xmltodict
import requests
import os

global NUMBERS
global user_dic

def movie_function(movie):
    global NUMBERS
    global user_dic
    sys.stdout = open('stdout.txt', 'w')
    ############################################################영화 검색 부분
    #movie = input("어떤 영화를 검색하시겠습니까? ")
    url = f'https://movie.naver.com/movie/search/result.naver?query={movie}&section=all&ie=utf8'

    res = requests.get(url)
    index = 1
    user_dic = {}   
    if res.status_code == 200:  #HTTP status code가 OK일 때
        soup=BeautifulSoup(res.text,'lxml')
        for href in soup.find("ul", class_="search_list_1").find_all("li"): 
            print(f"=============={index}번 영화===============")
            print(href.dl.text[:-2])    #영화 정보 출력
            user_dic[index] = int(href.dl.dt.a['href'][30:])    #index에 따른 영화 고유 코드 dictionary에 저장
            index = index+1
    sys.stdout.close()

def movie_num(num): 
    global user_dic
    #num = int(input("몇 번 영화를 선택하시겠습니까? (숫자만 입력) "))
    movie_num = user_dic[num]   #영화 고유 숫자
    #base_url = f'https://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code={num}&type=after&onlyActualPointYn=N&onlySpoilerPointYn=N&order=sympathyScore&page='
    #NUMBERS = movie_num
    return movie_num

def movie_crawling(movie_num):
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
        pass
        #print("오류 발생")


    with open(f'{movie_num}.txt','w',encoding='utf-8') as f:    #파일 저장
        for single_review in review_list:
            f.write(single_review+'\n')

    del review_list # 메모리 절약을 위한 리스트 삭제

    #NUMBERS = movie_num


def book_function(book_name):
    global NUMBERS
    global user_dic
    sys.stdout = open('stdout.txt', 'w')
    ############################################################ 책 검색 부분
    #book_name = input("어떤 책을 검색하시겠습니까? ")
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
    sys.stdout.close()

def book_num(num): 
    global user_dic
    #book_num = int(input("몇 번 책을 선택하시겠습니까? (숫자만 입력) "))
    book_num = user_dic[num]
    #NUMBERS = book_num
    return book_num

def book_crawling(book_num):
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

    with open(f'{book_num}.txt','w',encoding='utf-8') as f:    
        for single_review in review_list:
            f.write(single_review+'\n')

    del review_list # 메모리 절약을 위한 리스트 삭제
    #NUMBERS = book_num

def app_function(app):
    global user_dic
    sys.stdout = open('stdout.txt', 'w')
    global NUMBERS
        #네이버, 카카오, 웹툰, 구글, 유튜브,  <-----검색 잘되는 단어
    #app = input("어떤 앱을 검색하시겠습니까? ")
    url = f'https://www.apple.com/kr/search/{app}?src=globalnav'

    response = requests.get(url)
    index = 1
    user_dic = {}
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    titlelinks = soup.select(".rf-serp-productname")
    
    links = soup.select(".rf-serp-product-description")
    for link in links:
        text = str(link)
        #print(link)
        first = text.find('/id')
        second = text.find('더 보기')
        #print(text[first+3:second-2])
        user_dic[index] = int(text[first+3:second-2])    #dict에 넣기
        index+=1
        if (index ==6): 
            break
    
    index=1
    for titlelink in titlelinks:
        title=titlelink.text #태그 안 텍스트
        title = title.lstrip()
        #specific_url = link.attrs['href']   #href 속성값
        #book_code = specific_url[15:]
        print(f"=============={index}번===============")
        print(title)
        #print(specific_url)
        
        index = index+1
        print()
        if (index ==6): 
            break
    sys.stdout.close()

def app_num(chosen_num):
    global user_dic
    #chosen_num = int(input("몇 번 앱을 선택하시겠습니까? (숫자만 입력) "))
    book_num = user_dic[chosen_num]
    NUMBERS= book_num
    return book_num


def get_url_index(url):
    response = requests.get(url).content.decode('utf8')
    xml = xmltodict.parse(response)

    last_url = [l['@href'] for l in xml['feed']['link'] if (l['@rel'] == 'last')][0]
    last_index = [int(s.replace('page=', '')) for s in last_url.split('/') if ('page=' in s)][0]

    return last_index

# https://stackoverflow.com/questions/1090282/api-to-monitor-iphone-app-store-reviews
def appstore_crawler(appid, outfile='./appstore_reviews.csv'):
    url = 'https://itunes.apple.com/kr/rss/customerreviews/page=1/id=%i/sortby=mostrecent/xml' % appid

    try:
        last_index = get_url_index(url)
    except Exception as e:
        print (url)
        print ('\tNo Reviews: appid %i' %appid)
        print ('\tException:', e)
        return

    result = list()
    for idx in range(1, last_index+1):
        url = "https://itunes.apple.com/kr/rss/customerreviews/page=%i/id=%i/sortby=mostrecent/xml?urlDesc=/customerreviews/id=%i/sortBy=mostRecent/xml" % (idx, appid, appid)
        #print(url)

        response = requests.get(url).content.decode('utf8')
        try:
            xml = xmltodict.parse(response)
        except Exception as e:
            print ('\tXml Parse Error %s\n\tSkip %s :' %(e, url))
            continue

        try:
            num_reivews= len(xml['feed']['entry'])
        except Exception as e:
            print ('\tNo Entry', e)
            continue

        try:
            xml['feed']['entry'][0]['author']['name']
            single_reviews = False
        except:
            #print ('\tOnly 1 review!!!')
            single_reviews = True
            pass

        if single_reviews:
                result.append({
                    'REVIEW': xml['feed']['entry']['content'][0]['#text'],
                })
        else:
            for i in range(len(xml['feed']['entry'])):
                result.append({
                    'REVIEW': xml['feed']['entry'][i]['content'][0]['#text'],
                })

    res_df = pd.DataFrame(result)
    res_df.to_csv(outfile, encoding='utf-8-sig', index=False)
    #print ('Save reviews to file: %s \n' %(outfile))



# https://apps.apple.com/us/app/youtube-watch-listen-stream/id544007664






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


#########책 선택할 경우
#book_function()
#book_crawling(NUMBERS)

###########영화 선택할 경우
#movie_function("겨울왕국")
#movie_crawling(NUMBERS)

#########앱 선택할 경우
#app_function()
#outfile = os.path.join(str(NUMBERS)+'.txt')
#appstore_crawler(NUMBERS, outfile=outfile)



#frequency(str(NUMBERS))
#print(text_file_name)
#print_senti(str(NUMBERS))   
#cloud(str(NUMBERS))