import os
import sys
from collections import deque

import colorama
import requests
from bs4 import BeautifulSoup


def main(output_dir):
    history = deque()
    current_page = None
    while True:
        user_input = input('> ').strip().lower()

        if user_input == 'exit':
            break

        if user_input == 'back':
            if current_page is None:
                continue
            current_page = history.pop()
            user_input = current_page

        if not is_valid_url(user_input):
            if not is_valid_filename(output_dir, f'{user_input}.txt'):
                print('Error: Incorrect URL')
                continue

            print(get_saved_page(output_dir, f'{user_input}.txt'))
        else:
            if not user_input.startswith('http'):
                user_input = f'https://{user_input}'
            content = make_request(user_input)
            parsed_content = parse_content(content)
            save_page(output_dir, f'{user_input[8:user_input.rfind(".")]}.txt', parsed_content)
            print(parsed_content)

        if current_page is not None:
            history.append(current_page)
        current_page = user_input


def parse_content(content):
    valid_tags = ('p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'ul', 'ol', 'li')
    soup = BeautifulSoup(content, 'html.parser')
    return ''.join(tag.text.strip() if tag.name != 'a' else colorama.Fore.BLUE + tag.text.strip()
                   for tag in soup.find_all(valid_tags))


def validate_cmd_args():
    output_dir = None
    if len(sys.argv) > 1:
        output_dir = sys.argv[1]
        if not os.path.isdir(output_dir):
            os.mkdir(output_dir)
    return output_dir


def is_valid_url(url):
    return url.find('.') != -1


def is_valid_filename(output_dir, filename):
    return os.path.isfile(get_output_path(output_dir, filename))


def get_output_path(output_dir, filename):
    return os.path.join(output_dir, filename)


def get_saved_page(output_dir, filename):
    content = None
    with open(get_output_path(output_dir, filename), 'r') as webpage:
        content = webpage.read()
    return content


def make_request(url):
    response = requests.get(url)
    return response.content if response else None


def save_page(output_dir, filename, content):
    print(get_output_path(output_dir, filename))
    with open(get_output_path(output_dir, filename), 'w') as webpage:
        webpage.write(content)


if __name__ == '__main__':
    colorama.init(autoreset=True)
    output_dir = validate_cmd_args()
    main(output_dir)

