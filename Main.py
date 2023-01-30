import pandas as pd
from tk import *
from datetime import datetime
from tkinter import *
from tkinter import messagebox
import csv
import requests
from bs4 import BeautifulSoup
import openpyxl

import time

import threading
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, as_completed
from openpyxl import Workbook
MAX_THREADS = 30
remaining = 0
titles = ["name","description","category_id","sub_category_id","price","tax","status","discount","discount_type","tax_type","unit"]
data_all = []
links = []
length = 0
handled = 0
dataframe = pd.DataFrame(columns= titles)
category_id_r = ""

counter = 1
def isNone(liste):
    for i in liste:
        if i == None:
            return True
        
    return False
def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))
def take_product_link(link_2):
    products = []
    try:
        
        print(link_2) 
        response_urls = requests.get(link_2)
        html_content1 = response_urls.content
        soup_1= BeautifulSoup(html_content1, "html.parser")
        divs = soup_1.find_all("div",{"class":"MPProductItem"})
        if isNone(divs):
            try:
                time.sleep(0.1)
                response_urls = requests.get(link_2)
                html_content1 = response_urls.content
                soup_1= BeautifulSoup(html_content1, "html.parser")
                divs = soup_1.find_all("div",{"class":"MPProductItem"})
            except:
                pass
        for div in divs:
            href = "https://umico.az" + div.find("a").get("href")
            products.append(href)
        print(products)
        
        return products
    except:
        try:
            time.sleep(1)
            response_urls = requests.get(link_2)
            html_content1 = response_urls.content
            soup_1= BeautifulSoup(html_content1, "html.parser")
            divs = soup_1.find_all("div",{"class":"MPProductItem"})

            for div in divs:
                href = "https://umico.az" + div.find("a").get("href")
                products.append(href)
            print(products)
            return products
        except:
            pass
    
def take_product_data(link_1):
     
            
    data = []
    
    
                
    
    
    print("*")
    try:
        response = requests.get(link_1)
        html_content = response.content
        soup= BeautifulSoup(html_content, "html.parser")
        name_div = soup.find("div",{"class":"MPProductMainDesc"})
        name = name_div.find("h1")
        data.append(name.text)
        description = soup.find("div",{"class":"MPShortInfo"}).prettify()
        data.append(description)
        category_id_div = soup.find("div",{"class":"MPMegaDiscounts-AllCategories"})
        category_id_a = category_id_div.find("a")
        
        data.append(category_id_a.get("href").split("id=")[1])
        data.append(category_id_a.get("href").split("id=")[1])#for subcategory id
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
        """print(data)"""
        if isNone(data):
            data = []
            try:
                response = requests.get(link_1)
                html_content = response.content
                soup= BeautifulSoup(html_content, "html.parser")
                name_div = soup.find("div",{"class":"MPProductMainDesc"})
                name = name_div.find("h1")
                data.append(name.text)
                description = soup.find("div",{"class":"MPShortInfo"}).prettify()
                data.append(description)
                category_id_div = soup.find("div",{"class":"MPMegaDiscounts-AllCategories"})
                category_id_a = category_id_div.find("a")
                
                data.append(category_id_a.get("href").split("id=")[1])
                data.append(category_id_a.get("href").split("id=")[1])#for subcategory id
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
                """print(data)"""
                return data
            except:
                try:
                    time.sleep(0.1)
                    response = requests.get(link_1)
                    html_content = response.content
                    soup= BeautifulSoup(html_content, "html.parser")
                    name_div = soup.find("div",{"class":"MPProductMainDesc"})
                    name = name_div.find("h1")
                    data.append(name.text)
                    description = soup.find("div",{"class":"MPShortInfo"}).prettify()
                    data.append(description)
                    category_id_div = soup.find("div",{"class":"MPMegaDiscounts-AllCategories"})
                    category_id_a = category_id_div.find("a")
                    
                    data.append(category_id_a.get("href").split("id=")[1])
                    data.append(category_id_a.get("href").split("id=")[1])#for subcategory id
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
                    """print(data)"""
                    if isNone(data):
                        print("There is a none")
                    return data
                except:
                    pass
        
        return data
    except:
        try:
            time.sleep(1)
            response = requests.get(link_1)
            html_content = response.content
            soup= BeautifulSoup(html_content, "html.parser")
            name_div = soup.find("div",{"class":"MPProductMainDesc"})
            name = name_div.find("h1")
            data.append(name.text)
            description = soup.find("div",{"class":"MPShortInfo"}).prettify()
            data.append(description)
            category_id_div = soup.find("div",{"class":"MPMegaDiscounts-AllCategories"})
            category_id_a = category_id_div.find("a")
            
            data.append(category_id_a.get("href").split("id=")[1])
            data.append(category_id_a.get("href").split("id=")[1])#for subcategory id
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
            """print(data)"""
            return data
        except:
            pass
    
    
    

def VeriCek():
    global data_all
    global counter
    global links
    global dataframe
    global category_id_r
    
    file_name = str(datetime.now())[:19].replace(":", ".").replace(" ", "_") +".xlsx"#I will declare the file name as current date 
    
    
    urls = TextArea.get("1.0",END)
    url_list = urls.split("\n") 
    
    while '' in url_list:
        url_list.remove('')
    
    for url in url_list:
        category_id_r= url.split("/")[4].split("-")[0]
        
        
           
        if url[:-1].endswith("page=") or url[:-2].endswith("page=") or url[-3].endswith("page="):
            pass    
        else:
            url = url + f"page=1"
        links = []
        url = url.strip()
        print(url)
        items =[]
        response_urls = requests.get(url)
        html_content1 = response_urls.content
        soup_1= BeautifulSoup(html_content1, "html.parser")
        divs = soup_1.find_all("div",{"class":"MPProductItem"})
        
        last_page_list = soup_1.find_all("li",{"class":"MPProductPagination-PageItem"})
        print(last_page_list)

        try:

            last_page = int(last_page_list[-2].find("a").text)
        except ValueError or IndexError:
            last_page = int(last_page_list[-1].find("a").text)
        for div in divs:
            href = "https://umico.az" + div.find("a").get("href")
            links.append(href)

        print("Max Page:",last_page)
        category_urls = []
        for i in range(2,last_page+1):
            
            main_url = url.split("?")
            main_url[1] =  f"page={i}"
            main_url = "?".join(main_url)
            print(main_url)
            category_urls.append(main_url)
        
        print(category_urls)
        print(len(category_urls))
        """counter +=1"""
        with ThreadPoolExecutor(max_workers=min(len(category_urls), 20)) as executor:
           
            futures1 = [executor.submit(take_product_link, category_url)for category_url in category_urls]
            for future1 in as_completed(futures1):
                links.extend(future1.result())

        executor.shutdown()        
        print("The len of the links:" +  str(len(links)))
        """while True:
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
            print("The len of the links:" +  str(len(links)))"""
        handled = len(links)
        with ThreadPoolExecutor(max_workers=min(len(links), 70)) as executor:
            
            futures = [executor.submit(take_product_data, link) for link in links]
            for future in as_completed(futures):
                
                
                data_all.append(future.result())


        executor.shutdown()
    print(data_all)
    print(len(data_all))

            

        

        
                
                
                
                
        
    for i in data_all:
        try:
            i[2] = category_id_r
        except TypeError:
            continue

    
    print("data all uzunluk:"+str(len(data_all)))
    wb = Workbook()
    sheet = wb.active
    sheet.append(["name","description","category_id","sub_category_id","price","tax","status","discount","discount_type","tax_type","unit"])
    for row in data_all:
        try:
            sheet.append(row)
        except TypeError:
            continue

    wb.save(f'{file_name}')
    
    
        
    data_all.clear()
    links.clear()
    
    
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