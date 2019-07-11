# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 23:31:49 2019

@author: Lenovo
"""

import requests
from bs4 import BeautifulSoup as soup
from selenium import webdriver
import time
import csv
import re

with open('atdp.csv', 'a', encoding='utf-8') as csvFile:
    writer = csv.writer(csvFile)
    headers = ['company_name','Email','Website','Contact']
    writer.writerow(headers)
filename="a.csv"
f=open(filename,"w",encoding="utf-8")

headers="company_name,Email,Website,Contact\n"

f.write(headers)


url = "https://www.atdp-textiles.org/member-list/"

prefs = {
  "translate_whitelists": {"fr":"en"},
  "translate":{"enabled":"true"}
}
options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', prefs)
driver_location = r"C:\Users\Lenovo\Documents\chromedriver"
wb = webdriver.Chrome(driver_location, chrome_options=options)
wb.get(url)
time.sleep(1)
for i in range(46):
    first = int(i*1000)
    second = int(first + 1000)
    #print(first, second)
    time.sleep(0.5)
    wb.execute_script("window.scrollTo("+str(first)+", "+str(second)+")") 
html = wb.execute_script('return document.documentElement.outerHTML')

page_soup = soup(html, features="html.parser")
table=page_soup.findAll('table')
print(len(table))

for t in range(0,25):
    a=table[t].findAll('tr')
    print('rows=')
    print(len(a))

    for j in range(1,len(a)):
        tds=a[j].findAll('td')
        #print(len(tds))
        if ((len(tds))==5):

            company_name=tds[1].text
            #company_name = translator.translate(company_name).text
            #print(company_name)
            company_name = " ".join(re.findall("[a-zA-Z]+", company_name))

            print(company_name)
        
            detail=[]
            adress=[]
            Website='NaN'
            Email='NaN'
            contact=tds[2].findAll('p')
            for p in contact:
                detail.append(p.getText())
            #print(detail)
            for m in range(0,len(detail)):
                if('@' in detail[m]):
                    Email=detail[m]
                elif('www' in detail[m]):
                    Website=detail[m]
                else:
                    adress.append(detail[m])

            

            numbers=tds[3].text.replace(',','|').replace('\n','').replace(' ','')
            #numbers = translator.translate(numbers).text
            print(numbers)
            
            #print(company_name)
            print(Email)
            print(Website)
            f.write(company_name+","+Email.replace(',','|')+","+Website+","+numbers+"\n")
            
            with open('atdp.csv', 'a', encoding='utf-8') as csvFile:
                writer = csv.writer(csvFile)
                headers = [company_name,Email.replace(',','|'),Website,numbers.replace('"','|')]
                writer.writerow(headers)

csvFile.close()
f.close()

