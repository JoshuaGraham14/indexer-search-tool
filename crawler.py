from bs4 import BeautifulSoup
import requests
import time

def fetch_quotes():
    quotes_list = []
    # 10 for 10 pages on site
    for i in range(10):
        page_num = i+1
        page = requests.get(f'https://quotes.toscrape.com/page/{page_num}/')

        soup = BeautifulSoup(page.content, "html.parser")
        quotes = soup.find_all('div', class_='quote')

        for quotes_div in quotes:
            quote_text = quotes_div.find('span', class_='text').get_text()
            quotes_list.append(quote_text)

        print(f"Fetched quotes from page {page_num}")
        print(f"Waiting 6 secs (politeness window)...")
        time.sleep(6) #6 seconds politness window.

    return quotes_list
