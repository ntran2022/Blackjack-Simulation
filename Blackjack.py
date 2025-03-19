import random           #Used to randomly create the hand and draw a random card
import time             #Used to make the game flow naturally

#_________________________________________________________________________________
#Creates a hand for the player with 2 cards to begin.
def make_hand(hand):
    for i in range (2):
        hand.append(random.choice(cards))
    return hand

#Adds up the total amount of money won and lost.
def add_earnings(bet):
    global earnings
    earnings += int(bet)

#Gives the player a random card to their hand.
def hit(hand):
    hand.append(random.choice(cards))
    return hand

def return_hand(hand):
    return hand

#Doubles the player's bet and gives another random card to their hand.
def double_down(bet, hand):
    bet = int(bet)*2
    print("Your bet has been doubled to", "$"+str(bet))
    hit(hand)
    return bet

#Adds the money to the player's balance upon winning a game.
def bet_won(bet, balance):
    return balance + int(bet)

#Subtracts the money from the player's balance upon losing a game.
def bet_lost(bet, balance):
    return balance - int(bet)

#Calculates the total value of the player's hand so far.
def calculate_cards(hand):
    card_value = 0
    for i in hand:                                                              #For every card in the player's hand
        if i == "Jack" or i == "Queen" or i == "King":
            card_value += 10
        elif i == "Ace":
            card_value += 1
        else:
            card_value += int(i)
    return card_value

#Checks what decision the player made and performs a function accordingly.
def check_decision(decision, hand, value, bet):
    if int(decision) == 1:                               #Hit Function
        hit(hand)
        time.sleep(1)
        return int(bet), False
    elif int(decision) == 2:                             #Stand Function
        if value >= 17:                                  #Checks whether the player's hand value is above 17
            print("Good job!")
            time.sleep(1)
            return int(bet), True
        else:
            print("Not enough to compare!")
            time.sleep(1)
            return_hand(hand)
            return int(bet), False
    elif int(decision) == 3:
        bet = double_down(bet, hand)                     #Double Down Function
        time.sleep(1)
        return int(bet), False
    else:                                                #Checks for any invalid input
        print("Invalid input!")
        print("")
        time.sleep(1)
        decision = input("What is your decision?\n"
                        "1. Hit\n"
                        "2. Stand\n"
                        "3. Double Down\n")
        check_decision(decision, hand, value, bet)

#Returns a new balance to the player based on the amount that was bet and whether the player won or not.
def give_reward(bet, balance, value, dealer_value):   
    if value <= 21:                                                                 #If the player's value is below 21
        print("Lets compare!")
        time.sleep(1)
        print("Your card value is", value)
        print("The dealer's card value is", dealer_value)
        time.sleep(1)
        print("")
        if dealer_value == 22:                                                      #If the dealer busted with a value over 21.
            print("Congrats, the dealer has BUSTED!  You've won", "$"+str(bet))
            add_earnings(int(bet))
            balance = bet_won(bet, balance)
        elif value > dealer_value:                                                  #If the player's hand is greater than the dealer's hand
            print("Congrats!  You've won", "$"+str(bet))
            add_earnings(int(bet))
            balance = bet_won(bet, balance)
        elif value == dealer_value:                                                 #If both the player and dealer tied
            print("Tie, Nobody wins!")
        else:                                                                       #If the dealer's value is greater than the player's value
            print("Too bad... You've lost", "$"+str(bet),".")
            print("Better luck next time!")
            add_earnings(int(-bet))
            balance = bet_lost(bet, balance) 
    else:                                                                           #If the player went over 21
        print("Too bad... You've lost", "$"+str(bet),".")
        print("Better luck next time!")
        add_earnings(int(-bet))
        balance = bet_lost(bet, balance)
    return balance                                                                  #Returns the player's new balance upon a win or lost

#Checks the player's choice to continue the game or not.
def check_choice():
    choice = input("Do you want to try again?  Y or N? ")
    if choice == 'Y' or choice == 'N':
        return choice
    else:                                                                           #Checks for invalid responses from the player.
        print("Invalid choice!")
        time.sleep(1)
        return check_choice()                                                       #Recursive call so that the player can try again.

#Starts the game and continues to loop until the player wants to discontinue
#The second loop of start_game() keeps looping until the player's hand value goes over 21 for a bust or ends the hand.
def start_game():
    end_hand = False                                                                #Boolean value to end the loop if chosen within the decisions
    player_balance = 10000                                                          #The player starts with $10000
    choice = 'Y'
    
    #Loops until the player wants to stop playing Blackjack                         #String value  to loop the game or end it if chosen.
    while choice == 'Y':                                                            #Loops the game until the player says 'N'
        life = True                                                                 #Loops until either the player has won or lost a game of Blackjack
        print("Your currrent balance is", "$"+str(player_balance))
        player_bet = int(input("Place your bet: "))

        #Input for player to bet any amount of money
        print("You bet:", "$"+str(player_bet))
        print("")
        time.sleep(2)

        #Creates the player's hand and dealer's hand value randomly for comparision
        player_hand=[]
        make_hand(player_hand)
        value = calculate_cards(player_hand)
        dealer_value = random.randint(17,22)

        #Loops until the game is done
        while life:
            print("Your current hand is:", player_hand)
            value = calculate_cards(player_hand)
            print("The total value of your hand is: ", value)
            if value <= 21:
                player_decision = input("What is your decision?\n"
                                        "1. Hit\n"
                                        "2. Stand\n"
                                        "3. Double Down\n")
                player_bet, end_hand = check_decision(player_decision, player_hand, value, player_bet)
                print("")
                if end_hand:
                    life = False
            else:
                print("BUSTED")
                life = False

        #Results from one game of Blackjack
        player_balance = give_reward(player_bet, player_balance, value, dealer_value)
        print("")
        choice = check_choice()
        print("")
        time.sleep(1)
    #Returns the new player balance from any amount of Blackjack games played.    
    return player_balance

#________________________________________________________________________________________
#Main code
#Card list
cards = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
#Earnings variable set globally
earnings = 0

print("Welcome to Blackjack!")
start_game()
print("You've earned a total amount of ", "$"+str(earnings), " from playing Blackjack.")
time.sleep(1)

#Prints text based on earnings
if earnings > 0:
    print("Nice job on earning some money, Try not to lose it!")
    time.sleep(1)
else:
    print("Looks like luck wasn't on your side, not that it was ever there to begin with hahahaha!")
    time.sleep(1)

print("Thanks for playing!")
#Ends the program
exit(1)