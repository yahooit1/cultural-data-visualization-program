import tkinter as tk                # python 3
from tkinter import StringVar, font  as tkfont # python 3
from tkinter import messagebox
from PIL import ImageTk, Image
import sqlite3
import os
import crawling
import sys



#import Tkinter as tk     # python 2
#import tkFont as tkfont  # python 2

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.backcolor = "#FFFFFF" ## 
        self.buttoncolor = "#469bbb"

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.configure(bg=controller.backcolor, borderwidth=10) ## 배경색
        SearchPhoto = tk.PhotoImage(file="SearchPhoto.png")
        HistoryPhoto = tk.PhotoImage(file="HistoryPhoto.png")
        ClosePhoto = tk.PhotoImage(file="ClosePhoto.png")
        TitlePhoto = tk.PhotoImage(file="TitlePhoto.png")

        #label = tk.Label(self, text="start page", font=controller.title_font, background=controller.backcolor) ## 포인트 쓰려면 부모 클래스 controller. ㅁㅁ
        teamlabel = tk.Label(self, text= "예스파일!", font=controller.title_font, background=controller.backcolor)
        Title = tk.Label(self, image = TitlePhoto, background=controller.backcolor)
        Searchbutton = tk.Button(self, image = SearchPhoto, command = lambda: controller.show_frame("PageOne"), background=controller.backcolor)
        Historybutton = tk.Button(self, image = HistoryPhoto, command = lambda: controller.show_frame("PageTwo"), background=controller.backcolor) ## 기록 버튼
        closebutton = tk.Button(self, image = ClosePhoto, command = quit, background=controller.backcolor)
        
        
        ## 파이썬의 가비지 컬렉터가 사진을 지워버리기 때문에 수동으로 참고 횟수를 늘려주어야 이미지 유지가 가능함
        closebutton.image = ClosePhoto
        Searchbutton.image = SearchPhoto
        Historybutton.image = HistoryPhoto
        Title.image = TitlePhoto

        #label.place(x=0,y=0)
        Title.place(x=400,y=000)
        Searchbutton.place(x=545,y=440)
        Historybutton.place(x=545,y=505)
        closebutton.place(x=545,y=570)
        teamlabel.place(x=1200,y=620)


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg=controller.backcolor, borderwidth=10) ## 배경색 
        con, cur = None, None
        DB_dic={}
        def insertData(name, type) :
            con = sqlite3.connect("Test.db")##개인설정으로 바꿔야함.
            cur = con.cursor()
            sql_insert = 'insert into tb2 values ( ?, ? )'
            sql_data = (name, type )
            cur.execute( sql_insert, sql_data )
            con.commit()
            con.close()
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
                type = "책"
                name = input_text.get()
                insertData(name, type) 
                crawling.book_function(input_text.get())

                textbox.delete('1.0', tk.END)
                with open("stdout.txt", "r") as f:
                    textbox.insert(tk.END, f.read())
    
            if(RadioVariety_1.get() == 2):
                #DB_dic['type'] = "어플"
                #DB_dic['name'] = input_text.get()
                type = "어플"
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

                image_path = f"{code_num}.jpg"
                img = ImageTk.PhotoImage(Image.open(image_path))
                panel = tk.Label(self, image = img, background=controller.backcolor)
                panel.image = img
                panel.place(x=600,y=50)
                printData()

            if(RadioVariety_1.get() == 1):
                code_num = crawling.book_num(second_radio_num)
                crawling.book_crawling(code_num)
                crawling.frequency(code_num)    
                crawling.print_senti(code_num)   
                crawling.cloud(code_num)

                image_path = f"{code_num}.jpg"
                img = ImageTk.PhotoImage(Image.open(image_path))
                panel = tk.Label(self, image = img, background=controller.backcolor)
                panel.image = img
                panel.place(x=600,y=50)
                printData()

            if(RadioVariety_1.get() == 2):
                code_num = crawling.app_num(second_radio_num)
                outfile = os.path.join(str(code_num)+'.txt')
                crawling.appstore_crawler(code_num, outfile=outfile)
                crawling.frequency(code_num)    
                crawling.print_senti(code_num)   
                crawling.cloud(code_num)
                # time.sleep(10)

                image_path = f"{code_num}.jpg"
                img = ImageTk.PhotoImage(Image.open(image_path))
                panel = tk.Label(self, image = img)
                panel.image = img
                panel.place(x=600,y=50)
                printData()
            

        input_text= StringVar()   
        edit1 = tk.Entry(self,font=('Arial', 20), textvariable= input_text)
        edit1.place(x=80,y=100)

        RadioVariety_1=tk.IntVar()
        RadioVariety_2=tk.IntVar() 
        RadioVariety_3=tk.IntVar() 
        
        radio1=tk.Radiobutton(self, text="영화", value=0, variable=RadioVariety_1, command=check, background=controller.backcolor)
        radio1.place(x=40,y=160)

        radio2=tk.Radiobutton(self, text="책", value=1, variable=RadioVariety_1, command=check, background=controller.backcolor)
        radio2.place(x=140,y=160)

        radio3=tk.Radiobutton(self, text="어플", value=2, variable=RadioVariety_1, command=check, background=controller.backcolor)
        radio3.place(x=240,y=160)

        radio1=tk.Radiobutton(self, text="1번", value=1, variable=RadioVariety_2, command=second_check, background=controller.backcolor)
        radio1.place(x=40,y=550)
        radio2=tk.Radiobutton(self, text="2번", value=2, variable=RadioVariety_2, command=second_check, background=controller.backcolor)
        radio2.place(x=140,y=550)

        radio3=tk.Radiobutton(self, text="3번", value=3, variable=RadioVariety_2, command=second_check, background=controller.backcolor)
        radio3.place(x=240,y=550)

        radio4=tk.Radiobutton(self, text="4번", value=4, variable=RadioVariety_2, command=second_check, background=controller.backcolor)
        radio4.place(x=340,y=550)

        radio5=tk.Radiobutton(self, text="5번", value=5, variable=RadioVariety_2, command=second_check, background=controller.backcolor)
        radio5.place(x=440,y=550)

        label2 = tk.Label(self, text="이름",font=('Arial', 20), background=controller.backcolor)
        label2.place(x=0,y=100)

        textbox = tk.Text(self)
        textbox.place(x=10,y=200)

        LogoPhoto = tk.PhotoImage(file="LogoPhoto.png")
        Logo = tk.Label(self, image = LogoPhoto, background=controller.backcolor)
        Logo.image = LogoPhoto
        Logo.place(x=0,y=0)
        
        HomePhoto = tk.PhotoImage(file="homebutton.png")
        Homebutton = tk.Button(self, image = HomePhoto, background=controller.backcolor, command=lambda: controller.show_frame("StartPage"))
        Homebutton.image = HomePhoto
        Homebutton.place(x=1250,y=550)

        #Backbutton = tk.Button(self, text="뒤로 가기",font=("System", 30), command=lambda: controller.show_frame("StartPage"),background=controller.buttoncolor, activebackground=controller.buttoncolor) ## 배경색과 동일하게 
        
        #Backbutton.place(x=1100,y=600)


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.configure(bg=controller.backcolor, borderwidth=10) ## 배경색 
        label = tk.Label(self, text="page 2", font=controller.title_font, background=controller.backcolor)
        
        #뒤로 가기
        Backbutton = tk.Button(self, text="뒤로 가기",font=("System", 30),command=lambda: controller.show_frame("StartPage"),background=controller.buttoncolor, activebackground=controller.buttoncolor)
        #Backbutton = tk.PhotoImage(file="homebutton.jpg")
        #Backbutton = tk.Button(self, image = Backbutton, background=controller.backcolor)
        #Backbutton.image = Backbutton


        label.place(x=0,y=0)
        Backbutton.place(x=500,y=500)

        def db_text():
            textbox2.delete('1.0', tk.END)
            with open("mydb.txt", "r") as f:
                textbox2.insert(tk.END, f.read())
        ##db 텍스트 상자
        textbox2 = tk.Text(self, width=30, height=20,font=("System", 15))   ###
        #textbox2.resizable(width= tk.FALSE, height= tk.FALSE)

        textbox2.place(x=0,y=0)

        #새로고침 부분
        radio6=tk.Button(self, text="DB 새로고침", command=db_text, background=controller.buttoncolor, activebackground=controller.buttoncolor)
        radio6.place(x=000,y=650)



if __name__ == "__main__":
    
    app = SampleApp()
    app.geometry("1400x700")
    app.title("팀프로젝트")
    app.resizable(width= tk.FALSE, height= tk.FALSE)
    app.mainloop()