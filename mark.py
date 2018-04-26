#window.py
#Defining the playing field and stack object
#By Mark Conner

from graphics import *


class Stack:
    """This class defines the Stack objects that cards are played on to
on the game board. The stack contains a list of cards, which stack it is, and
methods to draw, undraw and highlight the stacks, and return if a point falls
within the stack."""

    def __init__(self, inventory, position, win,CB):
        """'inventory' is the list of card objects.
'posistion' is a string containing the position on the board or around the draw pile (N, NE, E, SE, etc).
'win' is the game board object
Other variables initialized:
'selected' determines if the stack is selected for highlighting;
'showBack' determines if the stack is hidden (card back showing);
'x', 'y' starting center locations of stacks;
'dirX', 'dirY' used to calculate verical and horizontal direction to expand the stack;
'vert' boolean value to determine which way to draw the card;
'outline' The outline for the stack origin"""
        self.inventory = inventory
        self.CB = CB
        self.win = win
        self.selected = False
        self.showBack = False
        self.x, self.y, self.dirX, self.dirY = 0, 0, 0, 0 #Initialize center x, y and expansion directions
        self.vert = False #Initialize cards to draw horizontally, must set to True to draw vertically.
                
        #Determine center, expansion direction, and orientation of stack
        if position.find("d") != -1: #Draw Pile: Stays at center, no expansion, drawn verticle
            self.vert = True
        if position.find("n") != -1: #NW, N, NE stacks:showStack Offset up, expand upwards, draw verticle
            self.y += 9
            self.dirY += 1
            self.vert = True
        if position.find("s") != -1: #SW, S, SE stacks: Offset down, expand downwards, draw verticle
            self.y += -9
            self.dirY += -1
            self.vert = True
        if position.find("e") != -1: #NE, E, SE stacks: Offset right, exapand right. If only E, 'vert' remains False to draw card horizontally
            self.x += 8
            self.dirX += 1
        if position.find("w") != -1: #NW, W, SW stacks: Offset left, exapand left. If only W, 'vert' remains False to draw card horizontally
            self.x += -8
            self.dirX += -1
        if position.find("h0") != -1: #Player 1: Set position on board, no expansion, draw vertical
            self.x += 36
            self.y += 18
            self.vert = True
        if position.find("h1") != -1: #Player 2: Set position on board, no expansion, draw vertical
            self.x += 43
            self.y += 18
            self.vert = True
        if position.find("h2") != -1: #Player 3: Set position on board, no expansion, draw vertical
            self.x += 50
            self.y += 18
            self.vert = True
        if position.find("h3") != -1: #Player 4: Set position on board, no expansion, draw vertical
            self.x += 57
            self.y += 18
            self.vert = True
            
        #Define the outline of the stack origin on the gameboard.
        self.origin = Rectangle(Point(self.x-(3 + (not self.vert)),self.y-(3 + self.vert)),
                                Point(self.x+(3 + (not self.vert)),self.y+(3 + self.vert))).draw(self.win)
								 

        #Define the card back image for the stack
        
        self.cardBack = Image(Point(self.x, self.y),self.CB)

    def getInventory(self):
        """Method used to retrieve the list of cards in the stack."""
        return self.inventory

    def getOrigin(self):
        """Method used to return the outline object of the stack."""
        return self.origin

    def getClicked(self, p):
        """Method used to return True if 'p' Point(x,y) is within the stack area."""
        return self.originClicked(p) or self.cardsClicked(p)

    def originClicked(self, p):
        """Method used to return if the origin area of the stack is clicked"""
        return (self.origin.getP1().getX() <= p.getX() <= self.origin.getP2().getX() and
                self.origin.getP1().getY() <= p.getY() <= self.origin.getP2().getY())

    def cardsClicked(self, p):
        """Method used to determine if cards in the stack were clicked"""
        for i in range(len(self.inventory)):
            if (self.inventory[i].getOutline().getP1().getX() <= p.getX() <= self.inventory[i].getOutline().getP2().getX() and
                self.inventory[i].getOutline().getP1().getY() <= p.getY() <= self.inventory[i].getOutline().getP2().getY()):
                return True
        return False

    def showStack(self, show):
        """Method used to draw or undraw a stack on the game board. Draws the card
if 'show' is True, otherwise removes the card."""
        for i in range(len(self.inventory)):
            if show: self.inventory[i].drawCard(Point((self.x+i*self.dirX), (self.y+i*self.dirY)), self.vert, self.win)
            else: self.inventory[i].undraw()

    def highlightStack(self, selected):
        """Method used to highlight the stack on the game board
if 'selected' is true, or unhighlight otherwise."""
        for i in range(len(self.inventory)):
            self.inventory[i].highlightCard(selected)

    def showCardBack(self, show):
        """Shows back of card on stack on game board if 'show' is True."""
        if show: self.cardBack.draw(self.win)
        else: self.cardBack.undraw()
		
    def showHand(self, show, player=True):
        """Display players hand on game board if 'show' is True, hide otherwise"""
        if show:
            self.showCardBack(False)
            x, y = 36, 7 #initial column, row
            self.cardBackList = []
            for i in range(len(self.getInventory())):
                if player: self.inventory[i].drawCard(Point(x, y), self.vert, self.win)
                else:
                    self.cardBackList.append(Image(Point(x, y), self.CB))
                    self.cardBackList[i].draw(self.win)
                x += 7 #Next card shows to the right
                if x > 57: x, y = 36, y - 9 #If more than 4 cards, row is full. Back to first column, down one row.
        else:
            if player:
                self.showStack(False)
            else:
                for i in self.cardBackList:
                    i.undraw()
            self.showCardBack(True)

def gameBoard(color = "green", width = 1024, height = 768):
    """This function returns the game board object with the empty stacks,
hands, text object, and help button."""
    window = GraphWin("Kings in the Corner", width, height) #Create the main game window
    window.setBackground(color)
    window.setCoords(-33, -38, 67, 38)
    
    playerText = Text(Point(0,35),"") #Define a text object on the board
    playerText.setTextColor("white")
    instText = Text(Point(0,30),"") #Define a text object on the board
    instText.setTextColor("yellow")
    return window, playerText, instText

def stackSetup(win,CB):
    """Creat empty stacks and draw outlines on 'win' game board."""
    position = ["d", "n", "e", "s", "w", "ne", "se", "sw", "nw"]
    stack = []
    for i in range(len(position)):
        stack.append(Stack([], position[i], win, CB))   
    return stack


if __name__ == "__main__": gameBoard()
