"""
Battleship Project
Name:
Roll No:
"""

import battleship_tests as test

project = "Battleship" # don't edit this

### SIMULATION FUNCTIONS ###

from tkinter import *
import random

EMPTY_UNCLICKED = 1
SHIP_UNCLICKED = 2
EMPTY_CLICKED = 3
SHIP_CLICKED = 4


'''
makeModel(data)
Parameters: dict mapping strs to values
Returns: None
'''
def makeModel(data):
    data["row"]=10
    data["col"]=10
    data["board-size"]=500
    data["cell_size"]=data["board-size"]/data["row"]
    data["numShips"]=5
    boarduser = emptyGrid(data["row"], data["col"])
    #boarduser = test.testGrid()
    boardcompu = emptyGrid(data["row"], data["col"])
    boardcompu = addShips(boardcompu, data["numShips"])
    data["boarduser"] = boarduser
    data["temporaryShip"] = []
    #data["temporaryShip"] = test.testShip()
    data["boardcompu"] = boardcompu
    data["userturn"] = 0
    data["winner"] = None
    data["maxturns"] = 50
    data["currentnoofturns"] = 0
    return


'''
makeView(data, userCanvas, compCanvas)
Parameters: dict mapping strs to values ; Tkinter canvas ; Tkinter canvas
Returns: None
'''
def makeView(data, userCanvas, compCanvas):
    drawGrid(data,userCanvas,data["boarduser"],showShips=True)
    drawGrid(data,compCanvas,data["boardcompu"],showShips=False)
    drawShip(data,userCanvas,data["temporaryShip"])
    drawGameOver(data,userCanvas)
    return


'''
keyPressed(data, events)
Parameters: dict mapping strs to values ; key event object
Returns: None
'''
def keyPressed(data, event):
    if event.keycode == 13:
        makeModel(data)
    pass


'''
mousePressed(data, event, board)
Parameters: dict mapping strs to values ; mouse event object ; 2D list of ints
Returns: None
'''
def mousePressed(data, event, board):
    if data["winner"] != None:
        return
    click = getClickedCell(data,event)
    if board == "user":
         clickUserBoard(data,click[0], click[1])
    else:
        runGameTurn(data,click[0],click[1])
    return

#### WEEK 1 ####

'''
emptyGrid(rows, cols)
Parameters: int ; int
Returns: 2D list of ints
'''
def emptyGrid(rows, cols):
    list=[]
    for i in range(rows):
        col = []
        for j in range(cols):
            col.append(EMPTY_UNCLICKED)
        list.append(col)
    return (list)


'''
createShip()
Parameters: no parameters
Returns: 2D list of ints
'''
def createShip():
    #len_ship = 3
    orientation = random.randint(0,1)
    shiprow = random.randint(1,8)
    shipcol = random.randint(1,8)
    lst = [[]]
    if orientation == 0:
        lst=[[shiprow,shipcol-1],[shiprow,shipcol],[shiprow,shipcol+1]]
    else:
        lst=[[shiprow-1,shipcol],[shiprow,shipcol],[shiprow+1,shipcol]]
    return lst


'''
checkShip(grid, ship)
Parameters: 2D list of ints ; 2D list of ints
Returns: bool
'''
def checkShip(grid, ship):
    count = 1
    i=0
    while i<len(ship):
        l = ship[i]
        l1=l[0]
        l2=l[1]
        if(grid[l1][l2]!=EMPTY_UNCLICKED):
            count = 0
        i = i+1
    if(count==0):
        return False
    return True


'''
addShips(grid, numShips)
Parameters: 2D list of ints ; int
Returns: 2D list of ints
'''
def addShips(grid, numShips):
    count=0
    while count<numShips:
        ship = createShip()
        if checkShip(grid,ship) == True:
            for i in ship:
                l1 = i[0]
                l2 = i[1]
                grid[l1][l2] = SHIP_UNCLICKED
            count = count + 1
    return grid


'''
drawGrid(data, canvas, grid, showShips)
Parameters: dict mapping strs to values ; Tkinter canvas ; 2D list of ints ; bool
Returns: None
'''
def drawGrid(data, canvas, grid, showShips):
    for i in range(data["row"]):
        for j in range(data["col"]):
            if (grid[i][j] == SHIP_UNCLICKED):
                canvas.create_rectangle(j*data["cell_size"],i*data["cell_size"],data["cell_size"]*(j+1),data["cell_size"]*(i+1),fill="yellow")
            if (grid[i][j] == SHIP_UNCLICKED) and showShips == False:
                canvas.create_rectangle(j*data["cell_size"],i*data["cell_size"],data["cell_size"]*(j+1),data["cell_size"]*(i+1),fill="blue")
            elif (grid[i][j] == SHIP_CLICKED):
                canvas.create_rectangle(j*data["cell_size"],i*data["cell_size"],data["cell_size"]*(j+1),data["cell_size"]*(i+1),fill="red")
            elif (grid[i][j] == EMPTY_CLICKED):
                canvas.create_rectangle(j*data["cell_size"],i*data["cell_size"],data["cell_size"]*(j+1),data["cell_size"]*(i+1),fill="white")
            elif (grid[i][j] == EMPTY_UNCLICKED):
                canvas.create_rectangle(j*data["cell_size"],i*data["cell_size"],data["cell_size"]*(j+1),data["cell_size"]*(i+1),fill="blue")
    return


### WEEK 2 ###

'''
isVertical(ship)
Parameters: 2D list of ints
Returns: bool
'''
def isVertical(ship):
    '''ship.sort()
    if (ship[0][1] == ship[1][1] == ship[2][1]) and (ship[0][0] + 1 == ship[1][0] == ship[2][0] - 1):
        return True
    return False'''
    (x,y)=ship[0]
    count = 0
    lst = []
    for i in ship:
        if i[0]<=9:
            lst.append(i[0])
    lst.sort()
    #to find diffrence between the coordinates
    res = [lst[i + 1] - lst[i] for i in range(len(lst)-1)]
    #to check for same column
    for i in ship:
        if i[1]==y and res[0]==1 and res[1]==1:
            count += 1
        else:
            count -= 1
    if count == 3:
        return True
    return False


'''
isHorizontal(ship)
Parameters: 2D list of ints
Returns: bool
'''
def isHorizontal(ship):
    '''ship.sort()
    if (ship[0][0] == ship[1][0] == ship[2][0]) and (ship[0][1] + 1 == ship[1][1] == ship[2][1] - 1):
        return True
    return False'''
    (x,y)=ship[0]
    count = 0
    lst = []
    for i in ship:
        if i[1]<=9:
            lst.append(i[1])
    lst.sort()
    #to find diffrence between the coordinates
    res = [lst[i + 1] - lst[i] for i in range(len(lst)-1)]
    #to check for same column
    for i in ship:
        if i[0]==x and res[0]==1 and res[1]==1:
            count += 1
        else:
            count -= 1
    if count == 3:
        return True
    return False


'''
getClickedCell(data, event)
Parameters: dict mapping strs to values ; mouse event object
Returns: list of ints
'''
def getClickedCell(data, event):
    #lst = []
    x,y = int(event.x / data["cell_size"]), int(event.y / data["cell_size"])
    #lst.append(y)
    #x = int(event.x / data["cell_size"])
    #lst.append(x)
    return [y,x]


'''
drawShip(data, canvas, ship)
Parameters: dict mapping strs to values ; Tkinter canvas; 2D list of ints
Returns: None
'''
def drawShip(data, canvas, ship):
    #ship = test.testShip()
    for i in ship:
        canvas.create_rectangle(data["cell_size"]*i[1],data["cell_size"]*i[0],data["cell_size"]*(i[1]+1),data["cell_size"]*(i[0]+1),fill="white")
    return


'''
shipIsValid(grid, ship)
Parameters: 2D list of ints ; 2D list of ints
Returns: bool
'''
def shipIsValid(grid, ship):
    if len(ship) == 3:
        if checkShip(grid, ship) and isVertical(ship) or isHorizontal(ship):
            return True
    return False


'''
placeShip(data)
Parameters: dict mapping strs to values
Returns: None
'''
def placeShip(data):
    if shipIsValid(data["boarduser"],data["temporaryShip"]):
        for i in range(len(data["temporaryShip"])):
            data["boarduser"][data["temporaryShip"][i][0]][data["temporaryShip"][i][1]]=SHIP_UNCLICKED
        data["userturn"]+=1
    else:
        print("Ship is not valid")
    data["temporaryShip"]=[]
    return


'''
clickUserBoard(data, row, col)
Parameters: dict mapping strs to values ; int ; int
Returns: None
'''
def clickUserBoard(data, row, col):
    if data["userturn"] == 5:
        print("You can start the game")
        return
    for i in data["temporaryShip"]:
        if [row,col] == i:
            return
    data["temporaryShip"].append([row,col])
    if len(data["temporaryShip"]) == 3:
        placeShip(data)
    return


### WEEK 3 ###

'''
updateBoard(data, board, row, col, player)
Parameters: dict mapping strs to values ; 2D list of ints ; int ; int ; str
Returns: None
'''
def updateBoard(data, board, row, col, player):
    if board[row][col] == SHIP_UNCLICKED:
        board[row][col] = SHIP_CLICKED
    elif board[row][col] == EMPTY_UNCLICKED:
        board[row][col] = EMPTY_CLICKED
    if isGameOver(board):
        data["winner"] = player
    return


'''
runGameTurn(data, row, col)
Parameters: dict mapping strs to values ; int ; int
Returns: None
'''
def runGameTurn(data, row, col):
    if(data["boardcompu"][row][col] == SHIP_CLICKED) or (data["boardcompu"][row][col]==EMPTY_CLICKED):
        return
    else:
        updateBoard(data, data["boardcompu"],row,col,"user")
    i = getComputerGuess(data["boarduser"])
    updateBoard(data, data["boarduser"], i[0], i[1], "comp")
    data["currentnoofturns"] += 1
    if data["currentnoofturns"] == data["maxturns"]:
        data["winner"] = "draw"
    


'''
getComputerGuess(board)
Parameters: 2D list of ints
Returns: list of ints
'''
def getComputerGuess(board):
    row = random.randint(0,9)
    col = random.randint(0,9)
    while(board[row][col]==EMPTY_CLICKED or board[row][col]==SHIP_CLICKED):
        row = random.randint(0,9)
        col = random.randint(0,9)
    if (board[row][col] == EMPTY_UNCLICKED) or (board[row][col]== SHIP_UNCLICKED):
        return [row,col]
    return


'''
isGameOver(board)
Parameters: 2D list of ints
Returns: bool
'''
def isGameOver(board):
    for i in range(len(board[0])):
        l=len(board[i])
        for j in range(l):
            if board[i][j] == SHIP_UNCLICKED:
                return False
    return True
    return


'''
drawGameOver(data, canvas)
Parameters: dict mapping strs to values ; Tkinter canvas
Returns: None
'''
def drawGameOver(data, canvas):
    if data["winner"] == "user":
        canvas.create_text(250, 80, text="Congratulations, You Won !", fill="black", font=('Helvetica 15 bold'))
        canvas.create_text(250, 120, text="Click enter to start over again !", fill="black", font=('Helvetica 15 bold'))
    elif data["winner"] == "draw":
        canvas.create_text(250, 80, text="Out of moves, It's a Draw !", fill="black", font=('Helvetica 15 bold'))
        canvas.create_text(250, 120, text="Click enter to start over again !", fill="black", font=('Helvetica 15 bold'))
    elif data["winner"] == "comp":
        canvas.create_text(250, 80, text="Oh no, You lost !", fill="black", font=('Helvetica 15 bold'))
        canvas.create_text(250, 120, text="Click enter to start over again !", fill="black", font=('Helvetica 15 bold'))
    return


### SIMULATION FRAMEWORK ###

from tkinter import *

def updateView(data, userCanvas, compCanvas):
    userCanvas.delete(ALL)
    compCanvas.delete(ALL)
    makeView(data, userCanvas, compCanvas)
    userCanvas.update()
    compCanvas.update()

def keyEventHandler(data, userCanvas, compCanvas, event):
    keyPressed(data, event)
    updateView(data, userCanvas, compCanvas)

def mouseEventHandler(data, userCanvas, compCanvas, event, board):
    mousePressed(data, event, board)
    updateView(data, userCanvas, compCanvas)

def runSimulation(w, h):
    data = { }
    makeModel(data)

    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window

    # We need two canvases - one for the user, one for the computer
    Label(root, text = "USER BOARD - click cells to place ships on your board.").pack()
    userCanvas = Canvas(root, width=w, height=h)
    userCanvas.configure(bd=0, highlightthickness=0)
    userCanvas.pack()

    compWindow = Toplevel(root)
    compWindow.resizable(width=False, height=False) # prevents resizing window
    Label(compWindow, text = "COMPUTER BOARD - click to make guesses. The computer will guess on your board.").pack()
    compCanvas = Canvas(compWindow, width=w, height=h)
    compCanvas.configure(bd=0, highlightthickness=0)
    compCanvas.pack()

    makeView(data, userCanvas, compCanvas)

    root.bind("<Key>", lambda event : keyEventHandler(data, userCanvas, compCanvas, event))
    compWindow.bind("<Key>", lambda event : keyEventHandler(data, userCanvas, compCanvas, event))
    userCanvas.bind("<Button-1>", lambda event : mouseEventHandler(data, userCanvas, compCanvas, event, "user"))
    compCanvas.bind("<Button-1>", lambda event : mouseEventHandler(data, userCanvas, compCanvas, event, "comp"))

    updateView(data, userCanvas, compCanvas)

    root.mainloop()


### RUN CODE ###

# This code runs the test cases to check your work
if __name__ == "__main__":
    test.testEmptyGrid()
    test.testCreateShip()
    test.testCheckShip()
    test.testAddShips()
    test.testMakeModel()
    test.testDrawGrid()
    test.testIsVertical()
    test.testIsHorizontal()
    test.testGetClickedCell()
    test.testDrawShip()
    test.testShipIsValid()
    test.testUpdateBoard()
    test.testGetComputerGuess()
    test.testIsGameOver()
    test.testDrawGameOver()
    
    ## Finally, run the simulation to test it manually ##
    runSimulation(500, 500)
