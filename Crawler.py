import sqlite3
import httplib2
from bs4 import BeautifulSoup
import re

#initilizing database
conn = sqlite3.connect('''drive2_data.sqlite''')
cur = conn.cursor()
cur.execute('''
    CREATE TABLE IF NOT EXISTS pages (Model TEXT, url TEXT, headers TEXT, body TEXT);
''')

model_url = '/experience/bmw/g2904/?t=20'
drive_domain = 'https://www.drive2.ru'

PostLinks = list()


while True:
    print('Running...')
    try:
        # connecting and parsing external data
        h = httplib2.Http(".cache")
        resp, content = h.request(drive_domain + model_url, "GET")
    except:
        print('Web address error')
    cur.execute('''SELECT url FROM pages WHERE url = ?''', (model_url,))
    link = cur.fetchone()
    if link is None:
        print('next page link:', model_url)
        cur.execute('''INSERT INTO pages (url) VALUES ( ? )''', (model_url,))
    else:
        print('All pages crawled')
        break

    soup = BeautifulSoup(content, "html.parser")

    links = soup('a')
    page_h1 = soup.h1.contents #find model name
    model_name = page_h1[4].strip() #and write it into variable
    for x in links: #crawling page for blog posts links and links to next pages
        try:
            if x['rel'][0] == 'next': #trying ot find links to next pages
                model_url = x['href']
            if len(x['class']) == 1 and x['class'][0] == 'c-link': #trying ot find all blogpost links according to page markup
                post_link = x['href']
                cur.execute('''SELECT url FROM pages WHERE url = ?''', ( post_link,))
                link = cur.fetchone()
                if link is None: #crawlong blogposts markup for futher manipulations
                    print('Crawling blog post')
                    post_resp, post_content = h.request(drive_domain + post_link, "GET")
                    post_soup = BeautifulSoup(post_content, "html.parser")
                    post_head = post_soup.head.contents
                    post_body = post_soup.body.contents
                    cur.execute('''INSERT INTO pages (Model,url, headers, body) VALUES ( ? , ? , ? , ?)''', (model_name, post_link, str(post_head), str(post_body)))
                    conn.commit()
        except:
            continue
    conn.commit()
conn.close()

