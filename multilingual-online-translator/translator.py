import sys

import requests
from requests.compat import urljoin
from bs4 import BeautifulSoup

LANGUAGES = (
    'All', 'Arabic', 'German', 'English', 'Spanish', 'French',
    'Hebrew', 'Japanese', 'Dutch', 'Polish', 'Portuguese',
    'Romanian', 'Russian', 'Turkish'
)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'
}

BASE_URL = 'https://context.reverso.net/translation/'

WORD_TRANS_HEADER_TEMPLATE = '{0} Translations:\n'
EXAMPLE_TRANS_HEADER_TEMPLATE = '{0} Examples:\n'
EXAMPLE_TRANS_CONTENT_TEMPLATE = '{0}:\n{1}\n\n'


def print_usage():
    print('Usage:')
    print('python translator.py <from_language> '
          '<to_language> <word_for_translation>')
    print('Example:')
    print('python translator.py english french hello')


def print_supported_langs():
    print('Supported languages are:')
    print(', '.join(LANGUAGES))


def get_lang_trans_pair():
    if len(sys.argv) < 4:
        print('Too few arguments!')
        print_usage()
        sys.exit(1)

    from_lang = sys.argv[1].title()
    to_lang = sys.argv[2].title()

    if from_lang not in LANGUAGES:
        print(f"Sorry, the program doesn't support {from_lang}")
        print_supported_langs()
        sys.exit(1)

    if to_lang not in LANGUAGES:
        print(f"Sorry, the program doesn't support {to_lang}")
        print_supported_langs()
        sys.exit(1)

    return from_lang, to_lang


def get_word_for_trans():
    return sys.argv[3]


def get_html_src(lang_pair, word):
    url = urljoin(BASE_URL, f'{lang_pair.lower()}/{word}')

    response = requests.get(url, headers=HEADERS)

    if not response:
        if response.status_code == 404:
            print(f'Sorry, unable to find {word}')
        else:
            print('Something wrong with your internet connection')

        sys.exit(1)

    return response.content


def parse_html_src(html_source):
    soup = BeautifulSoup(html_source, 'html.parser')

    translated_words = [word.text.strip() for word in soup.select('div#translations-content > a')]

    translated_examples = []
    for example in soup.select('section#examples-content > div[class="example"]'):
        translated_examples.append([sentence.text.strip() for sentence in example.select('span.text')])

    return translated_words, translated_examples


def get_trans(lang_pair, word):
    html_src = get_html_src(lang_pair, word)
    return parse_html_src(html_src)


def print_trans_to_user(lang, trans_words, trans_examples, file=None):
    formatted_words = '\n'.join(trans_words[:5]) + '\n\n'

    word_trans_header_formatted = WORD_TRANS_HEADER_TEMPLATE.format(lang)

    print(word_trans_header_formatted, end='')
    print(formatted_words, end='')
    if file:
        file.write(word_trans_header_formatted)
        file.write(formatted_words)

    example_trans_header_formatted = EXAMPLE_TRANS_HEADER_TEMPLATE.format(lang)
    print(example_trans_header_formatted, end='')
    if file:
        file.write(example_trans_header_formatted)
    for trans_example in trans_examples[:5]:
        formatted_example = EXAMPLE_TRANS_CONTENT_TEMPLATE.format(
            trans_example[0], trans_example[1]
        )
        print(formatted_example, end='')
        if file:
            file.write(formatted_example)


def main():
    from_lang, to_lang = get_lang_trans_pair()
    word = get_word_for_trans()

    if to_lang == LANGUAGES[0]:
        trans_file = open(f'{word}.txt', 'w+')

        for lang in LANGUAGES[1:]:
            if lang == from_lang:
                continue

            trans_words, trans_examples = get_trans(
                f'{from_lang}-{lang}',
                word
            )

            print_trans_to_user(
                lang, trans_words,
                trans_examples, trans_file
            )

        trans_file.close()
        return

    trans_words, trans_examples = get_trans(
        f'{from_lang}-{to_lang}',
        word
    )

    print_trans_to_user(
        to_lang, trans_words,
        trans_examples
    )


if __name__ == '__main__':
    main()
