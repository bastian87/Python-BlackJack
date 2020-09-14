import random

suits = ('Hearts','Diamonds','Spades','Clubs')
ranks = ('Two','Three', 'Four','Five','Six','Seven','Eight','Nine',
'Ten','Jack','Queen','King','Ace')
values ={'Two':2,'Three':3, 'Four':4,'Five':5,'Six':6,'Seven':7,'Eight':8,'Nine':9,
'Ten':10,'Jack':10,'Queen':10,'King':10,'Ace':11}

playing = True

class Card():
    
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        

    def __str__(self):
        return self.rank+" of "+self.suit

class Deck():

    def __init__(self):
        self.deck = [] #start with an empty List
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))
    
    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n'+ card.__str__()
        return "The deck has: " + deck_comp
    
    def shuffle(self):
        random.shuffle(self.deck)
    
    def deal(self):
        single_card = self.deck.pop()
        return single_card

# Hand() It's the representation of the player or the NPC
class Hand():
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]

        # track aces
        if card.rank == "Ace":
            self.aces += 1


    def adjust_for_ace(self):

        # if total value is 21 and i have an ace, then mi Ace is value 1 
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Chips():

    def __init__(self, total=100):
        self.total = total
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet

#FUNCTIONS DEFINITIONS
def take_bet(chips):

        while True:
            try:
                chips.bet = int(input("How many chips would you like to bet?"))

            except:
                print("You need to provide a number")            
            else:
                if chips.bet > chips.total:
                    print(f"You don't have enough chips. You have: {chips.total}")
                else:
                    break
    
def hit(deck, hand):
        
    single_card = deck.deal()
    hand.add_card(single_card)
    hand.adjust_for_ace()

def hit_or_stand(deck,hand):
    global playing

    while True:
        print("\n")
        x = input("Hit or Stand? Enter h or s: ")

        if x[0].lower() == 'h':
            hit(deck,hand)
        elif x[0].lower() == 's':
            print("Then it's dealer's turn")
            playing = False
        else:
            print("You must enter 'h' or 's' only")
            continue

        break       
    

def show_some(player,dealer):
    print("DEALERS HAND:\nOne card hidden")
    print("\n")
    print(dealer.cards[1])
    print("\nPLAYER HAND:")    
    for card in player.cards:
        print(card)

def show_all(player,dealer):
    print("DEALER HAND:")
    for card in dealer.cards:
        print(card)
    print("\n")
    print("PLAYER HAND:")
    for card in player.cards:
        print(card)

def player_busts(player,dealer,chips):
    print("YOU BUSTED!")
    chips.lose_bet()

def player_wins(player,dealer,chips):
    print("YOU WIN!")
    chips.win_bet()

def dealer_busts(player,dealer,chips):
    print("YOU WIN, DEALER BUSTED!")
    chips.lose_bet()

def dealer_wins(player,dealer,chips):
    print("YOU LOSE! DEALER WIN!")
    chips.win_bet()

def push(player,dealer):
    print("Both get a Tie!")

while True:

    print("WELCOME TO BLACKJACK 2020")

    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    player_chips = Chips()

    take_bet(player_chips)

    show_some(player_hand,dealer_hand)

    while playing:

        hit_or_stand(deck,player_hand)

        show_some(player_hand,dealer_hand)

        if player_hand.value > 21:
            player_busts(player_hand,dealer_hand,player_chips)
            break

    if player_hand.value <= 21:

        while dealer_hand.value < 17:
            hit(deck,dealer_hand)

        show_all(player_hand,dealer_hand)

        if dealer_hand.value > 21:
            dealer_busts(player_hand,dealer_hand,player_chips)

        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)

        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand,dealer_hand,player_chips)
        
        else:
            push(player_hand,dealer_hand)
    
    print(f'\n Player total chips are: {player_chips.total}')

    new_game = input("Would you want to play again? y/n")

    if new_game[0].lower() == "y":
        playing = True
        continue
    else:
        print("Thanks for Playing!")
        break