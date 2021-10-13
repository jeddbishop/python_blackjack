# Jedd's Python Blackjack - Final Version 2021-10-13

import random

import os
def cls():
  os.system('cls' if os.name=='nt' else 'clear')

class Card():
    def __init__(self, number, letter, suit):
        self.number = number
        self.letter = letter
        self.suit = suit

    def __str__(self):
        return str(f'{self.letter} {self.suit}')

    def show_card(self):
        print(f'{self.letter} {self.suit}')

class Deck():
    def __init__(self):
        self.box = []
        self.build_deck()

    def build_deck(self):
        for number, letter in enumerate(range(1,14), 1):
            if number == 1:
                letter = 'A'
            elif number == 11:
                number = 10
                letter = 'J'
            elif number == 12:
                number = 10
                letter = 'Q'
            elif number == 13:
                number = 10
                letter = 'K'
                        # spades  hearts  diamonds  clubs
            for suit in ['\u2660','\u2661','\u2662','\u2663']:
                self.box.append(Card(number, letter, suit))

    def show_deck(self):
        for card in self.box:
            card.show_card()

    def shuffle_deck(self):
        random.shuffle(self.box)

    def give_card(self):
        return self.box.pop()

class Player():
    def __init__(self):
        self.hand = []
        self.total = 0
        self.holding = False

        # used for dealer only
        self.reveal = False

    def __str__(self):
        return [i for i in self.hand]

    def draw_card(self, amount, deck):
        for i in range(amount):
            self.hand.append(deck.give_card())

    def show_hand(self):
        card_count = len(self.hand)

        card_edg = '\u2022-----\u2022 '
        card_spc = '|     | '
        card_mid = []

        print(f"\t\t    Player: {self.sum_hand()}")
        print('\t\t' + card_edg * card_count)
        print('\t\t' + card_spc * card_count)
        for card in self.hand:
            # len(str(card))) is 3 for normal cards, 4 for tens
            if len(str(card)) == 3:
                middles = f'| {str(card)} | '
                card_mid.append(middles)
            if len(str(card)) == 4:
                middles = f'| {str(card)}| '
                card_mid.append(middles)
        print('\t\t' + ''.join(card_mid))
        print('\t\t' + card_spc * card_count)
        print('\t\t' + card_edg * card_count)

    def dealer_hidden(self):
        card_edg = '\u2022-----\u2022 '
        card_spc = '|     | '
        card_up = f'| {str(self.hand[0])} | '
        card_up_ten = f'| {str(self.hand[0])}| '
        card_dwn = '|:::::| '

        print('\t\t' + "    Dealer:")
        print('\t\t' + card_edg + card_edg)
        print('\t\t' + card_spc + card_dwn)
        if len(str(self.hand[0])) == 3:
            print('\t\t' + card_up  + card_dwn)
        if len(str(self.hand[0])) == 4:
            print('\t\t' + card_up_ten  + card_dwn)
        print('\t\t' + card_spc + card_dwn)
        print('\t\t' + card_edg + card_edg + '\n')

    def dealer_reveal(self):
        card_count = len(self.hand)

        card_edg = '\u2022-----\u2022 '
        card_spc = '|     | '
        card_mid = []

        print('\t\t' + f"    Dealer: {self.total}")
        print('\t\t' + card_edg * card_count)
        print('\t\t' + card_spc * card_count)
        for card in self.hand:
            # len(str(card))) is 3 for normal cards, 4 for tens
            if len(str(card)) == 3:
                middles = f'| {str(card)} | '
                card_mid.append(middles)
            if len(str(card)) == 4:
                middles = f'| {str(card)}| '
                card_mid.append(middles)
        print('\t\t' + ''.join(card_mid))
        print('\t\t' + card_spc * card_count)
        print('\t\t' + card_edg * card_count + '\n')

    def sum_hand(self):
        self.total = 0

        # sort cards low to high
        sorted_hand = sorted([card.number for card in self.hand])
        # if sorted cards contain an ace
        if 1 in sorted_hand:
            # count how many aces
            ace_count = sorted_hand.count(1)
            # as many times as we have aces...
            for ace in range(ace_count):
                # ...put the ace at the end of the list
                sorted_hand.append(sorted_hand.pop(0))
            # count the sum of the sorted cards
            for card in sorted_hand:
                if card == 1:
                    # aces are 1 if they would bust us (or if we have more than one ace)
                    if self.total + 11 > 21 and ace_count >= 1:
                        self.total += 1
                        ace_count -= 1
                    # otherwise they are 11
                    else:
                        self.total += 11
                # add non-aces
                else:
                    self.total += card

        # if hand does not contain aces
        else:
            # just add em up
            for card in self.hand:
                self.total += card.number

        return self.total

def main():
    player = Player()
    dealer = Player()
    player.hand = []
    dealer.hand = []
    deck = Deck()
    deck.shuffle_deck()
    player.draw_card(2, deck)
    dealer.draw_card(2, deck)

    # use to start the player with a specific hand
    # a1 = Card(1, 'A', '\u2660')
    # a2 = Card(1, 'A', '\u2661')
    # player.hand.append(a1)
    # player.hand.append(a2)

    def blit_game():
        cls()
        print('''
        \u2022-----------------------------\u2022
        | * Jedd's Python Blackjack * |
        \u2022-----------------------------\u2022
        ''')
        if dealer.reveal:
            dealer.dealer_reveal()
        else:
            dealer.dealer_hidden()
        player.show_hand()

    def proceed():

        if player.total < 22 and not player.holding:
            choice = input('|----------|\n| HIT  - H |\n| STAY - S |\n|          |\n| DEAL - D |\n| QUIT - Q |\n|----------|\n\n\t')
            if choice.upper() == 'H':
                player.draw_card(1, deck)
                blit_game()
                proceed()
            if choice.upper() == 'S':
                dealer.reveal = True
                player.holding = True
                dealer.total = dealer.sum_hand()
                while dealer.total < 17:
                    dealer.draw_card(1, deck)
                    dealer.total = dealer.sum_hand()
            if choice.upper() == 'D':
                main()
            if choice.upper() == 'Q':
                global run_game
                run_game = False

    def result():
        # player bust
        if player.total > 21:
            player.total = 0
            choice = input('|----------|\n|          |\n| DEAL - D |\n|          |    Player busted!\n| QUIT - Q |\n|          |\n|----------|\n\n\t')
            if choice.upper() == 'D':
                pass
            if choice.upper() == 'Q':
                run_game = False

        # compare player/dealer
        if player.holding:
            blit_game()
            player.holding = False
            if player.total == dealer.total:
                choice = input('|----------|\n|          |\n| DEAL - D |\n|          |    Its a push!\n| QUIT - Q |\n|          |\n|----------|\n\n\t')
                if choice.upper() == 'D':
                    pass
                if choice.upper() == 'Q':
                    run_game = False
            if player.total < dealer.total and dealer.total < 22:
                choice = input('|----------|\n|          |\n| DEAL - D |\n|          |    Dealer wins!\n| QUIT - Q |\n|          |\n|----------|\n\n\t')
                if choice.upper() == 'D':
                    pass
                if choice.upper() == 'Q':
                    run_game = False
            if player.total < dealer.total and dealer.total > 21:
                choice = input('|----------|\n|          |\n| DEAL - D |\n|          |    Dealer busted!\n| QUIT - Q |\n|          |\n|----------|\n\n\t')
                if choice.upper() == 'D':
                    pass
                if choice.upper() == 'Q':
                    run_game = False
            if player.total > dealer.total:
                choice = input('|----------|\n|          |\n| DEAL - D |\n|          |    Player wins!\n| QUIT - Q |\n|          |\n|----------|\n\n\t')
                if choice.upper() == 'D':
                    pass
                if choice.upper() == 'Q':
                    run_game = False

    blit_game()
    proceed()
    result()

run_game = True
while run_game:
    main()
