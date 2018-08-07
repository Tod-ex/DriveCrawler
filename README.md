# drive_crawler
This crawler is dedicated to search for keywords in Drive2 blogs. In order it to work you should specify blogpost section.
For example blogpost related to tires for BMW F21 https://www.drive2.ru/experience/bmw/g4008/?t=20
Crawler will get all head and body content of the blogposts and store them in SQLite database

Then run counter script to search blogpost for keywords from tireBrands.xlsx. Search results will be stored in Script-results.xlsx
