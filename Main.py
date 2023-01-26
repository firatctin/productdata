import pandas as pd
from tk import *
from datetime import datetime
from tkinter import *
from tkinter import messagebox
import csv
def VeriCek():
    print(TextArea.get("1.0",END))
    messagebox.showinfo("Başarılı İşlem",f"Veri Başarıyla {file_name} Dosyasına Kaydedildi!")

#Creating the csv file which will store the data:
file_name = str(datetime.now())[:19].replace(":", ".").replace(" ", "_")#I will declare the file name as current date 
titles = ["name","description","category_id","sub_category_id","price","tax","status","discount","discount_type","tax_type","unit","total_stock"]
with open(f"{file_name}.csv", 'w') as csvfile:
    csvwriter = csv.writer(csvfile)#Writing the column titles to the csv file
    csvwriter.writerow(titles)


#UI Part

master = Tk()#Tkinter UI object
master.title('Data Scraping From umico.az')#For changing the main page title
canvas = Canvas(master, height=200 , width= 600)#Arranging the geometry of page
canvas.pack()

framekontrol = Frame(master,bg= '#65A8E1')#Main frame
framekontrol.place(relx = 0.05,rely = 0.05,relwidth = 0.90, relheight=0.90 )

title1 = Label(framekontrol,bg='#65A8E1', text = "Lütfen umico.az Ürün URL'si Giriniz:", font= "20")
title1.pack(anchor=N, padx= 10, pady= 10)#The title which is a indicator for the task of text area

TextArea = Text(framekontrol, height= 1, width = 50)#Text area which will take the link
TextArea.pack(anchor= N, padx = 10, pady = 1)

Submit_button = Button(framekontrol, text = "Veri Çek", command= VeriCek)
Submit_button.pack(anchor = S,padx=10,pady=40)#Button which can submit the link to the program.


mainloop()