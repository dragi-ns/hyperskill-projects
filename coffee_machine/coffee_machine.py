import sys


class CoffeeMachine:
    def __init__(self):
        self.water = 400
        self.milk = 540
        self.coffee_beans = 120
        self.disposable_cups = 9
        self.money = 550
        self.state = 'main_menu'

    def prompt_message(self):
        if self.state == 'main_menu':
            return 'Write action (buy, fill, take, remaining, exit):'
        elif self.state == 'buy_menu':
            return 'What do you want to buy? 1 - espresso, 2 - late, ' \
                   '3 - cappuccino, back - to main menu:'
        elif self.state == 'fill_menu':
            return 'Write how many ml of water do you want to add:'
        elif self.state == 'fill_menu_2':
            return 'Write how many ml of milk do you want to add:'
        elif self.state == 'fill_menu_3':
            return 'Write how many grams of coffee beans do you want to add:'
        elif self.state == 'fill_menu_4':
            return 'Write how many disposable cups of coffee do you want to add:'

    def user_action(self, action):
        if self.state == 'main_menu':
            self.main_menu(action)
        elif self.state == 'buy_menu':
            self.buy_menu(action)
        elif self.state in ('fill_menu', 'fill_menu_2', 'fill_menu_3', 'fill_menu_4'):
            self.fill_menu(action)

    def main_menu(self, action):
        if action == 'buy':
            self.state = 'buy_menu'
        elif action == 'fill':
            self.state = 'fill_menu'
        elif action == 'take':
            self.take()
        elif action == 'remaining':
            self.remaining()
        elif action == 'exit':
            sys.exit(0)
        else:
            print('Invalid action! Try again!')

    def buy_menu(self, action):
        if action == 'back':
            self.state = 'main_menu'
            return

        action_int = int(action)

        if action_int == 1:
            self.prepare_espresso()
        elif action_int == 2:
            self.prepare_latte()
        elif action_int == 3:
            self.prepare_cappuccino()
        else:
            print('Invalid coffee type! Try again!')
            return

        self.state = 'main_menu'

    def fill_menu(self, action):
        amount = int(action)

        if self.state == 'fill_menu':
            self.water += amount
            self.state = 'fill_menu_2'
        elif self.state == 'fill_menu_2':
            self.milk += amount
            self.state = 'fill_menu_3'
        elif self.state == 'fill_menu_3':
            self.coffee_beans += amount
            self.state = 'fill_menu_4'
        elif self.state == 'fill_menu_4':
            self.disposable_cups += amount
            self.state = 'main_menu'

    def take(self):
        print(f'I gave you ${self.money}')
        self.money = 0

    def remaining(self):
        print('The coffee machine has:')
        print(f'{self.water} of water')
        print(f'{self.milk} of milk')
        print(f'{self.coffee_beans} of coffee beans')
        print(f'{self.disposable_cups} of disposable cups')
        print(f'${self.money} of money')

    def prepare_espresso(self):
        if self.is_available('water', 250) \
           and self.is_available('coffee_beans', 16) \
           and self.is_available('disposable_cups', 1):
            self.water -= 250
            self.coffee_beans -= 16
            self.disposable_cups -= 1
            self.money += 4
            print('I have enough resources, making you a coffee!')

    def prepare_latte(self):
        if self.is_available('water', 350) \
           and self.is_available('milk', 75) \
           and self.is_available('coffee_beans', 20) \
           and self.is_available('disposable_cups', 1):
            self.water -= 350
            self.milk -= 75
            self.coffee_beans -= 20
            self.disposable_cups -= 1
            self.money += 7
            print('I have enough resources, making you a coffee!')

    def prepare_cappuccino(self):
        if self.is_available('water', 200) \
           and self.is_available('milk', 100) \
           and self.is_available('coffee_beans', 12) \
           and self.is_available('disposable_cups', 1):
            self.water -= 200
            self.milk -= 100
            self.coffee_beans -= 12
            self.disposable_cups -= 1
            self.money += 6
            print('I have enough resources, making you a coffee!')

    def is_available(self, resource, amount):
        available_amount = getattr(self, resource, 0)
        if available_amount >= amount:
            return True
        print(f'Sorry, not enough {resource}!')
        return False


coffee_machine = CoffeeMachine()

while True:
    print(coffee_machine.prompt_message())
    print('> ')
    coffee_machine.user_action(input().strip())
