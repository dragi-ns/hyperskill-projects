import random
from string import ascii_lowercase

WORDS = ('python', 'java', 'kotlin', 'javascript')
HEADER = 'H A N G M A N'
FOOTER = 'Thanks for playing!'


def get_random_word(words):
    return random.choice(words)


def mask_word(word):
    return ['-'] * len(word)


def get_masked_word_as_string(masked_word):
    return ''.join(masked_word)


def replace_masked_letter_in_word(word, masked_word, letter):
    start_index = 0
    while True:
        letter_index = word.find(letter, start_index)
        if letter_index == -1:
            if start_index == 0:
                print('No such letter in the word')
                return False
            break

        if masked_word[letter_index] != '-':
            print('No improvements')
            return False

        masked_word[letter_index] = letter
        start_index = letter_index + 1
    return True


def is_solved(masked_word):
    return '-' not in masked_word


def print_success_message():
    print('You guessed the word!')
    print('You survived!')


def print_failure_message():
    print('You are hanged!')


def validate_user_input(user_input, seen_letters):
    if len(user_input) != 1:
        print('You should input a single letter')
        return False

    if user_input not in ascii_lowercase:
        print('It is not an ASCII lowercase letter')
        return False

    if user_input in seen_letters:
        print('You already typed this letter')
        return False

    seen_letters.add(user_input)
    return True


def start_game():
    random_word = get_random_word(WORDS)
    masked_word = mask_word(random_word)

    user_tries = 8
    seen_letters = set()
    while user_tries > 0:
        print('\n' + get_masked_word_as_string(masked_word))

        if is_solved(masked_word):
            print_success_message()
            return True

        print('Input a letter: > ')
        user_input = input()

        if not validate_user_input(user_input, seen_letters):
            continue

        if not replace_masked_letter_in_word(random_word, masked_word, user_input):
            user_tries -= 1
    else:
        print_failure_message()
        return False


def main():
    print(HEADER)

    while True:
        print('Type "play" to play the game, "exit" to quit: > ')
        user_input = input().strip().lower()

        if user_input == 'play':
            start_game()

        if user_input == 'exit':
            break

    print(FOOTER)


if __name__ == '__main__':
    main()
