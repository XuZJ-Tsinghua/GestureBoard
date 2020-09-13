import board
import matplotlib.pyplot as plt




def paintPointOnBoard(x,y):
    img = plt.imread("keyboard.png")
    fig, ax = plt.subplots()
    ax.scatter([x], [y])
    plt.imshow(img)
    plt.show()

def paintCurveOnBoard(curveX,curveY):
    img = plt.imread("keyboard.png")
    fig, ax = plt.subplots()
    ax.scatter(curveX, curveY, s=1)
    plt.imshow(img)
    plt.show()
# x, y = board.getCharacterPos('A')
# paintPointOnBoard(x, y)

