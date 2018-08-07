import sqlite3
import xlrd
import pandas as pd

conn = sqlite3.connect('''drive2_data.sqlite''')
cur = conn.cursor()
cur.executescript('''
                DROP TABLE IF EXISTS TireBrands ;
                CREATE TABLE TireBrands (car_model TEXT, brand_name TEXT, count INTEGER)
            ''')

fname = "tireBrands.xlsx"
fh = xlrd.open_workbook(fname, encoding_override="cp1252")
sh = fh.sheet_by_index(0)
brands_list = dict()

for rx in range(sh.nrows): #create a dictionary from words list
    s_value = sh.cell_value(rx,0)
    brands_list[s_value] = 0
cur.execute('''SELECT model, body FROM pages''')
posts_body = cur.fetchall()
for x in posts_body: #loop through body html of the blog post which are stored in database
    model_name = x[0]
    blog_html = str(x[1])
    blog_html = blog_html.lower()
    for brand in brands_list:
        if blog_html.find(brand) > 0:
            cur.execute('''SELECT brand_name, count FROM TireBrands WHERE car_model = ? and brand_name = ?''', (model_name, brand))
            brand_data = cur.fetchone()
            if brand_data is None:
                cur.execute('''INSERT INTO TireBrands (car_model, brand_name, count) VALUES (?, ?, 1)''', (model_name, brand ))
            else:
                cur.execute('''UPDATE TireBrands SET count = count + 1 WHERE car_model = ? and brand_name = ?''', (model_name, brand))
conn.commit()

cur.execute('''SELECT car_model, brand_name, count body FROM TireBrands''')
dataset =  cur.fetchall()
df = pd.DataFrame(data=dataset, columns=['Car model','Tire brand','Mentions'])
df.head()
try:
    df.to_excel('Script result.xlsx', index=False)
    print('Done')
except:
    print('Cannot write to file')
conn.close()
