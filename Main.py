import pandas as pd
from tk import *
from datetime import datetime
from tkinter import *
from tkinter import messagebox
import csv
import requests
from bs4 import BeautifulSoup
import openpyxl
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
titles = ["name","description","category_id","sub_category_id","price","tax","status","discount","discount_type","tax_type","unit"]

def VeriCek():
    
    dataframe = pd.DataFrame(columns= titles)
    file_name = str(datetime.now())[:19].replace(":", ".").replace(" ", "_") +".xlsx"#I will declare the file name as current date 
    data_all =[]
    urls = TextArea.get("1.0",END)
    url_list = urls.split("\n") 
    
    while '' in url_list:
        url_list.remove('')
    
    for url in url_list:
        counter = 1
        
           
        if url[:-1].endswith("page="):
            pass    
        else:
            url = url + f"?page={counter}"
        links = []
        url = url.strip()
        
        items =[]
        response_urls = requests.get(url)
        html_content1 = response_urls.content
        soup_1= BeautifulSoup(html_content1, "html.parser")
        divs = soup_1.find_all("div",{"class":"MPProductItem"})
        
        last_page_list = soup_1.find_all("li",{"class":"MPProductPagination-PageItem"})
        try:
            last_page = int(last_page_list[-2].find("a").text)
        except ValueError:
            last_page = int(last_page_list[-1].find("a").text)

        print("Max Page:",last_page)
        
        for div in divs:
            href = "https://umico.az" + div.find("a").get("href")
            links.append(href)
        counter +=1
                
        while True:
            try:
                
                url = url.split("?")
                url[1] = f"page={counter}"
                url = "?".join(url)   
                print(url) 
                response_urls = requests.get(url)
                html_content1 = response_urls.content
                soup_1= BeautifulSoup(html_content1, "html.parser")
                divs = soup_1.find_all("div",{"class":"MPProductItem"})
            except:
                counter += 1
                continue    

            if counter > last_page:
                break
            for div in divs:
                href = "https://umico.az" + div.find("a").get("href")
                links.append(href)
                
            counter +=1
            print("The len of the links:" +  str(len(links)))

        
        for i in links: 
            try:
                data = []       
                print(i)
                
                response = requests.get(i)
                html_content = response.content
                soup= BeautifulSoup(html_content, "html.parser")
                name_div = soup.find("div",{"class":"MPProductMainDesc"})
                name = name_div.find("h1")
                data.append(name.text)
                description = soup.find("div",{"class":"MPShortInfo"})
                data.append(description.prettify())
                category_id_div = soup.find("div",{"class":"MPMegaDiscounts-AllCategories"})
                category_id_a = category_id_div.find("a")
                
                data.append(category_id_a.get("href").split("id=")[1])
                data.append("0")#for subcategory id
                price_div = soup.find("div",{"class":"MPProductMainDesc-OfferPrice"})
                
                
                if price_div.find("span",{"class":"MPPrice-RetailPrice"}):
                    price = soup.find("span",{"class":"MPPrice-RetailPrice"})
                    data.append(price.text.replace("₼","").strip())
                else:
                    old_price = price_div.find("span",{"class":"MPPrice-OldPrice"})
                    data.append(old_price.text.replace("₼","").strip())
                
                data.append("0")#for tax
                data.append("1")#for status
                if soup.find("div",{"class":"MPProductItem-Discount MPProductMainDesc-Discount"}):
                    discount = soup.find("div",{"class":"MPProductItem-Discount MPProductMainDesc-Discount"}).text.split(" ")[0].replace("%","")
                    data.append(discount)
                else:
                    data.append("0")
                data.append("percent")#for discount type
                data.append("percent")#for tax type
                data.append("pc")#for unit
                print(data)
                data_all.append(data)
            except:
                continue
                
                
                
                
        
    
    print(data_all)
    
    for i in data_all:#adding the dataframe our data
        
        dataframe.loc[len(dataframe)] = i
        

    
    

    
    dataframe.to_excel(file_name, index=False)#exporting an excel file
    messagebox.showinfo("Başarılı İşlem",f"Veri Başarıyla {file_name} Dosyasına Kaydedildi!")







#UI Part

master = Tk()#Tkinter UI object
master.title('Data Scraping From umico.az')#For changing the main page title
canvas = Canvas(master, height=400 , width= 600)#Arranging the geometry of page
canvas.pack()

framekontrol = Frame(master,bg= '#65A8E1')#Main frame
framekontrol.place(relx = 0.05,rely = 0.05,relwidth = 0.90, relheight=0.90 )

title1 = Label(framekontrol,bg='#65A8E1', text = "Lütfen umico.az Ürün URL(leri)'sini Giriniz:", font= "20")
title1.pack(anchor=N, padx= 10, pady= 10)#The title which is a indicator for the task of text area

TextArea = Text(framekontrol, height= 10, width = 50)#Text area which will take the link
TextArea.pack(anchor= N, padx = 10, pady = 1)

Submit_button = Button(framekontrol, text = "Veri Çek", command= VeriCek)
Submit_button.pack(anchor = S,padx=10,pady=40)#Button which can submit the link to the program.


title2 = Label(framekontrol,bg='#65A8E1', text = "Lütfen girdiğiniz her bir URL'nin ardından bir kere enter tuşuna basınız.", font= "20")
title2.pack(anchor=S, padx= 10, pady= 5)#The title which is a indicator for the task of text area



mainloop()