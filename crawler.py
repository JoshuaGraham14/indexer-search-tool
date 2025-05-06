from bs4 import BeautifulSoup
import requests
import time

quotes_list = []
# 10 for 10 pages on site
for i in range(10):
    page = requests.get(f'https://quotes.toscrape.com/page/{i+1}/')

    soup = BeautifulSoup(page.content, "html.parser")
    quotes = soup.find_all('div', class_='quote')

    for quotes_div in quotes:
        quote_text = quotes_div.find('span', class_='text').get_text()
        quotes_list.append(quote_text)

    print(quotes_list)
    time.sleep(6) #6 seconds politness window.

print(quotes_list)