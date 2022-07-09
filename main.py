from typing import Callable, List

import requests
import sys
import getopt
from bs4 import BeautifulSoup
import os

BASE_URL = "http://www.gutenberg.org/robot/"
#BASE_QUERY = "harvest?filetypes[]=txt&langs[]=de"
#FIRST_QUERY = BASE_URL + BASE_QUERY
#MAX = 1

def make_query(filetype, language):
    return f"harvest?filetypes[]={filetype}&langs[]={language}"

def make_url(base: str, query: str) -> str:
    return base + query

def is_http(object: str) -> bool:
    return object.startswith("http")

def get(url: str) -> Callable:
    return requests.get(url, timeout=5.0)

def get_stream(url: str) -> Callable:
    return requests.get(url, stream=True)

def parse(response: Callable) -> Callable:
    html = response.text
    return BeautifulSoup(html, 'html.parser')

def list_links(object: Callable) -> List:
    for link in object.body.find_all('a'):
        yield link.get("href")

def make_directories(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def save(stream: Callable, path: str) -> None:
    with open(path, 'wb') as f:
        for chunk in stream.iter_content(chunk_size=128):
            f.write(chunk)

def main(argv):
    filetype = None
    language = None
    max = None

    try:
        opts, args = getopt.getopt(
            argv, "ht:l:m:", ["filetype=", "language=", "max="]
        )
    except getopt.GetoptError:
        print('main.py -t <filetype> -l <language> -m <max>')
        sys.exit()
    
    for opt, arg in opts:
        if opt == '-h':
            print('main.py -t <filetype> -l <language> -m <max>')
            sys.exit()
        elif opt in ('-t', '--filetype'):
            filetype = arg
        elif opt in ('-l', '--language'):
            language = arg
        elif opt in ('-m', '--max'):
            max = int(arg)

    print(f"Downloading '{filetype}' in '{language}' with '{max}' threshold...")

    first_query = make_query(filetype=filetype, language=language)
    first_url = make_url(BASE_URL, first_query)

    response = get(first_url)
    parsed_html = parse(response)
    links = list_links(parsed_html)

    for i in range(0, max):
        link = next(links)
        if is_http(link):
            stream = get_stream(link)
            make_directories(f"./data/{language}/")
            save(stream, f"./data/{language}/{i}.zip")
        else:
            url = make_url(BASE_URL, link)
            response = get(url)
            parsed_html = parse(response)
            links = list_links(parsed_html)

    print(f"Saved in './data/{language}/'.")

if __name__ == "__main__":
    main(sys.argv[1:])