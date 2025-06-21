import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup


options = Options()
options.add_argument('--fasle')
chromedriver_path = "C:/Users/Cominn/Downloads/chromedriver-win64 (2)/chromedriver-win64/chromedriver.exe"
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service,options=options)




url = 'https://openlibrary.org/'
driver.get(url)

time.sleep(5) 
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

div = soup.find_all('div', class_='book-cover')
book_links = []
for links in div:
    a = links.find('a')
    if a and a.has_attr('href'):
        full_url = 'https://openlibrary.org'+a['href']
        book_links.append(full_url)

book_links = book_links[:30]
book_data = []
# for link in book_links:
#     print(f'visiting link is {link}')
#     driver.get(link)
#     time.sleep(3)
#     booksoup = BeautifulSoup(driver.page_source,'html.parser')
#     title = booksoup.find('h1',class_='work-title')
#     if title:
#         print('Title:', title.text.strip())
#     else:
#         'N/A'
#     aurthur = booksoup.find('h2',class_='edition-byline')
#     if aurthur:
#         print('Arthur name:', aurthur.text.strip())
#     else:
#         'N/A'
#     reviews = booksoup.find('li',class_='avg-ratings')
#     if reviews:
#         reviews = reviews.find('span',itemprop='ratingValue')
#         if reviews:
#            reviews = reviews.text.strip()
#            print(reviews)
#         else:
#             'N/A'
#     else:
#         'N/A'
#     book_data.append(
#         {
#             'Books Links':link,
#             'Title':title,
#             'Arthur':aurthur,
#             'Rating':reviews,

#         }
#     )
# driver.quit()


# df = pd.DataFrame(book_data)
# df.to_excel("openlibrary_books.xlsx", index=False)
# print('Data saved to excel file')

for link in book_links:
    print(f'Visiting: {link}')
    driver.get(link)
    time.sleep(2)
    booksoup = BeautifulSoup(driver.page_source, 'html.parser')

    # Extract title
    title_elem = booksoup.find('h1', class_='work-title')
    title = title_elem.text.strip() if title_elem else 'N/A'

    # Extract author
    author_elem = booksoup.find('h2', class_='edition-byline')
    author = author_elem.text.strip() if author_elem else 'N/A'

    # Extract rating
    rating = 'N/A'
    review_elem = booksoup.find('li', class_='avg-ratings')
    if review_elem:
        span = review_elem.find('span', itemprop='ratingValue')
        if span:
            rating = span.text.strip()

    print(f"Title: {title} | Author: {author} | Rating: {rating}")

    book_data.append({
        'Book Link': link,
        'Title': title,
        'Author': author,
        'Rating': rating
    })

driver.quit()

# Save to Excel
df = pd.DataFrame(book_data)
df.to_excel("openlibrary_books.xlsx", index=False)
print("Data saved to 'openlibrary_books.xlsx'")