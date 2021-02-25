import os
import string

import requests
from bs4 import BeautifulSoup


def main():
    num_pages = int(input('Enter a number of pages:\n> '))
    article_type = input('Enter an article type:\n> ')
    url = 'https://www.nature.com/nature/articles?page={num_page}'
    pages = get_articles_from_url(url, num_pages, article_type)
    save_articles(pages)
    print('Saved all articles.')


def get_articles_from_url(url, num_pages, article_type):
    articles = {}
    for num_page in range(1, num_pages + 1):
        response = requests.get(url.format(num_page=num_page))
        if response.status_code != 200:
            print(f'The URL returned {response.status_code}!')
            break
        if num_page not in articles:
            articles[num_page] = []
        articles[num_page].extend(parse_articles_from_source(
            response.content, article_type
        ))
    return articles


def parse_articles_from_source(source, type_name):
    main_soup = BeautifulSoup(source, 'html.parser')
    articles = []
    for article in main_soup.find_all('article'):
        article_type = article.find(
            'span', {'data-test': 'article.type'}
        ).text
        if article_type.lower() != type_name.lower():
            continue

        link_element = article.find('a', {'data-track-action': 'view article'})
        response = requests.get(
            f"https://www.nature.com{link_element.get('href')}"
        )
        if response.status_code != 200:
            continue

        article_soup = BeautifulSoup(response.content, 'html.parser')
        article_description = article_soup.find(
            'div', {'class', 'article__body'}
        )
        if article_description is None:
            article_description = article_soup.find(
                'div', {'class': 'article-item__body'}
            )

        articles.append({
            'title': clean_title(link_element.text),
            'description': article_description.text.strip()
        })
    return articles


def clean_title(title):
    trans = str.maketrans(' ', '_', string.punctuation)
    return title.strip().translate(trans)


def save_articles(pages):
    for page in pages:
        os.makedirs(f'Page_{page}', exist_ok=True)
        for article in pages[page]:
            output_path = f"Page_{page}/{article['title']}.txt"
            with open(output_path, 'wb') as file:
                file.write(article['description'].encode('UTF-8'))


if __name__ == '__main__':
    main()
