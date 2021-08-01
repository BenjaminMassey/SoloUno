import random

class Color:
    Red = 0
    Yellow = 1
    Blue = 2
    Green = 3
    Wild = 4
    Str = ["R", "Y", "B", "G", "W"]

class Card:

    def __init__(self, number, color):
        self.number = number
        self.color = color

    def matches(self, check):
        return self.number == check.number \
               or self.color == check.color \
               or self.color == Color.Wild \
               or check.color == Color.Wild
    
    def ToString(self):
        return str(self.number) + Color.Str[self.color]

    # Static method
    def ToCard(string):
        if string[0] == "+":
            return Card("+" + string[1], Color.Str.index(string[2]))
        else:
            return Card(int(string[0]), Color.Str.index(string[1]))

class Deck:

    def __init__(self):
        cards = []
        for col in [Color.Red, Color.Blue, Color.Green, Color.Red]:
            for i in range(10): # 0-9
                cards.append(Card(i, col))
            for i in range(2):
                cards.append(Card("+2", col))
        for i in range(4):
            cards.append(Card("0", Color.Wild))
        for i in range(4):
            cards.append(Card("+4", Color.Wild))
        self.cards = cards
        self.shuffle()
        self.active = self.draw()

    def shuffle(self):
        for i in range(2000):
            x = random.randint(0, len(self.cards) - 1)
            y = random.randint(0, len(self.cards) - 1)
            temp = self.cards[x]
            self.cards[x] = self.cards[y]
            self.cards[y] = temp

    def print_active(self):
        print(self.active.ToString())

    def draw(self):
        return self.cards.pop()

    # For debugging
    def print(self):
        for card in self.cards:
            print(card.number, card.color)


class Player:

    def __init__(self, deck):
        hand = []
        for i in range(7):
            hand.append(deck.draw())
        self.hand = hand

    def draw(self, deck):
        self.hand.append(deck.draw())

    def print_hand(self):
        statement = ""
        for card in self.hand:
            statement += card.ToString() + " "
        print(statement)

    # -1 = not has, otherwise returns index
    def has(self, check):
        i = 0
        #print("CHECK", check.number, check.color)
        for card in self.hand:
            #print("CARD", card.number, card.color)
            if str(card.number) == str(check.number) and str(card.color) == str(check.color):
                return i
            i += 1
        return -1

    # -1 = not has card, -2 = not match, 0 = played, 1 = won
    def play(self, card, deck):
        index = self.has(card)
        if index == -1:
            return -1
        if not card.matches(deck.active):
            return -2
        deck.active = card
        del self.hand[index]
        if self.check_win():
            return 1
        return 0

    def check_win(self):
        return len(self.hand) == 0


deck = Deck()
#deck.print()

player = Player(deck)

playing = True

while playing:
    print("Your hand:")
    player.print_hand()
    print("\nActive card:")
    deck.print_active()
    action = input("\nDraw or Play XX: ")
    pieces = action.split(" ")
    if pieces[0] == "Draw":
        player.draw(deck)
    elif pieces[0] == "Play":
        result = player.play(Card.ToCard(pieces[1]), deck)
        #print("Result", result)
        if result == 1:
            print("\n--- YOU WIN! ---")
            playing = False
        if result == -1:
            print("\n\n--- You don't have that card... ---")
        if result == -2:
            print("\n\n--- That card is not a match... ---")
    else:
        print("\n\n--- Unknown action :( ---")
    print()
