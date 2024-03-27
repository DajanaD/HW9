import requests
from bs4 import BeautifulSoup
import json
import re

def get_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

def parse_quotes(page):
    soup = BeautifulSoup(page, 'html.parser')
    quotes = []
    authors = set()
    
    for quote in soup.find_all('div', class_='quote'):
        text = quote.find('span', class_='text').text
        author = quote.find('small', class_='author').text
        tags = [tag.text for tag in quote.find_all('a', class_='tag')]
        
        quotes.append({'quote': text, 'author': author, 'tags': tags})
        authors.add(author)
    
    return quotes, list(authors)

def parse_author_page(author_url):
    response = get_page(author_url)
    if response:
        soup = BeautifulSoup(response, 'html.parser')
        fullname = soup.find('h3', class_='author-title').text
        born_date = soup.find('span', class_='author-born-date').text
        born_location = soup.find('span', class_='author-born-location').text
        description = soup.find('div', class_='author-description').text.strip()
        return {'fullname': fullname, 'born_date': born_date, 'born_location': born_location, 'description': description}
    else:
        return None

def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def main():
    base_url = 'http://quotes.toscrape.com'
    quotes_all = []
    authors_all = set()
    authors_info = []
    
    page = get_page(base_url)
    soup = BeautifulSoup(page, 'html.parser')
    if page:
        quotes, authors = parse_quotes(page)
        quotes_all.extend(quotes)
        authors_all.update(authors)
        
        
        next_page = soup.find('li', class_='next')
        while next_page:
            next_page_url = base_url + next_page.a['href']
            page = get_page(next_page_url)
            if page:
                quotes, authors = parse_quotes(page)
                quotes_all.extend(quotes)
                authors_all.update(authors)
                soup = BeautifulSoup(page, 'html.parser')
                next_page = soup.find('li', class_='next')
            else:
                break
    
    save_to_json(quotes_all, 'quotes.json')
    
    for author in authors_all:
        author = author.replace(".", " ")
        author_url = base_url + '/author/' + '-'.join(author.title().split())
        author_info = parse_author_page(author_url)
        if author_info:
            authors_info.append(author_info)
    
    save_to_json(authors_info, 'authors.json')

if __name__ == '__main__':
    main()
