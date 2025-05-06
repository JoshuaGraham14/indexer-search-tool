from bs4 import BeautifulSoup
import requests
import time
from collections import defaultdict
import spacy
import json
from urllib.parse import urljoin, urlparse
from collections import deque

nlp = spacy.load("en_core_web_sm")

BASE_URL = "https://quotes.toscrape.com/"

def crawl_pages():
    visited_urls = set()
    queue = deque([BASE_URL])

    #Follows format: {url: text}
    pages_content_dict = {}  

    #Uses BFS to crawl...
    #Reference: https://www.geeksforgeeks.org/breadth-first-search-or-bfs-for-a-graph/
    while queue:
        current_url = queue.popleft()

        if current_url in visited_urls:
            continue
        visited_urls.add(current_url)

        try:
            response = requests.get(current_url)
            if response.status_code!=200:
                print(f"Failed to fetch {current_url}")
                continue

            print(f"Fetching content from page: {current_url}") 
            soup = BeautifulSoup(response.text, "html.parser") 

            #retrieve all visible text from the site.
            #Reference: https://www.educative.io/answers/how-to-use-gettext-in-beautiful-soup
            body_text = soup.get_text(separator=' ', strip=True)
            pages_content_dict[current_url] =body_text

            # Find any internal links (same domain)
            for link_tag in soup.find_all('a', href=True):
                href = link_tag['href']
                #Reference: https://docs.python.org/3/library/urllib.parse.html
                full_url =urljoin(BASE_URL, href)
                parsed =urlparse(full_url)

                # Ensure we're staying on the same site
                if parsed.netloc==urlparse(BASE_URL).netloc and full_url not in visited_urls:
                    queue.append(full_url) 
            
            print(f"Waiting 6 secs (politeness window)...")
            time.sleep(6) #6 seconds politness window.

        except requests.RequestException as e: 
            print(f"Error fetching page: {current_url} . Error: {e}")
            continue  

    print(f"Finished crawling. Total pages={len(pages_content_dict)}")

    return pages_content_dict


def build_inverted_index(pages_content_dict):
    inverted_index = defaultdict(lambda: defaultdict(list))

    for url, text in pages_content_dict.items():
        doc = nlp(text.lower())  # tokenise and lowercase words
        pos = 0  # absolute position per page (DOESN'T INCLUDE STOP TOKENS)
        #note: 0 indexing is used.

        for token in doc:
            #check token is a word AND is not a stop word.
            #Reference: https://stackoverflow.com/questions/73078231/how-to-get-all-stop-words-from-spacy-and-dont-get-any-errors-typeerror-argume
            if token.is_alpha and not token.is_stop:
                word = token.text
                inverted_index[word][url].append(pos)
                pos += 1

        #sort words for better presentation...
        for word_pages in inverted_index.values():
            for positions in word_pages.values():
                positions.sort() 
 
    #Save inverted_index to json file
    with open("inverted_index.json", "w") as f:
        json.dump(inverted_index, f)

    print("Saved inverted index to 'inverted_index.json'")
    