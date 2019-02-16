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
    
    imdb_page_1 = "https://www.imdb.com/search/title?title_type=feature&release_date=" + 
    str(y1) + "-01-01," + str(y1) + 
    "-12-31&view=simple&sort=boxoffice_gross_us,desc&count=250&page=1&ref_=adv_nxt"
    
    imdb_page_2 = "https://www.imdb.com/search/title?title_type=feature&release_date=" + 
    str(y1) + "-01-01," + str(y1) + 
    "-12-31&view=simple&sort=boxoffice_gross_us,desc&count=250&start=251&ref_=adv_nxt"
    
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
    reviews_list_hyphens[x] = "https://www.metacritic.com/movie/" + film_list_hyphens[x] +  
    "/critic-reviews"
    film_list_hyphens[x] = "https://www.metacritic.com/movie/" + film_list_hyphens[x]

browser = webdriver.Chrome("/Users/Justin/Dropbox/Python and SQL/chromedriver")
browser.get('http://www.metacritic.com/movies')
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

browser.implicitly_wait(3)   
review_pages = [None] * len(film_list)
film_pages = [None] * len(film_list)
error_index = list()
for x in tqdm(range(0, len(film_list))):   #edited to continue search
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
import shelve 
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

#Database NOTE: authors with middle names listed are included within Last_name 
#(e.g., "Joy - Gould Boyum")
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
genre_film_unique_error = list()
for x in tqdm(range(579, len(film_pages))):   
##Reset temp_variables
    temp_film_title = None; temp_film_release_date = None; temp_film_runtime = None
    temp_film_genre_list = None; temp_reviews_name_list = None; temp_reviews_ratings_list = None

    if film_pages[x] is not None:
        ## Parse film html for webscraping
        film_soup = BeautifulSoup(film_pages[x].content, 'html.parser')
        if len(film_soup) > 0:
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
                    c.execute('INSERT INTO genre (genre_label) VALUES (?)', 
                              [temp_film_genre_list[i]])
                ## For updating the film_genre table -- retrieve film_id
                c.execute('SELECT film_id FROM film WHERE film_title=? AND film_release_date=?', 
                          [temp_film_title, temp_film_release_date])
                db_get_film_id = c.fetchone()
                ## For updating the film_genre table -- retrieve genre_id
                c.execute('SELECT genre_id FROM genre WHERE genre_label=?', 
                          [temp_film_genre_list[i]])
                db_get_genre_id = c.fetchone()   
                ## Update the film_genre table -- for each genre i and film x
                try:
                    c.execute("""
                              INSERT INTO film_genre
                              (film_id, genre_id) 
                              VALUES (?,?)""", [db_get_film_id[0], db_get_genre_id[0]])
                except:
                    genre_film_unique_error.append(x)
            ## Parse reviews html for webscraping
            reviews_soup = BeautifulSoup(review_pages[x].content, 'html.parser')
            ## Scrape author names and ratings for each review of film x 
            temp_reviews_name_list = scrape_reviews_auth_name_list(reviews_soup)
            temp_reviews_ratings_list = scrape_reviews_rating_list(reviews_soup)
            ##For each review check if author name exists in author table and update table if not
            for j in range(0, len(temp_reviews_name_list)): #NOTE: name j refers to current reviewer name
                ## If the review is credited to an author
                if temp_reviews_name_list[j] is not None:
                    c.execute('SELECT * FROM author WHERE last_name=? AND first_name=?', 
                              temp_reviews_name_list[j])
                    db_check_author = c.fetchone()
                    ## If author j doesn't exist yet insert it into the author table
                    if db_check_author is None: 
                        c.execute('INSERT INTO author (last_name, first_name) VALUES (?,?)', 
                                  temp_reviews_name_list[j])
                    ## For updating the review table -- retrieve film_id
                    c.execute('SELECT film_id FROM film WHERE film_title=? AND film_release_date=?', 
                              [temp_film_title, temp_film_release_date])
                    db_get_film_id = c.fetchone()
                    ## For updating the review table -- retrieve author_id
                    c.execute('SELECT author_id FROM author WHERE last_name=? AND first_name=?', 
                              temp_reviews_name_list[j])
                    db_get_author_id = c.fetchone()
                    ## update review table for review j and film x
                    c.execute("""
                        INSERT OR IGNORE INTO review
                        (film_id, author_id, rating) 
                        VALUES (?,?,?)""", [db_get_film_id[0], db_get_author_id[0], 
                        temp_reviews_ratings_list[j]])
                ## If the review is NOT credited to an author 
                else: 
                    ## create a new author_id for the uncredited review author
                    c.execute('INSERT INTO author (last_name, first_name) VALUES (?,?)', 
                              ("Uncredited", "Uncredited"))
                    ## For updating the review table -- retrieve film_id
                    c.execute('SELECT film_id FROM film WHERE film_title=? AND film_release_date=?', 
                              [temp_film_title, temp_film_release_date])
                    db_get_film_id = c.fetchone()
                    ## For updating the review table -- retrieve author_id
                    c.execute('SELECT MAX(author_id) FROM author')
                    db_get_author_id = c.fetchone()
    

###check db
conn.commit()    
df = pd.read_sql_query("""
    SELECT *
    FROM film
    --WHERE film_id = 579
""", conn)    
df = pd.read_sql_query("""
    SELECT COUNT(*), genre_label
    FROM film_genre INNER JOIN genre USING(genre_id)
    GROUP BY genre_id
""", conn)   
df = pd.read_sql_query("""
    SELECT COUNT(*) as count, author_id, first_name, last_name
    FROM review INNER JOIN author USING(author_id)
    GROUP BY author_id
    ORDER BY count DESC
""", conn)   
df = pd.read_sql_query("""
    SELECT *
    FROM author
""", conn)   
df = pd.read_sql_query("""
    SELECT *
    FROM review
""", conn)   

##load copy of film_and_reviews database
conn = sqlite3.connect("films_and_reviews.db")
conn = sqlite3.connect("C:/Users/Justin/Desktop/Projects/wisdom-of-the-tribe/films_and_reviews.db")
c = conn.cursor()

import pandas as pd
import numpy as np
import scipy as sp
import plotly.plotly as py
import plotly.figure_factory as ff
import plotly 
plotly.tools.set_credentials_file(username='jolds', api_key='QmM7nk1rNElpcqKM4o3I')

#save total number of films
df = pd.read_sql_query("""
    SELECT film_title, AVG(rating) AS RatingAVG, film_release_date, film_runtime, film_id
    FROM film INNER JOIN review USING(film_id)
    GROUP BY film_id
""", conn)   
no_films = len(df)
film_ids = tuple(df.film_id)
by_film={}
for x in film_ids:
    by_film[x]=None
titles = []
for x in film_ids:
    c.execute('SELECT rating FROM review INNER JOIN film USING(film_id) WHERE film_id=?', [x])
    temp_ratings = c.fetchall()
    temp_ratings_tuple = tuple([x[0] for x in temp_ratings])
    if len(temp_ratings) > 4:
        by_film[x]=temp_ratings_tuple
        c.execute('SELECT film_title FROM film WHERE film_id=?', [x])
        temp_title = c.fetchone()
        titles.append(temp_title)
    else:
        del by_film[x]
        
ratings_array = np.array()
hist_data = []
for x in by_film:
    hist_data.append(np.array(by_film[x]))
fig = ff.create_distplot([hist_data[0]], titles[0], curve_type='normal')
plotly.offline.plot(fig, filename='Distplot with Multiple Datasets')

import matplotlib.pyplot as plt
import seaborn as sns
df = sns.load_dataset('iris')
 
# Just switch x and y
plt.figure(figsize=(30 ,20))
df = pd.read_sql_query("""
    SELECT film_title, rating
    FROM film INNER JOIN review USING(film_id)
    WHERE film_id < 50
""", conn)   
sns.violinplot(y=df['film_title'], x=df['rating'])
#sns.plt.show()

# Add title
fig['layout'].update(title='Curve and Rug Plot')

# Plot!
py.iplot(fig, filename='Curve and Rug')

c.execute('SELECT rating FROM review INNER JOIN film USING(film_id) WHERE film_id=1')

df = pd.DataFrame({'2012': np.random.randn(201),
                   '2013': np.random.randn(200)+1})
py.plot(ff.create_distplot([df[c] for c in df.columns], df.columns, bin_size=.25),
                            filename='distplot with pandas')
### To start plot all film averages

x2 = np.random.randn(200)


import plotly
import plotly.figure_factory as ff
plotly.offline.init_notebook_mode()
import numpy as np

# data with different sizes
x1 = np.random.randn(3)-2  
x2 = np.random.randn(200)  
x3 = np.random.randn(4000)+2  
x4 = np.random.randn(50)+4  

# Group data together
hist_data = [x1, x2, x3, x4]

# use custom names
group_labels = ['x1', 'x2', 'x3', 'x4']

# Create distplot with custom bin_size
fig = ff.create_distplot(hist_data, group_labels, bin_size=.2)

# change that if you don't want to plot offline
plotly.offline.plot(fig, filename='Distplot with Multiple Datasets')

##boxplots by film
# library & dataset

film_averages = pd.read_sql_query("""
    SELECT film_title, AVG(rating) AS RatingAVG, COUNT(*) as count, 
           film_release_date, film_runtime, film_id
           
    FROM film INNER JOIN review USING(film_id)
    
    GROUP BY film_id
""", conn)
fig = plt.hist(film_averages['count'], bins=40, color='#1c819e', 
               edgecolor='black', linewidth=1.2)
fig[0]
               
reviews = pd.read_sql_query("""
    SELECT *
    FROM review 
""", conn)
print('\nMean of mean film ratings:')
print(np.mean(film_averages[['RatingAVG']]))

print('\nStandard Deviation of mean film ratings:')
print(np.std(film_averages[['RatingAVG']]))
plt.hist(film_averages['RatingAVG'], normed=True, bins=50)
hist = film_averages['RatingAVG'].hist(bins=100)
g = film_averages.groupby('RatingAVG')
info = g['RatingAVG'].agg(['sum','count']).reset_index()

plt.plot(info['RatingAVG'], savgol_filter(info['count'], 5, 1), label = 'Mean film rating') 
plt.xlabel('Rating')
plt.ylabel('Frequency')
plt.show()

import plotly.plotly as py
import plotly.tools as tls

import matplotlib.pyplot as plt
import numpy as np
plt.hist(film_averages['RatingAVG'])
fig = plt.gcf()
plotly_fig = tls.mpl_to_plotly(fig)
py.iplot(plotly_fig, filename='mpl-basic-histogram')

film_averages = pd.read_sql_query("""
    SELECT film_title, AVG(rating) AS RatingAVG, COUNT(*) as count, 
    film_release_date, film_runtime, film_id
    FROM film INNER JOIN review USING(film_id)
    GROUP BY film_id
""", conn)

SDvalues = list()
import statistics as stats
for x in film_averages['film_id']:
    c.execute('SELECT rating FROM review INNER JOIN film USING(film_id) WHERE film_id=?', [x])
    individ_film_reviews = c.fetchall()
    temp_ratings_tuple = tuple([x[0] for x in individ_film_reviews])
    try:
        SDvalues.append(stats.stdev(temp_ratings_tuple))
    except:
        SDvalues.append(None)

film_averages = film_averages.assign(SD=SDvalues)

films_filt = film_averages.where(film_averages['count']>5)
films_filt = films_filt.dropna(0)
plt.hist(films_filt['SD'], bins=40, color='#1c819e', edgecolor='black', linewidth=1.2)
plt.xlabel('Rating')
plt.ylabel('Frequency')
plt.axvline(x=np.mean(films_filt['SD']), color="#ffbe00", linewidth=4.5, 
            label='Mean = {0:.1f}'.format(np.mean(films_filt['SD'])))
plt.axvline(x=np.median(films_filt['SD']), color="#89a4c7", linewidth=4.5, 
            label='Median = {0:.1f}'.format(np.median(films_filt['SD'])))
plt.legend()
plt.show()
    
by_author = pd.read_sql_query("""
    SELECT AVG(rating) AS RatingAVG, COUNT(*) as count, author_id, first_name, last_name
    FROM review INNER JOIN author USING(author_id)
    GROUP BY author_id
""", conn)
by_author_filt = by_author.where(by_author['count']>5)
by_author_filt = by_author_filt.dropna(0)
#by_author_filt.reset_index(drop=True)
by_author_filt.set_index('author_id', inplace=True, drop=False)
SDvalues2 = list()
for x in by_author_filt['author_id']:
    #print(x)
    c.execute('SELECT rating FROM review INNER JOIN author USING(author_id) 
    WHERE author_id=?', [x])
    individ_film_reviews = c.fetchall()
    temp_ratings_tuple = tuple([x[0] for x in individ_film_reviews])
    try:
        SDvalues2.append(stats.stdev(temp_ratings_tuple))
    except:
        SDvalues2.append(None)
SDdf = pd.DataFrame(SDvalues2, columns=['SD'])
SDdf.set_index(by_author_filt['author_id'], inplace=True)
by_author_filt['SD'] = SDdf['SD']
by_author_filt2 = by_author_filt.sort_values(['SD'],ascending=False)

by_author_filt2 = by_author_filt2.where(by_author_filt2['SD']>30)
by_author_filt2 = by_author_filt2.dropna(0)


#### add columns to sql tables -- author: author_rating_avg, 
###author_rating_sd, total_score, score_count, pref_aff
## film: film_rating_avg, film_rating_sd
#conn = sqlite3.connect("films_and_reviews.db")
import sqlite3
import pandas as pd
from datetime import datetime

conn = sqlite3.connect("films_and_reviews3.db")
c = conn.cursor()

c.execute('ALTER TABLE author ADD review_count INTEGER')
c.execute('ALTER TABLE author ADD author_rating_avg REAL')
c.execute('ALTER TABLE author ADD author_rating_sd REAL')
c.execute('ALTER TABLE author ADD total_score REAL')
c.execute('ALTER TABLE author ADD score_count REAL')
c.execute('ALTER TABLE author ADD pref_aff REAL')
c.execute('ALTER TABLE film ADD film_rating_avg REAL')
c.execute('ALTER TABLE film ADD film_rating_sd REAL')
### create index for film_id and author_id
c.execute('CREATE UNIQUE INDEX idx_film_id ON film (film_id)')
c.execute('CREATE UNIQUE INDEX idx_author_id ON author (author_id)')
c.execute('CREATE UNIQUE INDEX idx_author_film ON review (film_id, author_id)')
conn.commit()    
### saved as 'films_and_reviews3.db'
#conn = sqlite3.connect("films_and_reviews3_clean.db")
conn = sqlite3.connect("films_and_reviews3.db")

## check for new columns:
df = pd.read_sql_query("""
    SELECT *
    FROM author
""", conn)   

### create loop to generate film_rating_avg & film_rating_sd values 
### same for author: review_count, author_rating_avg, author_rating_sd
##step 1: get all film_id values to build loop
df = pd.read_sql_query("""
    SELECT film_id
    FROM film
""", conn)   
film_ids = df['film_id']
film_ids_tuple = tuple([x for x in df['film_id']]) ## convert to tuple

import statistics as stats
error_list = list()
for x in film_ids_tuple: 
    c.execute('SELECT rating FROM review INNER JOIN film USING(film_id) WHERE film_id=?', [x])
    individ_film_reviews = c.fetchall()
    temp_ratings_tuple = tuple([x[0] for x in individ_film_reviews])
    try:
        c.execute('UPDATE film SET film_rating_avg= ?, film_rating_sd=? WHERE film_id = ?', 
                  [stats.mean(temp_ratings_tuple), stats.stdev(temp_ratings_tuple), x])
    except:
        error_list.append(x)
        
###author summary stats
df = pd.read_sql_query("""
    SELECT author_id
    FROM author
""", conn)   
author_ids = df['author_id']
author_ids_tuple = tuple([x for x in df['author_id']]) ## convert to tuple

import statistics as stats
error_list2 = list()
for x in author_ids_tuple: 
    c.execute('SELECT rating FROM review WHERE author_id=?', [x])
    individ_film_reviews = c.fetchall()
    temp_ratings_tuple = tuple([x[0] for x in individ_film_reviews])
    try:
        c.execute('UPDATE author SET author_rating_avg= ?, author_rating_sd=?, review_count = ? WHERE author_id = ?', 
                  [stats.mean(temp_ratings_tuple), stats.stdev(temp_ratings_tuple), len(temp_ratings_tuple), x])
    except:
        error_list2.append(x)
        
        
print(sqlite3.paramstyle)
df = pd.read_sql_query("""
    SELECT *
    FROM review INNER JOIN author USING(author_id)
    WHERE author.review_count > 1
""", conn) 

c.execute('PRAGMA table_info(author)')
c.fetchall()
c.execute('INSERT INTO film (film_rating_avg) VALUES (?)', [stats.mean(temp_ratings_tuple)])
 

#### generate example user ratings update loop over all relevant authors

### use average film rating and average film sd to compute z scores for user ratings
film_averages = pd.read_sql_query("""
    SELECT film_title, AVG(rating) AS RatingAVG, COUNT(*) as count, 
           film_release_date, film_runtime, film_id
    FROM film INNER JOIN review USING(film_id)
    GROUP BY film_id
""", conn)
avg0 = np.mean(film_averages['RatingAVG']);sd0 = np.std(film_averages['RatingAVG'])
ex_film = "Evil Dead II"; ex_rating = 80
ex_film = "On Golden Pond"; ex_rating = 95
ex_df = pd.read_sql_query("""
    SELECT *
    FROM review INNER JOIN film USING(film_id) INNER JOIN author USING(author_id)
    WHERE film_title=? AND review_count > 1
""", conn, params=[ex_film]) 

### clear author scores 
c.execute('UPDATE author SET total_score = NULL, score_count = NULL, pref_aff = NULL')
##this will will need to be nested into another loop with x for each user film rating
for x in range(len(ex_df)):
    #print(ex_df['rating'][x])
    user_z = (ex_rating-avg0)/sd0
    by_film_points = user_z * (ex_df['rating'][x]-ex_df['film_rating_avg'][x])/ex_df['film_rating_sd'][x]
    by_author_points = user_z * (ex_df['rating'][x]-ex_df['author_rating_avg'][x])/ex_df['author_rating_sd'][x]
    temp_score = (by_film_points + by_author_points)/2 ##update db
    ### get total_score from SELECT by author and update + temp_score
    if ex_df['total_score'][x] is not None:
        ex_df.loc[x, 'total_score'] = ex_df.loc[x, 'total_score'] + temp_score
    else: 
        ex_df.loc[x, 'total_score'] = temp_score
    if ex_df['score_count'][x] is not None:
        ex_df.loc[x, 'score_count'] = ex_df.loc[x, 'score_count'] + 1
    else: 
        ex_df.loc[x, 'score_count'] = 1
    ex_df.loc[x, 'pref_aff'] = ex_df.loc[x, 'total_score'] / ex_df.loc[x, 'score_count']   
    c.execute('''UPDATE author 
              SET total_score = ?, score_count = ?, pref_aff = ? 
              WHERE author_id =?''', [ex_df.at[x, 'total_score'], ex_df.at[x, 'score_count'],ex_df.at[x, 'pref_aff'],ex_df.at[x, 'author_id'])])
    ### get score_count from SELECT by author
    ### update score_count by adding 1 to 

### get list of films to update  
update_df = pd.read_sql_query('''
                SELECT * 
                FROM review INNER JOIN author USING(author_id) INNER JOIN film USING(film_id)
                WHERE pref_aff > 0
                GROUP BY film_id''', conn)
#set index to film_ids
update_df.set_index('film_id', inplace=True, drop=False)
#create tribe rating column
update_df['tribe_rating'] = None
### calc tribe ratings 
for x in update_df['film_id']:
    ##get by film reviews for each tribe member
    temp_df = \
    pd.read_sql_query("""
                      SELECT *
                      FROM review INNER JOIN author USING(author_id) INNER JOIN film USING(film_id)
                      WHERE film_id=? AND pref_aff > 0
                      """, conn, params=[x]) 
    ### normalize pref_aff weights to sum to number of tribe members
    normer = len(temp_df)/sum(temp_df['pref_aff'])
    temp_df['n_pref_aff']= normer * temp_df['pref_aff']
    tribe_rating = sum(temp_df['rating'] * temp_df['n_pref_aff'])/sum(temp_df['n_pref_aff'])
    update_df.loc[x, 'tribe_rating'] = tribe_rating


### ROLLBACK
c.execute('ROLLBACK')

##hist of pref_aff after 1 rating
author_df = pd.read_sql_query('''
                SELECT * 
                FROM author
                WHERE pref_aff > 0 OR pref_aff < 0
                ''', conn)
##replace nan values with 0
author_df['pref_aff'].fillna(0, inplace=True)
##plot hist
plt.hist(author_df['pref_aff'], bins=40, color='#1c819e', edgecolor='black', linewidth=1.2)

plt.xlabel('Preference Affinity')
plt.ylabel('Frequency')
#plt.axvline(x=np.mean(films_filt['SD']), color="#ffbe00", linewidth=4.5, label='Mean = {0:.1f}'.format(np.mean(films_filt['SD'])))
#plt.axvline(x=np.median(films_filt['SD']), color="#89a4c7", linewidth=4.5, label='Median = {0:.1f}'.format(np.median(films_filt['SD'])))
#plt.legend()
plt.show()
##correlation spaghetti 
import math as m
user=-.6; auth=.5
(user*auth)/m.sqrt((m.pow(user,2))*(m.pow(auth,2)))
m.pow(.45,2)

type(ex_df.loc[x, 'total_score'])

##overall film ratings used to compute user z-scores


###
film_averages = pd.read_sql_query("""
    SELECT film_title, AVG(rating) AS RatingAVG, COUNT(*) as count, film_release_date, film_runtime, film_id
    FROM film INNER JOIN review USING(film_id)
    GROUP BY film_id
""", conn)
overall_film_mean = stats.mean(film_averages['RatingAVG'])
overall_film_sd = stats.stdev(film_averages['RatingAVG'])

def pref_update(film_, rating_):
    ex_df = pd.read_sql_query("""
    SELECT *
    FROM review INNER JOIN film USING(film_id) INNER JOIN author USING(author_id)
    WHERE film_title=? AND review_count > 1
    ORDER BY rating DESC
    """, conn, params=[film_])
    #print('Updating preferences based on {0} Rating = {1}').format(film_,rating_)
    #loop across all author ratings (x) for film 
    for x in range(len(ex_df)):
        user_z = (rating_-overall_film_mean)/overall_film_sd
        by_film_points = user_z * (ex_df['rating'][x]-ex_df['film_rating_avg'][x])/ex_df['film_rating_sd'][x]
        by_author_points = user_z * (ex_df['rating'][x]-ex_df['author_rating_avg'][x])/ex_df['author_rating_sd'][x]
        temp_score = (by_film_points + by_author_points)/2
        ### get total_score from SELECT by author and update + temp_score
        if ex_df['total_score'][x] is not None:
            ex_df.loc[x, 'total_score'] = ex_df.loc[x, 'total_score'] + temp_score
        else: 
            ex_df.loc[x, 'total_score'] = temp_score
        if ex_df['score_count'][x] is not None:
            ex_df.loc[x, 'score_count'] = ex_df.loc[x, 'score_count'] + 1
        else: 
            ex_df.loc[x, 'score_count'] = 1
        ex_df.loc[x, 'pref_aff'] = ex_df.loc[x, 'total_score'] / ex_df.loc[x, 'score_count']
        c.execute('''UPDATE author 
                  SET total_score = ?, score_count = ?, pref_aff = ? 
                  WHERE author_id =?''', [ex_df.loc[x, 'total_score'], int(ex_df.loc[x, 'score_count']),ex_df.loc[x, 'pref_aff'],int(ex_df.loc[x, 'author_id'])])


pref_update("The Green Mile", 90)
c.execute('UPDATE author SET total_score = NULL, score_count = 0, pref_aff = NULL')
author_df = pd.read_sql_query('''
                SELECT * 
                FROM author
                WHERE author_id = 1205
                ''', conn)


##overall film ratings used to compute user z-scores
overall_film_mean = stats.mean(film_averages['RatingAVG'])
overall_film_sd = stats.stdev(film_averages['RatingAVG'])
#film_="The Green Mile"
#rating_=90
x=35

def pref_update(film_, rating_):
    ex_df = pd.read_sql_query("""
    SELECT *
    FROM review INNER JOIN film USING(film_id) INNER JOIN author USING(author_id)
    WHERE film_title=? AND review_count > 1
    ORDER BY rating DESC
    """, conn, params=[film_])
    #print('Updating preferences based on {0} Rating = {1}').format(film_,rating_)
    #loop across all author ratings (x) for film 
    for x in range(len(ex_df)):
        user_z = (rating_-overall_film_mean)/overall_film_sd
        by_film_points = user_z * (ex_df['rating'][x]-ex_df['film_rating_avg'][x])/ex_df['film_rating_sd'][x]
        by_author_points = user_z * (ex_df['rating'][x]-ex_df['author_rating_avg'][x])/ex_df['author_rating_sd'][x]
        temp_score = (by_film_points + by_author_points)/2
        ### get total_score from SELECT by author and update + temp_score
        if ex_df['total_score'][x] is not None:
            ex_df.loc[x, 'total_score'] = ex_df.loc[x, 'total_score'] + temp_score
        else: 
            ex_df.loc[x, 'total_score'] = temp_score
        if ex_df['score_count'][x] is not None:
            ex_df.loc[x, 'score_count'] = ex_df.loc[x, 'score_count'] + 1
        else: 
            ex_df.loc[x, 'score_count'] = int(1)
        ex_df.loc[x, 'pref_aff'] = ex_df.loc[x, 'total_score'] / ex_df.loc[x, 'score_count']
        update_total_score = ex_df.at[x, 'total_score']
        update_score_count = ex_df.at[x, 'score_count']
        update_pref_aff = ex_df.at[x, 'pref_aff']
        update_author_id = int(ex_df.at[x, 'author_id'])
        c.execute('''UPDATE author 
                  SET total_score = ?, score_count = ?, pref_aff = ? 
                  WHERE author_id =?''', [update_total_score, update_score_count, update_pref_aff,update_author_id])
    author_df = pd.read_sql_query('''
                SELECT * 
                FROM author
                WHERE pref_aff > 0 OR pref_aff < 0
                ORDER BY pref_aff DESC
                ''', conn)    
    return(author_df)    
    
SDvalues = list()
import statistics as stats
for x in film_averages['film_id']:
    c.execute('SELECT rating FROM review INNER JOIN film USING(film_id) WHERE film_id=?', [x])
    individ_film_reviews = c.fetchall()
    temp_ratings_tuple = tuple([x[0] for x in individ_film_reviews])
    try:
        SDvalues.append(stats.stdev(temp_ratings_tuple))
    except:
        SDvalues.append(None)
film_averages = film_averages.assign(SD=SDvalues)
films_filt = film_averages.where(film_averages['count']>5)
films_filt = films_filt.dropna(0)
showme = films_filt[['film_title','film_release_date','count', 'SD']]


###load movielens user reviews

sqlite3.connect(':memory:')
fd = open('movielens1.sql', 'r')
script = fd.read()
c.executescript(script)
fd.close()
c.execute('PRAGMA table_info(Movies)');c.fetchall()
users