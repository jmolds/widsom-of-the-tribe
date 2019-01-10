import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import IPython
from IPython.display import HTML
from IPython.display import display
import requests
from bs4 import BeautifulSoup
import time
from tqdm import tqdm
import csv

####copy code for imdb
film_list = list()
films_per_page_range = range(0,250)
temp_films_list1 = [None] * len(films_per_page_range)
temp_films_list2 = [None] * len(films_per_page_range)
year_range = range(1980,2018)
for year in tqdm(year_range):
    y1 = year
    imdb_page_1 = "https://www.imdb.com/search/title?title_type=feature&release_date=" + str(y1) + "-01-01," + str(y1) + "-12-31&view=simple&sort=boxoffice_gross_us,desc&count=250&page=1&ref_=adv_nxt"
    imdb_page_2 = "https://www.imdb.com/search/title?title_type=feature&release_date=" + str(y1) + "-01-01," + str(y1) + "-12-31&view=simple&sort=boxoffice_gross_us,desc&count=250&start=251&ref_=adv_nxt"
    #imdb_page_2 = "https://www.imdb.com/search/title?title_type=feature&release_date=" + str(y1) + "-01-01," + str(y1) + "-12-31&view=simple&sort=boxoffice_gross_us,desc&count=250&page=2&ref_=adv_nxt"
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
    
for x in range(0,len(film_list)):
    film_list[x] = film_list[x].replace("amp;","")

###Export film list as csv

#with open('C:/Users/Justin/Dropbox/Python and SQL/film_list.csv', 'w', newline='') as myfile:
#    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
#    for x in range(0,len(film_list)):
#        wr.writerow([film_list[x]])
       
film_list = []
with open('C:/Users/Justin/Dropbox/Python and SQL/film_list.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        film_list.append(row[0])
        
        
####copy code for turning film titles into urls
    
#### EDIT FOR BOTH PAGES -- film (genre, runtime) & Reviews
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

browser = webdriver.Chrome("/Users/Justin/Dropbox/Python and SQL/chromedriver")
browser.get('http://www.metacritic.com/movies')
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

browser.implicitly_wait(3)   
review_pages = [None] * len(film_list)
film_pages = [None] * len(film_list)
error_index = list()
for x in tqdm(range(len(film_list))):   #edited to continue search
    if film_pages[x] is None: 
        try:
            review_pages[x] = requests.get(reviews_list_hyphens[x], headers=headers)       
            if review_pages[x].status_code != 200:
                searchBar = browser.find_element_by_id('primary_search_box')
                searchBar.send_keys(film_list[x])
                time.sleep(2)  
                elem = browser.find_elements_by_class_name('search_results_item')
                time.sleep(2)  
                if len(elem) > 0:
                    elem[0].click()
                    time.sleep(3) 
                    film_url = browser.current_url
                    critics_url = browser.current_url + '/critic-reviews'
                    review_pages[x] = requests.get(critics_url, headers=headers)
                    film_pages[x] = requests.get(film_url, headers=headers)
                    soup = BeautifulSoup(review_pages[x].content, 'html.parser')
                    header_check = soup.select("a > h1")
                    header_check = str(header_check)
                    header_check = header_check.partition('</h1>')[0]
                    header_check = header_check.partition('<h1>')[2]
                    if header_check != film_list[x]:
                        review_pages[x] = "No page found"
                        film_pages[x] = "No page found"
                else: 
                    review_pages[x] = "No page found" 
                    film_pages[x] = "No page found"
                    searchBar.send_keys(100 * Keys.BACKSPACE)
                    time.sleep(2)
            else:
                film_pages[x] = requests.get(film_list_hyphens[x], headers=headers)
        except (Exception, RuntimeError, ConnectionError):
            error_index.append(x)
            continue
    
restart = review_pages.index(None) #save loop starting value   

### save get.requests (film_pages & revew_pages) to shelve with error index
#import shelve 
#s = shelve.open("films.requests.dat") 
#s["film_pages"]= film_pages
#s["review_pages"]= review_pages
#s["error_index"]= error_index
#s.close() 

r = shelve.open("films.requests.dat") 
film_pages = r["film_pages"] 
review_pages = r["review_pages"] 
error_index = r["error_index"] 
r.close()

###Double check if missing or not found

###Throw out any missing film pages
#film_pages.append(None)
film_pages = [x for x in film_pages if x is not None]
review_pages = [x for x in review_pages if x is not None]
film_pages = [x for x in film_pages if "No page found" not in x]
review_pages = [x for x in review_pages if "No page found" not in x]


### Define functions for webscraping
def scrape_film_title(soup_source):
    scrape = soup_source.select("div > h1")
    scrape = str(scrape)
    scrape = scrape.partition('</h1>')[0]
    scrape = scrape.partition('<h1>')[2]
    return scrape
####returns string to be temporarily saved for db insert

def scrape_film_release_date(soup_source):
    scrape = soup_source.select("span.release_date")
    scrape = str(scrape)
    scrape = scrape.partition('</span>\n<span>')[2]
    scrape = scrape.partition('</span>')[0]
    scrape = datetime.strptime(scrape, "%B %d, %Y")
    scrape = scrape.strftime('%Y-%m-%d')
    return scrape


def scrape_film_runtime(soup_source):
    scrape = soup_source.select("div.runtime")
    scrape = str(scrape)
    scrape = scrape.partition('</span>\n<span>')[2]
    scrape = scrape.partition(' min</span>')[0]
    return scrape

def scrape_film_genre_list(soup_source):
    scrape = soup_source.select("div.genres > span")[1]
    scrape = scrape.select("span")
    for x in range(0, len(scrape)):
        scrape[x] = str(scrape[x])
        scrape[x] = scrape[x].partition('</span>')[0]
        scrape[x] = scrape[x].partition('<span>')[2]
    return scrape
##### Returns a list of strings. List length can vary depending on the number of listed genres

def scrape_reviews_auth_name_list(soup_source):
    scrape = soup_source.select("span.author")
    first_name_list = [None] * len(scrape)
    last_name_list = [None] * len(scrape)
    last_name_first_name_list = [None] * len(scrape)
    for x in range(0, len(scrape)):
        scrape[x] = str(scrape[x])
        scrape[x] = scrape[x].partition('author">')[2]
        if '<a href=' in scrape[x]:
            scrape[x] = scrape[x].partition('movies">')[2]
            scrape[x] = scrape[x].partition('</a></span>')[0]
        else:
            scrape[x] = scrape[x].partition('</span>')[0]
        if 'Staff' not in scrape[x]:
            first_name_list[x] = scrape[x].partition(' ')[0]
            last_name_list[x] = scrape[x].partition(' ')[2]
            last_name_first_name_list[x] = (last_name_list[x], first_name_list[x])
        else: 
            last_name_first_name_list[x] = None
    return (last_name_first_name_list)
#Database NOTE: authors with middle names listed are included within Last_name (e.g., "Joy - Gould Boyum")
#Returns tuple for last name and first name or None object if author is uncredited

def scrape_reviews_rating_list(soup_source):
    scrape = soup_source.select("div.left.fl")
    for x in range(0, len(scrape)):
        scrape[x] = str(scrape[x])
        scrape[x] = scrape[x].partition('</div>')[0]
        scrape[x] = scrape[x].partition('>')[2]
        scrape[x] = scrape[x].partition('>')[2]
    return scrape

###create DB tables
import sqlite3
import pandas as pd
from datetime import datetime

conn = sqlite3.connect("films_and_reviews.db")
c = conn.cursor()

####### create tables
c.execute('DROP TABLE IF EXISTS film')
c.execute('DROP TABLE IF EXISTS review') 
c.execute('DROP TABLE IF EXISTS author') 
c.execute('DROP TABLE IF EXISTS genre')
c.execute('DROP TABLE IF EXISTS film_genre')
 
c.execute("""
          CREATE TABLE film (
          film_id INTEGER PRIMARY KEY AUTOINCREMENT, 
          film_title TEXT, 
          film_release_date TEXT,
          film_runtime INTEGER
          )""")


c.execute("""
          CREATE TABLE genre (
          genre_id INTEGER PRIMARY KEY AUTOINCREMENT, 
          genre_label TEXT 
          )""")

c.execute("""
          CREATE TABLE film_genre (
          film_id REFERENCES film(film_id),
          genre_id REFERENCES review(genre_id), 
              CONSTRAINT film_genre_pk PRIMARY KEY (film_id, genre_id)
          )""")

c.execute("""
          CREATE TABLE review (
          film_id INTEGER, 
          author_id INTEGER,
          rating INTEGER,
              FOREIGN KEY (film_id) REFERENCES film(film_id)
              FOREIGN KEY (author_id) REFERENCES author(author_id)
              CONSTRAINT review_pk PRIMARY KEY (film_id, author_id)
          )""")

c.execute("""
          CREATE TABLE author (
          author_id INTEGER PRIMARY KEY AUTOINCREMENT,
          first_name TEXT, 
          last_name TEXT
          )""")


conn.commit()

###Loop for extracting attributes and inserting into db  
release_date_error = list()
runtime_error = list()
for x in tqdm(range(258, len(film_pages))):   
##Reset temp_variables
    temp_film_title = None; temp_film_release_date = None; temp_film_runtime = None
    temp_film_genre_list = None; temp_reviews_name_list = None; temp_reviews_ratings_list = None

    if film_pages[x] is not None: 
        ## Parse film html for webscraping
        film_soup = BeautifulSoup(film_pages[x].content, 'html.parser')
        ## Scrape title, release date and runtime and temporarily save for film x 
        temp_film_title = scrape_film_title(film_soup)
        try:
            temp_film_release_date = scrape_film_release_date(film_soup)
        except:
            temp_film_release_date = "NULL"
            error_index.append(x)
        try:
            temp_film_runtime = scrape_film_runtime(film_soup)
        except:
            temp_film_runtime = "NULL"
            runtime_error.append(x)    
        ## Insert film information into film table (no uniqueness checks required)
        c.execute("""
              INSERT INTO film
              (film_title, film_release_date, film_runtime) 
              VALUES (?,?,?)""", [temp_film_title, temp_film_release_date, temp_film_runtime])
        ## Scrape the list of genre labels for film x 
        temp_film_genre_list = scrape_film_genre_list(film_soup)
        ## check if each genre label exists and insert any new labels into the genre table
        for i in range(0, len(temp_film_genre_list)): #NOTE: genre i refers to current genre
            c.execute('SELECT * FROM genre WHERE genre_label=?', [temp_film_genre_list[i]])
            db_check_genre = c.fetchone()
            ## If genre label doesn't exist yet insert it into the genre table
            if db_check_genre is None: 
                c.execute('INSERT INTO genre (genre_label) VALUES (?)', [temp_film_genre_list[i]])
            ## For updating the film_genre table -- retrieve film_id
            c.execute('SELECT film_id FROM film WHERE film_title=? AND film_release_date=?', [temp_film_title, temp_film_release_date])
            db_get_film_id = c.fetchone()
            ## For updating the film_genre table -- retrieve genre_id
            c.execute('SELECT genre_id FROM genre WHERE genre_label=?', [temp_film_genre_list[i]])
            db_get_genre_id = c.fetchone()   
            ## Update the film_genre table -- for each genre i and film x
            c.execute("""
              INSERT INTO film_genre
              (film_id, genre_id) 
              VALUES (?,?)""", [db_get_film_id[0], db_get_genre_id[0]])
        ## Parse reviews html for webscraping
        reviews_soup = BeautifulSoup(review_pages[x].content, 'html.parser')
        ## Scrape author names and ratings for each review of film x 
        temp_reviews_name_list = scrape_reviews_auth_name_list(reviews_soup)
        temp_reviews_ratings_list = scrape_reviews_rating_list(reviews_soup)
        ##For each review check if author name exists in author table and update table if not
        for j in range(0, len(temp_reviews_name_list)): #NOTE: name j refers to current reviewer name
            ## If the review is credited to an author
            if temp_reviews_name_list[j] is not None:
                c.execute('SELECT * FROM author WHERE last_name=? AND first_name=?', temp_reviews_name_list[j])
                db_check_author = c.fetchone()
                ## If author j doesn't exist yet insert it into the author table
                if db_check_author is None: 
                    c.execute('INSERT INTO author (last_name, first_name) VALUES (?,?)', temp_reviews_name_list[j])
                ## For updating the review table -- retrieve film_id
                c.execute('SELECT film_id FROM film WHERE film_title=? AND film_release_date=?', [temp_film_title, temp_film_release_date])
                db_get_film_id = c.fetchone()
                ## For updating the review table -- retrieve author_id
                c.execute('SELECT author_id FROM author WHERE last_name=? AND first_name=?', temp_reviews_name_list[j])
                db_get_author_id = c.fetchone()
                ## update review table for review j and film x
                c.execute("""
                    INSERT OR IGNORE INTO review
                    (film_id, author_id, rating) 
                    VALUES (?,?,?)""", [db_get_film_id[0], db_get_author_id[0], temp_reviews_ratings_list[j]])
            ## If the review is NOT credited to an author 
            else: 
                ## create a new author_id for the uncredited review author
                c.execute('INSERT INTO author (last_name, first_name) VALUES (?,?)', ("Uncredited", "Uncredited"))
                ## For updating the review table -- retrieve film_id
                c.execute('SELECT film_id FROM film WHERE film_title=? AND film_release_date=?', [temp_film_title, temp_film_release_date])
                db_get_film_id = c.fetchone()
                ## For updating the review table -- retrieve author_id
                c.execute('SELECT MAX(author_id) FROM author')
                db_get_author_id = c.fetchone()


###check db
conn.commit()    
df = pd.read_sql_query("""
    SELECT *
    FROM film
""", conn)    
df = pd.read_sql_query("""
    SELECT *
    FROM genre
""", conn)   
df = pd.read_sql_query("""
    SELECT *
    FROM author
""", conn)   
df = pd.read_sql_query("""
    SELECT *
    FROM film_genre
""", conn)   
df = pd.read_sql_query("""
    SELECT *
    FROM review
""", conn)   



#### TESTING CODE
test_page = requests.get(reviews_list_hyphens[2], headers=headers)
elem = browser.find_elements_by_class_name('search_results_item')
len(elem)
review_pages[2].status_code
#### loop for scraping and inserting data in db



c.executemany('INSERT INTO q1_person_name(first_name, last_name) VALUES (?,?)', data_person_name)

c.execute("""
          INSERT INTO review
          (film_title, film_year, film_runtime, film_release_date) 
          VALUES (?,?,?,?)""", film_data)


c.execute("""
          INSERT INTO film
          (film_title, film_year, film_runtime, film_release_date) 
          VALUES (?,?,?,?)""", film_data)

c.execute("""INSERT INTO author
          (first_name, last_name) 
          VALUES (?,?)""", author_data)
author_data =("Sam", "Raimi")
curr_author = ("Jim", "Jarmusch")
curr_author = author_data
hi = c.execute("""
          SELECT auth_id
          FROM author
          WHERE first_name=? AND last_name=?
          """, curr_author).fetchone()
### None returned if no match. 
df = pd.read_sql_query("""
    SELECT *
    FROM author
""", conn)
df = pd.read_sql_query("""
    SELECT *
    FROM film
""", conn)
df[0,'fist_name':'last_name']
film_data = ["Evil Dead II", 1987, 90, "Yesterday"]
c.execute("INSERT INTO film VALUES (?,?,?,?,?)", film_data)
