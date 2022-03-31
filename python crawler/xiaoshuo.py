import os
import requests 
from bs4 import BeautifulSoup 
search_url = "https://www.tadu.com/search" 
uri = "https://www.tadu.com" 
search_content = input("请输入小说名：") 
search_req = requests.post(search_url, data={"query": search_content})
search_soup = BeautifulSoup(search_req.text, "lxml")
search_data = []
num = 1 
for search_a in search_soup.find_all("a", {"class": "bookNm"}):
    title = search_a.text
    search_result = uri+search_a.get("href")
    search_data.append([title, search_result])
    print("[" + str(num) + "]", title)
    num = num + 1 
choose_num = input("请选择数字:") 
book_title = search_data[int(choose_num)-1][0] 
os.mkdir(book_title) 
book_url = search_data[int(choose_num)-1][1] 
tmp = book_url.rsplit("/", 2) 
book_url = tmp[0] + "/catalogue/" + tmp[1]
# book_url = "https://www.tadu.com/book/catalogue/734979" 
ua = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36"}
book_req = requests.get(book_url, headers=ua) 
book_soup = BeautifulSoup(book_req.text, "lxml") 
book_soup.find("div", {"class": "chapter clearfix"}) 
book_div = book_soup.find("div", {"class": "chapter clearfix"}) 
book_a = book_div.find_all("a") 
# uri = "https://www.tadu.com"
for i in book_a:
    title = i.text.replace("\n", "").replace(" ", "") 
    chapter_url = uri + i.get("href").replace(" ", "")
    print(title) 
    print(chapter_url) 
    chapter_req = requests.get(chapter_url, headers=ua) 
    chapter_soup = BeautifulSoup(chapter_req.text, "lxml") 
    data_url = chapter_soup.find("input").get("value") 
    data_req = requests.get(data_url, headers=ua) 
    data_soup = BeautifulSoup(data_req.text, "lxml")
    file = open(book_title+"\\"+title.split("章")[0]+"章.txt", "w")
    for j in data_soup.find_all("p")[1:]: 
        line = j.text.replace("\u3000", "") + "\n"
        file.write(line)
    file.close()
    #break