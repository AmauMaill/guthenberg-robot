import requests
from bs4 import BeautifulSoup

BASE_URL = "http://www.gutenberg.org/robot/"
BASE_QUERY = "harvest?filetypes[]=txt&langs[]=de"
FIRST_QUERY = BASE_URL + BASE_QUERY

MAX = 5 

response = requests.get(FIRST_QUERY, timeout=5.0)

html = response.text
parsed_html = BeautifulSoup(html)

print(parsed_html.body.prettify())

for link in parsed_html.body.find_all('a'):
    print(link.get('href'))

URL = BASE_URL + "harvest?offset=112933&filetypes[]=txt&langs[]=de"

response = requests.get(URL, timeout=5.0)

html = response.text
parsed_html = BeautifulSoup(html)

print(parsed_html.body.prettify())

for link in parsed_html.body.find_all('a'):
    print(link.get('href'))

links = [link.get('href') for link in parsed_html.body.find_all('a')]
print([link for link in links if link.startswith("http")])
print([link for link in links if link.startswith("harvest")])