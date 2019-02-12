#access csv and extract emails
#convert the emails to domains, filter bad data, visit sites and grab html as a soup
#export html to a txt file for each page scraped

import requests
with requests.Session() as s:
    url = "https://yourloginsite.com/sign-in"
    headers = {"user-agent" : "your browser headers"}
    r = s.get(url, headers=headers)
login_data = {"login id": "youremail@email.com",
"password": "yourpassword",
"Sign_In":""}
r = s.post(url, data =login_data, headers=headers)
url = "http://yourfile.com/file.csv"
r = s.get(url)

import csv
with open("channelpartnerpy.csv", "w") as f:
    writer = csv.writer(f)
    reader = csv.reader(r.text.splitlines())

    for row in reader:
        writer.writerow(row)

import pandas as pd
path = "yourfile.csv"
df = pd.read_csv(path,encoding = "ISO-8859-1")
df.to_csv("file.csv",encoding = "utf-8", index =False, header = True)

df1 = df[["Email 1"]]
df2 = df[["Email 2"]]

df1 = df1.dropna()
df2 = df2.dropna()

email1 = df1["Email 1"].tolist()
email2 = df2["Email 2"].tolist()
emails = email1 + email2

num = 0
string = ""
domains =[]
length = len(emails)-1

for i in range (0,length):
    string = emails[i]
    num = (string.find("@"))+1
    string = string[num:]
    domains.append(string)
domains = list(dict.fromkeys(domains))
domains = sorted(domains, key=str.lower)

emaildomains = pd.read_csv('mostcommondomains.csv', sep=',')
emaildomains = emaildomains["domain"].tolist()
domains = [x for x in domains if '@' not in x]
cleanemails = [x for x in domains if x not in emaildomains]

import bs4
import re
import time
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

length = len(cleanemails)-1
cleandomains = []
for i in range(0,length):
    string = "http://www."+ cleanemails[i]
    cleandomains.append(string)

soup_array = []
urls = cleandomains
def get_soup():
    n=0
    while n <length:
        try:
            my_url = urls[n]
            uReq(my_url)
            uClient = uReq(my_url)
            page_html = uClient.read()
            uClient.close()
            page_soup = str(soup(page_html, "html.parser"))
            soup_array.append(page_soup)
            print(urls[n])
            print(page_soup[:200])
            n += 1
            print('saving soup number '+str(n))
            text_file = open("file"+str(n)+".txt", "w", encoding = "utf-8")
            text_file.write(urls[n] + " \n")
            text_file.write(page_soup)
            text_file.close()
        except:
            print("error " + str(n) +" "+str(urls[n]))
            n+=1
            
get_soup()
