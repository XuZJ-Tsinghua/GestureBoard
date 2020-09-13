WIDTH = 626
HEIGHT = 220
KEY_WIDTH = WIDTH/10
KEY_HEIGHT = HEIGHT/3
posDict = {'Q':(KEY_WIDTH/2,KEY_HEIGHT/2),
           'W':(KEY_WIDTH/2+KEY_WIDTH,KEY_HEIGHT/2),
           'E':(KEY_WIDTH/2+KEY_WIDTH*2,KEY_HEIGHT/2),
           'R':(KEY_WIDTH/2+KEY_WIDTH*3,KEY_HEIGHT/2),
           'T':(KEY_WIDTH/2+KEY_WIDTH*4,KEY_HEIGHT/2),
           'Y':(KEY_WIDTH/2+KEY_WIDTH*5,KEY_HEIGHT/2),
           'U':(KEY_WIDTH/2+KEY_WIDTH*6,KEY_HEIGHT/2),
           'I':(KEY_WIDTH/2+KEY_WIDTH*7,KEY_HEIGHT/2),
           'O':(KEY_WIDTH/2+KEY_WIDTH*8,KEY_HEIGHT/2),
           'P':(KEY_WIDTH/2+KEY_WIDTH*9,KEY_HEIGHT/2),
           'A':(KEY_WIDTH,KEY_HEIGHT/2+KEY_HEIGHT),
           'S':(KEY_WIDTH*2,KEY_HEIGHT/2+KEY_HEIGHT),
           'D':(KEY_WIDTH*3,KEY_HEIGHT/2+KEY_HEIGHT),
           'F':(KEY_WIDTH*4,KEY_HEIGHT/2+KEY_HEIGHT),
           'G':(KEY_WIDTH*5,KEY_HEIGHT/2+KEY_HEIGHT),
           'H':(KEY_WIDTH*6,KEY_HEIGHT/2+KEY_HEIGHT),
           'J':(KEY_WIDTH*7,KEY_HEIGHT/2+KEY_HEIGHT),
           'K':(KEY_WIDTH*8,KEY_HEIGHT/2+KEY_HEIGHT),
           'L':(KEY_WIDTH*9,KEY_HEIGHT/2+KEY_HEIGHT),
           'Z':(KEY_WIDTH/2+KEY_WIDTH*1,KEY_HEIGHT/2+KEY_HEIGHT*2),
           'X':(KEY_WIDTH/2+KEY_WIDTH*2,KEY_HEIGHT/2+KEY_HEIGHT*2),
           'C':(KEY_WIDTH/2+KEY_WIDTH*3,KEY_HEIGHT/2+KEY_HEIGHT*2),
           'V':(KEY_WIDTH/2+KEY_WIDTH*4,KEY_HEIGHT/2+KEY_HEIGHT*2),
           'B':(KEY_WIDTH/2+KEY_WIDTH*5,KEY_HEIGHT/2+KEY_HEIGHT*2),
           'N':(KEY_WIDTH/2+KEY_WIDTH*6,KEY_HEIGHT/2+KEY_HEIGHT*2),
           'M':(KEY_WIDTH/2+KEY_WIDTH*7,KEY_HEIGHT/2+KEY_HEIGHT*2)}


def getCharacter(x,y):
    # get the target character using its coordinate
    return 0


def getCharacterPos(ch):
    # get a character's position on a keyboard
    return posDict[ch]



