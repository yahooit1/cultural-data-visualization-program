import tkinter as tk                # python 3
from tkinter import StringVar, font  as tkfont # python 3
from tkinter import messagebox
from PIL import ImageTk, Image
import time
import os
import crawling
#################################################################3333
window=tk.Tk()

window.title("팀프로젝트")
window.geometry("1500x800")

def check():
    
    if(RadioVariety_1.get() == 0):
        crawling.movie_function(input_text.get())
        textbox.delete('1.0', tk.END)
        with open("stdout.txt", "r") as f:
            textbox.insert(tk.END, f.read())

    if(RadioVariety_1.get() == 1):
        crawling.book_function(input_text.get())
        textbox.delete('1.0', tk.END)
        with open("stdout.txt", "r") as f:
            textbox.insert(tk.END, f.read())
    
    if(RadioVariety_1.get() == 2):
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
        panel.place(x=600,y=200)

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
        panel.place(x=600,y=200)#pack(side = "bottom", fill = "both", expand = "yes")

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
        panel.place(x=600,y=200)


input_text= StringVar() ##string 변수 선언
edit1 = tk.Entry(window,font=('Arial', 20), textvariable= input_text)  
edit1.place(x=80,y=100)

RadioVariety_1=tk.IntVar()
RadioVariety_2=tk.IntVar()        
    
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
scrollbar = tk.Scrollbar(window)
scrollbar.pack()
textbox = tk.Text(window)
textbox.place(x=10,y=200)


textbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=textbox.yview)

SearchPhoto = tk.PhotoImage(file="SearchPhoto.png")
Searchbutton = tk.Button(window, image = SearchPhoto)
Searchbutton.image = SearchPhoto
Searchbutton.place(x=0,y=0)
window.mainloop()

