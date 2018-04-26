from winsound import *
from graphics import *
from KitC import __mouseClick
class Sounds:
    def __init__ (self):
        pass

    def getSoundOn(self):
        return self.soundOn        

    def playSound(self):
        if self.soundOn:
            PlaySound("assets\\Sounds\\mouseClk.wav", SND_ASYNC)
    def setOn(self,soundOn):
        self.soundOn = soundOn

def deal(stack, dest, source, handsize=7):
    for i in range(handsize):
        draw(stack, dest, source)

def draw(stack, dest, source):
    if len(stack[source].getInventory()) > 0:
        stack[dest].getInventory().append(stack[source].getInventory().pop())            

def moveStack(stack, fromStack, toStack, rp=True):
    if rp: stack[fromStack].highlightStack(False)
    stack[fromStack].showStack(False)
    stack[toStack].showStack(False)
    for i in range (len(stack[fromStack].getInventory())):
        stack[toStack].getInventory().append(stack[fromStack].getInventory().pop(0))
    stack[toStack].showStack(True)
         
def moveCard(stack,fromStack,cardNum,toStack,top = False, rp=True):
    if rp: stack[fromStack].getInventory()[cardNum].highlightCard(False)
    stack[fromStack].showHand(False, player=rp)
    stack[toStack].showStack(False)
    if top: stack[toStack].getInventory().insert(0,stack[fromStack].getInventory().pop(cardNum))
    else: stack[toStack].getInventory().append(stack[fromStack].getInventory().pop(cardNum))
    stack[toStack].showStack(True)
    stack[fromStack].showHand(True, player=rp)

def handCard(stack,playerHand,p):
    for i in range (len(stack[playerHand].getInventory())):
        if (stack[playerHand].getInventory()[i].getOutline().getP1().getX() <= p.getX() <= stack[playerHand].getInventory()[i].getOutline().getP2().getX() and
            stack[playerHand].getInventory()[i].getOutline().getP1().getY() <= p.getY() <= stack[playerHand].getInventory()[i].getOutline().getP2().getY()):
            return i
    return False

def getStack(stack,p):
    for i in range(1,9):
        if stack[i].getClicked(p):
            return i
    return False
        
def playMusic(tune):
    music = tune
    PlaySound(music,
    SND_ASYNC | SND_LOOP)

def start(win):
    start = Image(Point(17,0),'assets\\images\\titlescreen.gif')
    Ps = Image(Point(17,0),'assets\\images\\playercardSelect.gif')
    Play = Image(Point(55.2,-24),'assets\\images\\play.gif')
    start.draw(win)
    playFx = Sounds()
    select1 = 1
    select2 = 0
    select3 = 2
    select4 = 2
    cardback = 4
    cbimg = "assets\\Images\\CardBacks\\cardback.gif"
    playFx.setOn(True)

    while True:
        p = __mouseClick(win,playFx)
        if (4.2 < p.getX() < 27 and
            -23.7 < p.getY() < -18.5):
            Ps.draw(win)
            Play.draw(win)
            break
        elif (4.2 < p.getX() < 27 and
            -32.6 < p.getY() < -25.3):
            win.close()
            sys.exit()

    while True:
        img = playerOrAi(select4)
        start = Image(Point(44,17.4),img)
        start.draw(win)
        img = playerOrAi(select3)
        start = Image(Point(26,17.4),img)
        start.draw(win)
        img = playerOrAi(select2)
        start = Image(Point(7.8,17.4),img)
        start.draw(win)
        img = playerOrAi(select1)
        start = Image(Point(-10,17.4),img)
        start.draw(win)
        cbimg = cBackSelect(cardback)
        cardBack = Image(Point(17,-22),cbimg)
        cardBack.draw(win)
        p = __mouseClick(win,playFx)
        
        if (-18 < p.getX() < -16 and
            16 < p.getY() < 18):
                select1 = select1 - 1
                select1 = __wraparound(select1,2)
                img = playerOrAi(select1)
                start = Image(Point(-10,17.4),img)
                start.draw(win)
                
        elif (-4 < p.getX() < -2 and
            16 < p.getY() < 18):
                select1 = select1 + 1
                select1 = __wraparound(select1,2)
                img = playerOrAi(select1)
                start = Image(Point(-10,17.4),img)
                start.draw(win)
                

        elif (-0.1 < p.getX() < 2 and
            16 < p.getY() < 18):
                select2 = select2 - 1
                select2 = __wraparound(select2,2)
                img = playerOrAi(select2)
                start = Image(Point(7.8,17.4),img)
                start.draw(win)
                
        elif (14 < p.getX() < 16 and
            16 < p.getY() < 18):
                select2 = select2 + 1
                select2 =__wraparound(select2,2)
                img = playerOrAi(select2)
                start = Image(Point(7.8,17.4),img)
                start.draw(win)
                

        elif (18 < p.getX() < 20 and
            16 < p.getY() < 18):
                select3 = select3 - 1
                select3 =__wraparound(select3,2)
                img = playerOrAi(select3)
                start = Image(Point(26,17.4),img)
                start.draw(win)
                
        elif (31 < p.getX() < 34 and
            16 < p.getY() < 18):
                select3 = select3 + 1
                select3 = __wraparound(select3,2)
                img = playerOrAi(select3)
                start = Image(Point(26,17.4),img)
                start.draw(win)
                

        elif (35 < p.getX() < 38 and
            16 < p.getY() < 18):
                select4 = select4 - 1
                select4 = __wraparound(select4,2)
                img = playerOrAi(select4)
                start = Image(Point(44,17.4),img)
                start.draw(win)
                
        elif (49 < p.getX() < 52 and
            16 < p.getY() < 18):
                select4 = select4 + 1
                select4 = __wraparound(select4,2)
                img = playerOrAi(select4)
                start = Image(Point(44,17.4),img)
                start.draw(win)
                
        elif (7 < p.getX() < 12 and
            -24 < p.getY() < -20):
                cardback = cardback -1
                cardback = __wraparound(cardback,4)
                cbimg = cBackSelect(cardback)
                cardBack = Image(Point(17,-22),cbimg)
                cardBack.draw(win)

        elif (22 < p.getX() < 25 and
            -24 < p.getY() < -20):
                cardback = cardback +1
                cardback = __wraparound(cardback,4)
                cbimg = cBackSelect(cardback)
                cardBack = Image(Point(17,-22),cbimg)
                cardBack.draw(win)

        elif (48 < p.getX() < 61 and
            -27 < p.getY() < -19):
            User =[]
            User.append(select1)
            User.append(select2)
            User.append(select3)
            User.append(select4)
            cardBack = cbimg
            
            if User != [2, 2, 2,2]: return User,cardBack
   
        


def __wraparound(selection,mx):
    if selection > mx:
        selection = 0

    elif selection < 0:
        selection = mx

    return selection

def playerOrAi(selection):
    if selection == 2:
        img = "assets\\Images\\noneCard.gif"
        return img

    elif selection == 1:
        img = "assets\\Images\\playerCard.gif"
        return img

    elif selection == 0:
        img = "assets\\Images\\AIcard.gif"
        return img

def cBackSelect(selection):
    if selection == 4:
        img = "assets\\Images\\CardBacks\\cardback.gif"
        return img

    elif selection == 3:
        img = "assets\\Images\\CardBacks\\PLANETS.gif"
        return img

    elif selection == 2:
        img = "assets\\Images\\CardBacks\\tree.gif"
        return img

    elif selection == 1:
        img = "assets\\Images\\CardBacks\\redBlack.gif"
        return img

    elif selection == 0:
        img = "assets\\Images\\CardBacks\\BlazerBill.gif"
        return img


    
                
        


    
                    

