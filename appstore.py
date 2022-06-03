from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
import re

from konlpy.tag import Twitter
from collections import Counter

import pytagcloud
#네이버, 카카오, 웹툰, 구글, 유튜브,  <-----검색 잘되는 단어
app = input("어떤 앱을 검색하시겠습니까? ")
url = f'https://www.apple.com/kr/search/{app}?src=globalnav'

response = requests.get(url)
index = 1
user_dic = {}
html = response.text
soup = BeautifulSoup(html, 'html.parser')
titlelinks = soup.select(".rf-serp-productname")
links = soup.select(".rf-serp-product-description")
for link in links:
    print("####################")
    
    text = str(link)
    #print(link)
    first = text.find('/id')
    second = text.find('더 보기')
    print(text[first+3:second-2])
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

book_num = int(input("몇 번 앱을 선택하시겠습니까? (숫자만 입력) "))
book_num = user_dic[book_num]
######################################################

import pandas as pd
import xmltodict
import requests
import os

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
        print(url)

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
                    #'USER': xml['feed']['entry']['author']['name'],
                    #'DATE': xml['feed']['entry']['updated'],
                    #'STAR': int(xml['feed']['entry']['im:rating']),
                    #'LIKE': int(xml['feed']['entry']['im:voteSum']),
                    #'TITLE': xml['feed']['entry']['title'],
                    'REVIEW': xml['feed']['entry']['content'][0]['#text'],
                })
        else:
            for i in range(len(xml['feed']['entry'])):
                result.append({
                    #'USER': xml['feed']['entry'][i]['author']['name'],
                    #'DATE': xml['feed']['entry'][i]['updated'],
                    #'STAR': int(xml['feed']['entry'][i]['im:rating']),
                    #'LIKE': int(xml['feed']['entry'][i]['im:voteSum']),
                    #'TITLE': xml['feed']['entry'][i]['title'],
                    'REVIEW': xml['feed']['entry'][i]['content'][0]['#text'],
                })

    res_df = pd.DataFrame(result)
    #res_df['DATE'] = pd.to_datetime(res_df['DATE'], format="%Y-%m-%dT%H:%M:%S")
    res_df.to_csv(outfile, encoding='utf-8-sig', index=False)
    print ('Save reviews to file: %s \n' %(outfile))



# https://apps.apple.com/us/app/youtube-watch-listen-stream/id544007664
app_id = book_num
outfile = os.path.join(str(book_num)+'_appstore'+'.txt')
appstore_crawler(app_id, outfile=outfile)


##########################################################################
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


frequency(str(book_num)+"_appstore")
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


print_senti(str(book_num)+"_appstore")


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

    
cloud(str(book_num)+"_appstore")
