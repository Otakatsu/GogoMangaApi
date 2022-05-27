from bs4 import BeautifulSoup
import requests
import re


def get_search(query, page=1):  
        try:
            mangalink = f"https://gogomanga.fun/page/{page}/?s={query}"
            response = requests.get(mangalink)
            response_html = response.text
            soup = BeautifulSoup(response_html, 'html.parser')
            source_url = soup.find_all('div', attrs={'class': 'bsx'})
            res_search_list = []
            for links in source_url:
                title = links.find('div', attrs={'class': 'tt'}).text.strip()
                mangaId = links.find('a')['href'].split('/')[-2]
                res_search_list.append({"title":f"{title}","mangaid":f"{mangaId}"})
            if res_search_list == []:
                return {"status":"204", "reason":"No search results found for the query"}
            return res_search_list
        except requests.exceptions.ConnectionError:
            return {"status":"404", "reason":"Check the host's network Connection"}



def get_detail(mangaid):  
        try:
            mangalink = f"https://gogomanga.fun/manga/{mangaid}"
            response = requests.get(mangalink)
            response_html = response.text
            soup = BeautifulSoup(response_html, 'html.parser')
            title = soup.find('h1', attrs={'class': 'entry-title'}).text
            imageurl = soup.find('img', class_="attachment- size- wp-post-image")['src']            
            mangaid = mangaid
            url = f"https://gogomanga.fun/manga/{mangaid}"           
            res_search_list = []    
            chapters = []
            chap_url = soup.find_all('div', attrs={'class': 'eph-num'})
            chap_url.reverse()
            for chap in chap_url:
                chapter = chap.find('span', attrs={'class': 'New Chapter'}).text    
                chapternum = 1
                chapters.append({"title":f"{chapter}","chapternum":f"{chapternum}"})
                chapternum = chapternum + 1
                res_search_list.append({"title":f"{title}","imageurl":f"{imageurl}","url":f"{url}","chapter":f"{chapters}"})
            if res_search_list == []:
                return {"status":"204", "reason":"No search results found for the mangaid"}
            return res_search_list
        except requests.exceptions.ConnectionError:
            return {"status":"404", "reason":"Check the host's network Connection"}


def get_chapter(mangaid, chapternum):  
        try:
            mangalink = f"https://gogomanga.fun/{mangaid}-chapter-{chapternum}"
            response = requests.get(mangalink)
            response_html = response.text
            soup = BeautifulSoup(response_html, 'html.parser')           
            res_search_list = []    
            imageurl = []
            url = soup.find_all('img', attrs={'class': 'size-full'})
            for x in url:
                imageurl.append(x['src'])                
                res_search_list.append({"img":f"{imageurl}"})
            if res_search_list == []:
                return {"status":"204", "reason":"No search results found for the chapter"}
            return res_search_list
        except requests.exceptions.ConnectionError:
            return {"status":"404", "reason":"Check the host's network Connection"}




