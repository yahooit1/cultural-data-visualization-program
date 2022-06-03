import tkinter as tk                # python 3
from tkinter import StringVar, font  as tkfont # python 3
from tkinter import messagebox
from PIL import ImageTk, Image
import sqlite3
import os
import crawling
import sys


con, cur = None, None
DB_dic={}
def insertData(name, type) :
    con = sqlite3.connect("Test.db")##개인설정으로 바꿔야함.
    cur = con.cursor()
    ##data1 = DB_dic['name']
    ##data2 = DB_dic['type']
    #data3 = str(DB_dic['number'])
    #print(data1)
    #print(type(data1), type(data2), type(data3))
    #sql = "INSERT INTO ex VALUES('"+data1+"','"+data2+"','"+data3+"');"
    ##sql = "INSERT INTO tb2 VALUES('"+data1+"','"+data2+"');"
    ##cur.execute(sql)
    sql_insert = 'insert into tb2 values ( ?, ? )'
    sql_data = (name, type )
    cur.execute( sql_insert, sql_data )
    con.commit()
    con.close()
'''
def printData() :
    sys.stdout = open('mydb.txt', 'w')
    conn = sqlite3.connect( 'test.db' )

    cursor = conn.cursor()

    cursor.execute("select * from tb2;") 
    print(cursor.fetchall())                                                   #db
    cursor.close()
    conn.close()
    sys.stdout.close()'''

def printData() :
    sys.stdout = open('mydb.txt', 'w')
    conn = sqlite3.connect( 'test.db' )
    cursor = conn.cursor()
    cursor.execute("select * from tb2;") 

    conn.commit()
    item_list = cursor.fetchall()

    for it in item_list:
        print(it)
    conn.close()

    sys.stdout.close()

#################################################################3333
window=tk.Tk()

window.title("팀프로젝트")
window.geometry("1300x700")

def check():
    
    if(RadioVariety_1.get() == 0):
        #DB_dic['type'] = "영화"
        #DB_dic['name'] = input_text.get()
        type = "영화"
        name = input_text.get()
        insertData(name, type) 

        crawling.movie_function(input_text.get())
        textbox.delete('1.0', tk.END)
        with open("stdout.txt", "r") as f:
            textbox.insert(tk.END, f.read())

    if(RadioVariety_1.get() == 1):
        #DB_dic['type'] = "책"
        #DB_dic['name'] = input_text.get()
        type = "영화"
        name = input_text.get()
        insertData(name, type) 
        crawling.book_function(input_text.get())

        textbox.delete('1.0', tk.END)
        with open("stdout.txt", "r") as f:
            textbox.insert(tk.END, f.read())
    
    if(RadioVariety_1.get() == 2):
        #DB_dic['type'] = "어플"
        #DB_dic['name'] = input_text.get()
        type = "영화"
        name = input_text.get()
        insertData(name, type) 
        crawling.app_function(input_text.get())
        textbox.delete('1.0', tk.END)
        with open("stdout.txt", "r") as f:
            textbox.insert(tk.END, f.read())

    

def second_check():
    second_radio_num = RadioVariety_2.get()

    if(RadioVariety_1.get() == 0):
        code_num = crawling.movie_num(second_radio_num)
        crawling.movie_crawling(code_num)
        crawling.frequency(code_num)    
        crawling.print_senti(code_num)   
        crawling.cloud(code_num)
        image_path = "wordcloud.jpg"
        img = ImageTk.PhotoImage(Image.open(image_path))
        #The Label widget is a standard Tkinter widget used to display a text or image on the screen.
        panel = tk.Label(window, image = img)
        #The Pack geometry manager packs widgets in rows or columns.
        panel.pack(side="right")

    if(RadioVariety_1.get() == 0):
        code_num = crawling.movie_num(second_radio_num)
        crawling.movie_crawling(code_num)
        crawling.frequency(code_num)    
        crawling.print_senti(code_num)   
        crawling.cloud(code_num)

        image_path = "wordcloud.jpg"
        img = ImageTk.PhotoImage(Image.open(image_path))
        panel = tk.Label(window, image = img)
        panel.image = img
        panel.place(x=600,y=50)
        printData()

    if(RadioVariety_1.get() == 1):
        code_num = crawling.book_num(second_radio_num)
        crawling.book_crawling(code_num)
        crawling.frequency(code_num)    
        crawling.print_senti(code_num)   
        crawling.cloud(code_num)

        image_path = "wordcloud.jpg"
        img = ImageTk.PhotoImage(Image.open(image_path))
        panel = tk.Label(window, image = img)
        panel.image = img
        panel.place(x=600,y=50)#pack(side = "bottom", fill = "both", expand = "yes")
        printData()

    if(RadioVariety_1.get() == 2):
        code_num = crawling.app_num(second_radio_num)
        outfile = os.path.join(str(code_num)+'.txt')
        crawling.appstore_crawler(code_num, outfile=outfile)
        crawling.frequency(code_num)    
        crawling.print_senti(code_num)   
        crawling.cloud(code_num)
       # time.sleep(10)

        image_path = "wordcloud.jpg"
        img = ImageTk.PhotoImage(Image.open(image_path))
        panel = tk.Label(window, image = img)
        panel.image = img
        panel.place(x=600,y=50)
        printData()


input_text= StringVar() ##string 변수 선언
edit1 = tk.Entry(window,font=('Arial', 20), textvariable= input_text)  
edit1.place(x=80,y=100)

RadioVariety_1=tk.IntVar()
RadioVariety_2=tk.IntVar() 
RadioVariety_3=tk.IntVar()  
    
radio1=tk.Radiobutton(window, text="영화", value=0, variable=RadioVariety_1, command=check)
radio1.place(x=40,y=160)

radio2=tk.Radiobutton(window, text="책", value=1, variable=RadioVariety_1, command=check)
radio2.place(x=140,y=160)

radio3=tk.Radiobutton(window, text="어플", value=2, variable=RadioVariety_1, command=check)
radio3.place(x=240,y=160)


radio1=tk.Radiobutton(window, text="1번", value=1, variable=RadioVariety_2, command=second_check)
radio1.place(x=40,y=550)

radio2=tk.Radiobutton(window, text="2번", value=2, variable=RadioVariety_2, command=second_check)
radio2.place(x=140,y=550)

radio3=tk.Radiobutton(window, text="3번", value=3, variable=RadioVariety_2, command=second_check)
radio3.place(x=240,y=550)

radio4=tk.Radiobutton(window, text="4번", value=4, variable=RadioVariety_2, command=second_check)
radio4.place(x=340,y=550)

radio5=tk.Radiobutton(window, text="5번", value=5, variable=RadioVariety_2, command=second_check)
radio5.place(x=440,y=550)

label2 = tk.Label(window, text="이름",font=('Arial', 20))
label2.place(x=0,y=100)

##텍스트 상자
#scrollbar = tk.Scrollbar(window)
#scrollbar.pack()
textbox = tk.Text(window)
textbox.place(x=10,y=200)


#textbox.config(yscrollcommand=scrollbar.set)
#scrollbar.config(command=textbox.yview)

SearchPhoto = tk.PhotoImage(file="SearchPhoto.png")
Searchbutton = tk.Button(window, image = SearchPhoto)
Searchbutton.image = SearchPhoto
Searchbutton.place(x=0,y=0)


def db_text():
    textbox2.delete('1.0', tk.END)
    with open("mydb.txt", "r") as f:
        textbox2.insert(tk.END, f.read())
##db 텍스트 상자
#scrollbar2 = tk.Scrollbar(window)
#scrollbar2.pack()
textbox2 = tk.Text(window, width=50, height=10)
textbox2.place(x=700,y=500)
#textbox.config(yscrollcommand=scrollbar2.set)
#scrollbar.config(command=textbox2.yview)

radio6=tk.Radiobutton(window, text="DB 새로고침", value=0, variable=RadioVariety_3, command=db_text)
radio6.place(x=000,y=650)


window.mainloop()

