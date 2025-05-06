from bs4 import BeautifulSoup
import requests
import time
from collections import defaultdict
import spacy
import json

nlp = spacy.load("en_core_web_sm")

def fetch_quotes():
    quotes_by_page = {}
    # 10 for 10 pages on site
    for i in range(10):
        page_num = i+1
        page = requests.get(f'https://quotes.toscrape.com/page/{page_num}/')
        if page.status_code == 200:
            print(f"Fetching quotes from https://quotes.toscrape.com page {page_num}")

        soup = BeautifulSoup(page.content, "html.parser")
        quotes = soup.find_all('div', class_='quote')
        
        quotes_list = []
        for quotes_div in quotes:
            quote_text = quotes_div.find('span', class_='text').get_text()
            quotes_list.append(quote_text)

        quotes_by_page[page_num] = quotes_list

        print(f"Waiting 6 secs (politeness window)...")
        # time.sleep(6) #6 seconds politness window.

    return quotes_by_page

def build_inverted_index(quotes_hashmap):
    inverted_index = defaultdict(lambda: defaultdict(int))

    for page_num, quotes in quotes_hashmap.items():
        for quote in quotes:
            doc = nlp(quote.lower())  # tokenise and lowercase words
            words = [token.text for token in doc if token.is_alpha]
            for word in words:
                inverted_index[word][page_num] +=1

    #Print inverted_index:
    # for word in list(inverted_index.keys()):
    #     print(f"{word}: {dict(inverted_index[word])}")

    #Save inverted_index to json file
    with open("inverted_index.json", "w") as f:
        json.dump(inverted_index, f)

    print("Saved inverted index to 'inverted_index.json'")
    