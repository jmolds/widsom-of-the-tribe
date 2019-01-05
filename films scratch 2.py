import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import IPython
from IPython.display import HTML
from IPython.display import display
import requests
from bs4 import BeautifulSoup

film_list = list()
films_per_page_range = range(0,250)
temp_films_list1 = [None] * len(films_per_page_range)
temp_films_list2 = [None] * len(films_per_page_range)
year_range = range(1980,2018)
for year in year_range:
    y1 = year
    imdb_page_1 = "https://www.imdb.com/search/title?title_type=feature&release_date=" + str(y1) + "-01-01," + str(y1) + "-12-31&view=simple&sort=boxoffice_gross_us,desc&count=250&page=1&ref_=adv_nxt"
    imdb_page_2 = "https://www.imdb.com/search/title?title_type=feature&release_date=" + str(y1) + "-01-01," + str(y1) + "-12-31&view=simple&sort=boxoffice_gross_us,desc&count=250&page=2&ref_=adv_nxt"
    page1 = requests.get(imdb_page_1)
    page2 = requests.get(imdb_page_2)
    soup1 = BeautifulSoup(page1.content, 'html.parser')        
    soup2 = BeautifulSoup(page2.content, 'html.parser')  
    lister_tag_list1 = soup1.find_all(class_='lister-item-header')
    lister_tag_list2 = soup2.find_all(class_='lister-item-header')
    for film in films_per_page_range:
        #temp_films_list[film] = str(lister_tag_list1[film])
        #temp_films_list[film] = temp_films_list[film].partition('</a>')[0]
        #temp_films_list[film] = temp_films_list[film].partition('li_tt">')[2]
        temp_films_list1[film] = str(lister_tag_list1[film])
        temp_films_list1[film] = temp_films_list1[film].partition('</a>')[0]
        temp_films_list1[film] = temp_films_list1[film].partition('li_tt">')[2]
        temp_films_list2[film] = str(lister_tag_list2[film])
        temp_films_list2[film] = temp_films_list2[film].partition('</a>')[0]
        temp_films_list2[film] = temp_films_list2[film].partition('li_tt">')[2]
    film_list.extend(temp_films_list1) 
    film_list.extend(temp_films_list2)        
    
pages = [None] * len(imdb_page_range)
soup = [None] * len(imdb_page_range)
for x in range(0,len(imdb_page_range)):
    pages[x] = requests.get(imdb_page_html[x])
    soup[x] = BeautifulSoup(pages[x].content, 'html.parser')
    
lister = [None] * len(imdb_page_range)
for x in range(0,len(imdb_page_range)):
    lister[x] = soup[x].find_all(class_='lister-item-header')
    
temp_films_string = [None] * len(imdb_page_range)
temp_films_seg = [None] * len(imdb_page_range)
temp_films_title = [None] * len(imdb_page_range)
full_films_title = list()
for page in range(0,len(lister)):
    temp_films_title = [None] * len(imdb_page_range)
    for x in range(0,len(lister[page])):
        temp_films_string[x] = str(lister[page][x])
        temp_films_seg[x] = temp_films_string[x].partition('</a>')[0]
        temp_films_title[x] = temp_films_seg[x].partition('li_tt">')[2]
    full_films_title.extend(temp_films_title)
    
len(full_films_title)

def remove_values_from_list(the_list, val):
   return [value for value in the_list if value != val]

full_films_title = remove_values_from_list(full_films_title, None)

for x in range(0,len(full_films_title)):
    full_films_title[x] = full_films_title[x].replace("amp;","")

#####
import csv
film_list = list()
#films_list = csv.reader('/Users/-/Dropbox/Python and SQL/out.csv', dialect='excel')
print(film_list)
film_list = list()
with open('/Users/-/Dropbox/Python and SQL/out.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
        film_list.append(str(row[1]))
full_films_title = film_list  
del full_films_title[0]  

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions
import time
import re

#browser.implicitly_wait(6)
browser = webdriver.Chrome("/Users/-/Dropbox/Python and SQL/chromedriver")
browser.get('http://www.metacritic.com')

#####Spaghetti 
film_list_hyphens = film_list.copy()
reviews_list_hyphens = film_list.copy()
#film_list_hyphens[0] = film_list_hyphens[0].lower()
for x in range(0,len(film_list_hyphens)):
    film_list_hyphens[x] = film_list_hyphens[x].replace(" ","-")
    film_list_hyphens[x] = film_list_hyphens[x].replace(":","")
    film_list_hyphens[x] = film_list_hyphens[x].replace(".","")
    film_list_hyphens[x] = film_list_hyphens[x].replace(",","")
    film_list_hyphens[x] = film_list_hyphens[x].replace("'","")
    film_list_hyphens[x] = film_list_hyphens[x].replace("& ","")
    film_list_hyphens[x] = film_list_hyphens[x].lower()
film_list_links = [None] * len(film_list_hyphens)
for x in range(0,len(film_list_hyphens)):
    reviews_list_hyphens[x] = "https://www.metacritic.com/movie/" + film_list_hyphens[x] +  "/critic-reviews"
    film_list_hyphens[x] = "https://www.metacritic.com/movie/" + film_list_hyphens[x]

browser = webdriver.Chrome("/Users/-/Dropbox/Python and SQL/chromedriver")
browser.get('http://www.metacritic.com')
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
browser.implicitly_wait(3)   
review_pages = [None] * len(film_list)
film_pages = [None] * len(film_list)
error_index = list()
for x in range(0, len(film_list)):   #edited to continue search
    try:
        review_pages[x] = requests.get(film_list_links[x], headers=headers)
        if review_pages[x].status_code != 200:
            searchBar = browser.find_element_by_id('primary_search_box')
            searchBar.send_keys(film_list[x])
            time.sleep(3)     
            elem = browser.find_elements_by_class_name('search_results_item')
            if len(elem)>0:
                elem[0].click()
                time.sleep(3) 
                critics_url = browser.current_url + '/critic-reviews'
                review_pages[x] = requests.get(critics_url, headers=headers)
                soup = BeautifulSoup(review_pages[x].content, 'html.parser')
                header_check = soup.select("a > h1")
                header_check = str(header_check)
                header_check = header_check.partition('</h1>')[0]
                header_check = header_check.partition('<h1>')[2]
                if header_check != film_list[x]:
                    review_pages[x] = "Non-matching page"
            else: 
                review_pages[x] = "No page found"
                searchBar.send_keys(100 * Keys.BACKSPACE)
                time.sleep(2)
    except (Exception, RuntimeError, ConnectionError):
        error_index.append(x)
        continue
    
restart = review_pages.index(None) #save loop starting value           
            
page = requests.get('https://www.metacritic.com/movie/x-men-apocalypse/critic-reviews', headers=headers)            
page.status_code        
soup = BeautifulSoup(page.content, 'html.parser')
header_check = soup.select("a > h1")
header_check = str(header_check)
header_check = header_check.partition('</h1>')[0]
header_check = header_check.partition('<h1>')[2]

####Old get.request version
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
review_pages = [None] * len(full_films_title)
browser.implicitly_wait(3)
for x in range(0, len(full_films_title)):
    searchBar = browser.find_element_by_id('primary_search_box')
    searchBar.send_keys(full_films_title[x])
    time.sleep(3)
    elem = browser.find_elements_by_class_name('search_results_item')
    #elem = browser.find.elements_by_link_text(full_films_title[x]) #doesnt work here
    if len(elem)>0:
        elem[0].click()
        critics_url = browser.current_url + '/critic-reviews'
        review_pages[x] = requests.get(critics_url, headers=headers)
    else: 
        review_pages[x] = "DeleteMe"
        searchBar.send_keys(60 * Keys.BACKSPACE)
    time.sleep(2)
####  PROBLEM X-Men is not the first result when searching for x-men
   ### change to look for exact title  
## Unresolved -- consider adding match check between search item and title on page. ### DO THIS regardless ####
## try to convert title into url with hyphens. if it doesn't work can retry. 


searchBar = browser.find_element_by_id('primary_search_box')
searchBar.send_keys(full_films_title[18])
#browser.switch_to.frame(1)
elem = browser.find_element_by_link_text(full_films_title[18])
elem = browser.find_element_by_link_text("2000")
browser.find_element_by_xpath('..//*[text()=full_films_title[18]]').click()
browser.find_element_by_xpath('..//*[@data-mctitle=full_films_title[18]]').click()
browser.find_element_by_xpath('//span[@class='title']/[@data-mctitle=full_films_title[18]]')
title = "X-Men"
year = "2000"
browser.find_element_by_xpath("//span[text()=year]").click()
browser.find_element_by_xpath("//span[text()='2000']").click()
browser.find_element_by_xpath("//b[text()='X-Men']")
browser.find_element(:link_text, full_films_title[18])
browser.findElement(By.linkText(full_films_title[18]))

if len(elem)>0:
    print("1 - Got a true expression value")
else: 
    print("Empty")
    
page = requests.get("https://www.metacritic.com/movie/the-shawshank-redemption/critic-reviews", headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')
print(soup.prettify())
junk2 = soup.find(class_='critic_reviews')
len(junk2)
type(junk2)
junk2[0]
list(soup.children)
junk2 = soup.find_all(class_='review pad_top1 pad_btm1')

soup = BeautifulSoup(review_pages[3].content, 'html.parser')
junk3 = soup.find_all(class_='review pad_top1 pad_btm1')
len(junk3)


## try exporting big html list

import csv
with open("film_html.csv", "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerows(review_pages)