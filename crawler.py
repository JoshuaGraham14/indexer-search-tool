from bs4 import BeautifulSoup

soup = BeautifulSoup('''<h1>Geeks for Geeks</h1>''',
                     "html.parser")

print(type(soup))