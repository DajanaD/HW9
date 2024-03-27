import json
from models import Author, Quote
import connect


# Функція для завантаження авторів з JSON-файлу
def load_authors_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        authors_data = json.load(file)
    for author_data in authors_data:
        fullname = author_data['fullname']
        author = Author.objects(fullname=fullname).first()  # Перевіряємо, чи існує вже автор з таким ім'ям
        if author:
            # Оновлюємо існуючого автора
            author.update(**author_data)
        else:
            # Створюємо нового автора
            author = Author(**author_data)
            author.save()

# Функція для завантаження цитат з JSON-файлу
def load_quotes_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        quotes_data = json.load(file)
    for quote_data in quotes_data:
        author_fullname = quote_data.pop('author')
        author = Author.objects(fullname=author_fullname).first()
        if author:
            quote = Quote(**quote_data, author=author)
            quote.save()

if __name__ == "__main__":
    # Шлях до JSON-файлів
    authors_file_path = 'authors.json'
    quotes_file_path = 'quotes.json'

    # Завантаження даних з JSON-файлів
    load_authors_from_json(authors_file_path)
    load_quotes_from_json(quotes_file_path)