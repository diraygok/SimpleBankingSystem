import sqlite3
from random import randint
from luhn import verify as ln

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute(
    "CREATE TABLE IF NOT EXISTS card(id INTEGER PRIMARY KEY, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);")
conn.commit()


class Banking:

    def __init__(self):
        self.accounts = {}

    def num_generator(self, number):
        num = []

        for i in range(0, number):
            num.append(str(randint(0, 9)))

        return "".join(num)

    def card_generator(self):

        IIN = 400000
        ACCOUNT_NUMBER = self.num_generator(9)
        CHECKSUM = self.num_generator(1)

        return str(IIN) + str(ACCOUNT_NUMBER) + str(CHECKSUM)

    def pin_generator(self):

        PIN = self.num_generator(4)

        return PIN

    def account_creator(self):

        card_number = self.card_generator()
        while ln(card_number) is False:
            card_number = self.card_generator()

        pin_number = self.pin_generator()

        self.accounts[card_number] = (pin_number, 0)

        cur.execute(f"INSERT INTO card(number, pin) VALUES ({card_number}, {pin_number})")
        conn.commit()

        print("Your card has been created")
        print("Your card number:")
        print(card_number)
        print("Your card PIN:")
        print(pin_number)

    # user operations

    def card_check(self, card):
        # 2: correct, not db
        # pin: correct, db
        # 0: luhn error
        if ln(card):
            for row in cur.execute(f'SELECT pin FROM card WHERE number = {card};'):
                pin = row[0]
                break
            else:
                return 2
            return pin
        else:
            return 0

    def login(self, card, pin):

        state = self.card_check(card)

        if state == 0 or state == 2:
            return False
        else:
            if state == pin:
                return True
            else:
                return False

    def balance(self, card):
        for row in cur.execute(f'SELECT balance FROM card WHERE number = {card};'):
            balance = row
            break
        else:
            return "An error occurred!"

        return balance[0]

    def update_balance(self, card, balance):
        cur.execute(f'UPDATE card SET balance = {balance} WHERE number = {card}')
        conn.commit()

    def add_income(self, card, amount):
        current = self.balance(card)
        new = current + int(amount)
        self.update_balance(card, new)
        return True

    def do_transfer(self, card_from, card_to, amount):
        balance_from = self.balance(card_from)
        amount = int(amount)

        if balance_from < amount:
            return False
        else:
            balance_to = self.balance(card_to)
            balance_from -= amount
            balance_to += amount

            self.update_balance(card_from, balance_from)
            self.update_balance(card_to, balance_to)

            return True

    def close_account(self, card):
        cur.execute(f'DELETE FROM card WHERE number = {card}')
        conn.commit()
        return True


menu_main = """\n1. Create an account
2. Log into account
0. Exit"""

menu_account = """\n1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit"""

banking = Banking()

while True:
    print(menu_main)
    selection = int(input())

    if selection == 1:
        banking.account_creator()
    elif selection == 2:
        print("Enter your card number:")
        login_card = input()
        print("Enter your PIN:")
        login_pin = input()

        succession = banking.login(login_card, login_pin)

        if succession:
            print("You have successfully logged in!")

            while True:
                print(menu_account)
                option = int(input())

                if option == 1:
                    print(f"Balance: {banking.balance(login_card)}")
                elif option == 2:
                    print("Enter income:")
                    income = input()
                    banking.add_income(login_card, income)
                    print("Income was added!")
                elif option == 3:
                    print("Transfer")
                    print("Enter card number:")
                    number = input()

                    card_check = banking.card_check(number)
                    if card_check == 0:
                        print("Probably you made a mistake in the card number. Please try again!")
                    elif card_check == 2:
                        print("Such a card does not exist.")
                    else:
                        if number == login_card:
                            print("You can't transfer money to the same account!")
                        else:
                            print("Enter how much money you want to transfer:")
                            amount = input()
                            transfer_check = banking.do_transfer(login_card, number, amount)
                            if transfer_check:
                                print("Success!")
                            else:
                                print("Not enough money!")
                elif option == 4:
                    banking.close_account(login_card)
                    print("The account has been closed!")
                    break
                elif option == 5:
                    print("You have successfully logged out!")
                    break
                elif option == 0:
                    selection = 0
                    break
                else:
                    continue
        else:
            print("Wrong card number or PIN!")
    else:
        pass

    if selection == 0:
        print("Bye!")
        break
