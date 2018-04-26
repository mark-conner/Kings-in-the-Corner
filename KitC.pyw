#KitC.py
#Main loops and testing

from graphics import *
from sys import exit
from time import sleep
from mark import *
from chris import *
from taylor import *


def main():
    """This is the main function that runs the game."""
    playFx = Sounds() #Define the mouse click sound and set to on
    playFx.setOn(True)
    playMusic("assets\\Sounds\\music.wav")
    gb, winText, instText = gameBoard() #Define the game board object
    playerList, cardBack = start(gb) # Get number of players
    playFx.playSound()
    if cardBack == "assets\\Images\\CardBacks\\BlazerBill.gif":
        test = Image(Point(17,0),"assets\\Images\\CCBG.gif")
    else: 
        test = Image(Point(17,0),'assets\\Images\\test.gif')
    test.draw(gb)
    menuB = Image(Point(-31,36),'assets\\Images\\menubutton.gif')
    menuB.draw(gb)
    winText.draw(gb)
    instText.draw(gb)
    stack = stackSetup(gb,cardBack) #Define and initialize the stacks on the 'gb'
    stack[0].inventory = deck() #Create a shuffled deck of cards and assign it to the draw pile.
    stack[0].showCardBack(True) #Show the card back in the draw pile
    winner = False
    
    
    dealCards(stack, gb, playerList,cardBack) #Deal cards to player

    while True: #Infinite game loop
        for player in range(4): #Cycle through players
            if playerList[player] is 1: #Loop for real player
                winText.setText("Player "+str(player+1)+"'s Turn.") #Display which player's turn.
                winner = playerTurn(player, stack, gb,playFx,instText) #Execute player's turn, returns True if they are out of cards.
            elif playerList[player] is 0: #Loop for computer player
                winText.setText("Computer "+str(player+1)+"'s Turn.") #Display which player's turn.
                winner = computerTurn(player, stack, gb, playFx) #Execute computer's turn, returns True if it is out of cards.
            if winner: #Check for current player winning
                if playerList[player]: winText.setText("Player "+str(player+1)+" Has Won The Game!")
                else: winText.setText("Computer "+str(player+1)+" Has Won The Game!")
                winText.setTextColor("yellow")
                instText.setText("")
                winText.setSize(15)
                while True:
                    __mouseClick(gb,playFx)
            
                


def dealCards(stack, win, playerList,CB):
    """Function to deal cards to players and place cards on 'win' game board."""
    for player in range(4): #Deal cards to players hands
        hand = player + 9 #First player stack is at stack[9]
        stack.append(Stack([], "h"+str(player), win,CB)) #Create a new stack object for the players hand
        if playerList[player] != 2:
            deal(stack, hand, 0) #Give the player seven cards from the draw pile
            stack[hand].showCardBack(True) #Display the card back on the player's stack
                    
    for i in range(1, 5): #Deal one card to N,S,E,W stacks
        draw(stack, i, 0)
        stack[i].showStack(True)
        

def playerTurn(curPlayer, stack, win, playFx, instText):
    """This function contains all of the control logic for a turn and
returns True if the player is out of cards."""
    playerStack = curPlayer+9 #First player hand is stack 9
    instText.setText("Select your hand to show your cards.")
    __chkStkClick(stack, playerStack, win,playFx) #Checking when player selects their hand.
    stack[playerStack].showHand(True)
    if len(stack[0].getInventory()) > 0: #If there are cards in the Draw Pile, player must draw a card.
        instText.setText("You must draw a card.")
        __chkStkClick(stack, 0, win,playFx) #Checking when player draws a card.
        stack[playerStack].showHand(False)
        draw(stack, playerStack, 0) #Draw one card from draw pile
        stack[playerStack].showHand(True)
    if len(stack[0].getInventory()) > 0: instText.setText("Draw a card to end your turn.")
    else: instText.setText("Select your hand to end your turn.")
        
    while True: #Infinite play cards loop
        firstClick = __mouseClick(win,playFx) #Get first click selection
        if __chkForDraw(stack, playerStack, firstClick, win, playFx, instText): return False #Check if player wants to end turn already and return did not win
        firstCard = handCard(stack, playerStack, firstClick) #Get the card selected from hand, or False if not a card from player's hand
        firstStack = getStack(stack, firstClick) #Get the stack selected, or False if not a stack

        #Loop for moving a card from players hand
        while firstCard is not False: 
            stack[playerStack].getInventory()[firstCard].highlightCard(True) #Highlight the card
            secondClick = __mouseClick(win,playFx) #Get the second selection
            if __chkForDraw(stack,playerStack,secondClick, win, playFx, instText):
                stack[playerStack].getInventory()[firstCard].highlightCard(False)
                return False #Checking if player ends their turn and return did not win
            secondStack = getStack(stack, secondClick) #Get number of To stack selected

            #Did player want to unselect their first choice
            if handCard(stack,playerStack,secondClick) is firstCard: #Checking if first and second selections are the same
                stack[playerStack].getInventory()[firstCard].highlightCard(False) #Unhighlight card
                firstCard = False
            #Kings can only move to empty corners
            elif (stack[playerStack].getInventory()[firstCard].getValue() == 12 and #Check for card being a King
                  len(stack[secondStack].getInventory()) == 0 and #Check for second stack being empty
                  secondStack >=5 and secondStack <=8): #Check for second stack being a corner
                moveCard(stack, playerStack, firstCard, getStack(stack, secondClick))
                firstCard = False
            #All other cards may move to empty N, S, E, W stacks
            elif (stack[playerStack].getInventory()[firstCard].getValue() != 12 and #Check for card is not a King
                  len(stack[secondStack].getInventory()) == 0 and #Check for second stack being empty
                  secondStack >=1 and secondStack <=4): #Check for second stack being a corner N, S, E, W stack
                moveCard(stack, playerStack, firstCard, secondStack)
                firstCard = False
            #A Card of opposite color, one value less than bottom of stack may move
            elif (len(stack[secondStack].getInventory()) > 0 and #Check stack is not empty to avoid error
                  stack[playerStack].getInventory()[firstCard].getValue() == stack[secondStack].getInventory()[-1].getValue()-1 and #Check if hand card is one value less than bottom To stack
                  stack[playerStack].getInventory()[firstCard].getColor() != stack[secondStack].getInventory()[-1].getColor()and #Check that cards are opposite color
                  stack[playerStack].getInventory()[firstCard] != 12): #Check that card is not a King
                moveCard(stack, playerStack, firstCard, secondStack)
                firstCard = False
            #If there is an empty stack, a valid card may be inserted at the top of a stack
            elif (__chkForEmptyStacks(stack) and #Check if any N,S,E,W stack is empty
                  len(stack[secondStack].getInventory()) > 0 and #Check stack is not empty to avoid error
                  stack[playerStack].getInventory()[firstCard].getValue() == stack[secondStack].getInventory()[0].getValue()+1 and #Check if hand card is one value more than top To stack
                  stack[playerStack].getInventory()[firstCard].getColor() != stack[secondStack].getInventory()[0].getColor()and #Check that cards are opposite color
                  stack[playerStack].getInventory()[firstCard] != 12): #Check that card is not a King
                moveCard(stack, playerStack, firstCard, secondStack, top=True)
                firstCard = False
            #Check if players hand is empty
            if len(stack[playerStack].getInventory()) == 0:
                return True

        #Loop for moving a stack
        while (firstStack is not False and 
               firstStack >=1 and firstStack <=4 and #Only N,S,E,W stacks can be selected to move
               len(stack[firstStack].getInventory()) > 0): #Check that first stack has cards
            stack[firstStack].highlightStack(True) #Highlight the stack
            secondClick = __mouseClick(win,playFx)
            if __chkForDraw(stack,playerStack,secondClick,win,playFx,instText): #Checking if player ends turn
                stack[firstStack].highlightStack(False)
                return
            secondStack = getStack(stack, secondClick) # Get second stack selected
            if secondStack is firstStack: #Check if player wants to unselect stack
                stack[firstStack].highlightStack(False) #Unhighlight the stack
                firstStack = False
            #Move fistStack with a King to an empty corner
            elif (stack[firstStack].getInventory()[0].getValue() == 12 and #Check for first card being a King
                  len(stack[secondStack].getInventory()) == 0 and #Check for second stack being empty
                  secondStack >=5 and secondStack <=8): #Check for second stack being a corner
                moveStack(stack, firstStack, secondStack)
                firstStack = False
            #Check for secondStack being empty (moving a stack to an empty stack)
            elif (stack[firstStack].getInventory()[0].getValue() != 12 and #Check for first card not being a King
                  len(stack[secondStack].getInventory()) == 0 and #Check for second stack being empty
                  secondStack >=1 and secondStack <=4): #Check for second stack being N,S,E,W stack
                moveStack(stack, firstStack, secondStack)
                FirstStack = False
            #Move stack if top card firstStack is one less and different color of bottom of secondStack
            elif (stack[firstStack].getInventory()[0].getValue() == stack[secondStack].getInventory()[-1].getValue()-1 and #Check if top From stack is one value less than bottom To stack
                  stack[firstStack].getInventory()[0].getColor() != stack[secondStack].getInventory()[-1].getColor()and #Check that cards are opposite color
                  stack[firstStack].getInventory()[0] != 12): #Check that top From card is not a King
                moveStack(stack, firstStack, secondStack)
                firstStack = False

def computerTurn(curPlayer, stack, win, playFx):
    """Computer AI player"""
    playerStack = curPlayer+9
    stack[playerStack].showHand(True, player=False)
    playFx.playSound()
    if len(stack[0].getInventory()) > 0: #Check draw pile for cards left
        sleep(0.5)
        stack[playerStack].showHand(False, player=False)
        draw(stack, playerStack, 0)
        stack[playerStack].showHand(True, player=False)
        playFx.playSound()
    moveMade = True
    sleep(0.5)
    while moveMade: #Main play loop
        sleep(0.5)
        stack[playerStack].getInventory().sort(key =  lambda card: card.value)
        print("Cards in hand:", end = " ")
        for i in range(len(stack[playerStack].getInventory())):
            print(stack[playerStack].getInventory()[i].getValue(), end=' ')
        print()
        while moveMade: #Loop to move stacks and cards from hand, even with empty stacks
            print("Started over.")
            sleep(0.5)
            moveMade = False
            
            #Loop to check for movable stacks
            for firstStack in range(1,5):
                print("Checking stack", firstStack, "as firstStack")
                if (len(stack[firstStack].getInventory()) > 0 and #Make sure there are cards in the stack
                    stack[firstStack].getInventory()[0].getValue() == 12): #If there is a King to move
                    for secondStack in range(5, 9): #Find an empty corner stack
                        print("Found a king at ,", secondStack)
                        if (len(stack[secondStack].getInventory())==0): #Check for empty stack
                            moveStack(stack, firstStack, secondStack, rp=False)
                            playFx.playSound()
                            sleep(1)
                            moveMade = True
                            break
                    if moveMade: break #Start over
                elif len(stack[firstStack].getInventory()) > 0: #Check if stack can move
                    for secondStack in range(1, 9):
                        print("Checking second stack for move", secondStack)
                        if (len(stack[secondStack].getInventory()) > 0 and #If top firstStack value is one less and opposite color of bottom secondStack
                            stack[firstStack].getInventory()[0].getValue() == stack[secondStack].getInventory()[-1].getValue()-1 and #Check if top firstStack is one value less than bottom secondStack
                            stack[firstStack].getInventory()[0].getColor() != stack[secondStack].getInventory()[-1].getColor()): #Check that cards are opposite color
                            print("Found at stack to move to at,", secondStack)
                            moveStack(stack, firstStack, secondStack, rp=False)
                            playFx.playSound()
                            sleep(1)
                            moveMade = True
                            break
            if moveMade: break #Start over
            
            #Loop to check for playable cards from hand
            for firstCard in range(len(stack[playerStack].getInventory())):
                print("Checking hand ", firstCard, len(stack[playerStack].getInventory()))
                if (stack[playerStack].getInventory()[firstCard].getValue() == 12): #Check for playable king
                    print("Found a king at,", firstCard)
                    for secondStack in range(5, 9): #Find empty corner
                        print("Checking stack for empty corner", secondStack)
                        if (len(stack[secondStack].getInventory()) == 0): #Check for empty stack
                            moveCard(stack, playerStack, firstCard, secondStack, rp=False)
                            moveMade =True
                            playFx.playSound()
                            sleep(1)
                            print("Moved king from card",firstCard,"to stack",secondStack)
                            break
                if moveMade: break #Start over        
                elif (stack[playerStack].getInventory()[firstCard].getValue() < 12): #Check for a place to play firstCard on any stack
                    for secondStack in range(1, 9):
                        print("Checking stack to move card to", secondStack)
                        #A Card of opposite color, one value less than bottom of stack may move
                        if (len(stack[secondStack].getInventory()) > 0 and #secondStack should not be empty yet
                            stack[playerStack].getInventory()[firstCard].getValue() == stack[secondStack].getInventory()[-1].getValue()-1 and #Check if hand card is one value more than top To stack
                            stack[playerStack].getInventory()[firstCard].getColor() != stack[secondStack].getInventory()[-1].getColor()): #Check that cards are opposite color
                            moveCard(stack, playerStack, firstCard, secondStack, rp=False)
                            moveMade = True
                            playFx.playSound()
                            sleep(1)
                            print("Moved", firstCard, "Card to stack",secondStack)
                            break
                        #If there is an empty stack, a valid card may be inserted at the top of a stack
                        elif (__chkForEmptyStacks(stack) and #Check if any N,S,E,W stack is empty
                              secondStack < 5 and #Second stack cannot be a corner
                              len(stack[secondStack].getInventory()) > 0 and #Check stack is not empty to avoid error
                              stack[playerStack].getInventory()[firstCard].getValue() == stack[secondStack].getInventory()[0].getValue()+1 and #Check if hand card is one value more than top To stack
                              stack[playerStack].getInventory()[firstCard].getColor() != stack[secondStack].getInventory()[0].getColor()): #Check that cards are opposite color
                            moveCard(stack, playerStack, firstCard, secondStack, top= True, rp=False)
                            moveMade = True
                            playFx.playSound()
                            sleep(1)
                            print("Moved", firstCard, "Card to top of stack",secondStack,"************************")
                            break
                if moveMade: break #Start over
            if len(stack[playerStack].getInventory()) == 0:
                return True
        #If no moves left and there are empty stacks
        stack[playerStack].getInventory().sort(key =  lambda card: card.value)#Sort cards highest to lowest value
        for secondStack in range(1, 5):
            if (len(stack[secondStack].getInventory()) == 0):
                moveCard(stack, playerStack, 0, secondStack, rp=False)
                playFx.playSound()
                moveMade = True
                if len(stack[playerStack].getInventory()) == 0:
                    return True
            if moveMade: break #Start over
    if len(stack[0].getInventory()) > 0: #Check draw pile for cards left
        stack[playerStack].showHand(False, player=False)
        draw(stack, playerStack, 0)
        playFx.playSound()
        stack[playerStack].showHand(True, player=False)
        sleep(0.5)
    stack[playerStack].showHand(False, player=False)
    playFx.playSound()
    sleep(0.5)
    return False

def helpWindow(win,playFx):
    """Function to activate help window"""
    opaque = Image(Point(17,0),'assets\\Images\\opaquelayer.pbm')
    menu = Image(Point(-23,32),'assets\\Images\\OpenMenu.gif')
    
    opaque.draw(win)
    menu.draw(win)

    x = True
    check = Image(Point(-15,28),'assets\\Images\\checkbox.gif')
    if playFx.getSoundOn():
        check.draw(win)
        
    while x:
        p = win.getMouse()
        playFx.playSound()
        print(p.getX(),"",p.getY())
        if (p.getX() < -30 and p.getY() > 35):            
            opaque.undraw()
            menu.undraw()
            if playFx.getSoundOn():
                check.undraw()
            x = False

        elif (-29 < p.getX() < -14 and
            35 < p.getY() < 37):
            img = Image(Point(17, 0), "assets\\Images\\RUSure.gif").draw(win)
            while True:
                p = win.getMouse()
                if (8 < p.getX() < 16 and -2.5 < p.getY() < 1):
                    win.close()
                    main()
                elif (19 < p.getX() < 26 and -2.5 < p.getY() < 1):
                    img.undraw()
                    break

        elif (-32 < p.getX() < -14 and
            32 < p.getY() < 34):
            hlpImg = Image(Point(17,0),"assets\\Images\\helpScreen.gif").draw(win)
            win.getMouse()
            playFx.playSound()
            hlpImg.undraw()
            
        elif (-32 < p.getX() < -14 and
              29 < p.getY() < 32):
            creditsImg = Image(Point(17,0),"assets\\Images\\credits.gif").draw(win)
            text = [Text(Point(17, 25), "A joint project by The PyKings:"),
                    Text(Point(17, 23), "Taylor Chambers"),
                    Text(Point(17, 21), "Mark Conner"),
                    Text(Point(17, 19), "Chris Hollemon"),
                    Text(Point(17, 15), "Special Thanks to Instructor Samuel Small"),
                    Text(Point(17, 13), "And Centralia Community College."),
                    Text(Point(17, 0), "Blazer Bill and Centralia College Logos courtesy of\nCentralia Community College."),
                    Text(Point(17, -5), "Title screen background music provided by Looperman.com\nSound Effects provided by Freesound.org")]
            for i in text:
                i.setTextColor("White")
                i.draw(win)
            win.getMouse()
            playFx.playSound()
            for i in text: i.undraw()
            creditsImg.undraw()
            
        elif (-32 < p.getX() < -14 and
            26 < p.getY() < 29):
            playFx.setOn(not playFx.getSoundOn()) 
            if playFx.getSoundOn():
                check.draw(win)
            else:
                check.undraw()
                
def __chkForEmptyStacks(stack):
    """A Function that returns True if a N,S,E,W stack is empty."""
    for i in range(1, 5):
        if len(stack[i].getInventory()) == 0: return True
    return False
    
def __chkForDraw(stack, playerStack ,point ,win,playFx,instText):
    """A Function to check if player has ended their turn."""
    if len(stack[0].getInventory()) > 0:  #If Draw Pile still has cards
        if stack[0].originClicked(point):
               stack[playerStack].showHand(False)
               draw(stack, playerStack, 0)
               if len(stack[0].getInventory()) == 0: #If last card removed from Draw Pile, remove the card back
                   stack[0].showCardBack(False)
               stack[playerStack].showHand(True)
               instText.setText("Select your hand to switch players.")
               __chkStkClick(stack, playerStack, win,playFx)
               stack[playerStack].showHand(False)
               instText.setText("")
               return True
        else: return False
    elif stack[playerStack].originClicked(point): #If Draw Pile is empty
        stack[playerStack].showHand(False)
        instText.setText("")
        return True
    else: return False #Draw Pile was not selected and/or 
            
def __chkStkClick(stack, chkStack, win,playFx):
    """A Helper Function to wait for player's stack to be selected"""
    x= False
    while x == False:
        p = __mouseClick(win,playFx)
        x = stack[chkStack].originClicked(p)

def __mouseClick(win,playFx):
    """A Helper Function to get a point from a mouse click.  Will exit nicely if the window is closed."""
    try:
        p = win.getMouse()
        playFx.playSound()
        if (p.getX() < -30 and p.getY() > 35): helpWindow(win, playFx)
        return p
    except GraphicsError: sys.exit() #Exit nicely if the window is closed


if __name__ == "__main__": main()
