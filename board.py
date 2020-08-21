from tkinter import *
from tkinter import messagebox
import time
from _thread import *
def make_move(list):
    strlist=str(list[0][0])+' '+str(list[0][1])+' '+str(list[1][0])+' '+str(list[1][1])
    return strlist

def read_move(list):
    [num1,num2,num3,num4]=list.split()
    return [[int(num1),int(num2)],[int(num3),int(num4)]]

class CheckerBoard(Frame):
    '''makes checkerboard fame that has all the overall atributes'''

    def __init__(self,turn,net):
        master= Tk()
        Frame.__init__(self, master)
        self.turn = 0
        self.playablet=turn
        self.grid()
        self.net=net
        self.squares = []
        self.white = []
        self.red = []
        self.clicklist = []
        for row in range(0, 8):
            self.squares.append([])
            for column in range(0, 8):
                peice = None
                if (row + column) % 2 == 0:
                    color = 'blanched almond'
                else:
                    color = 'dark green'
                    if row < 3:
                        self.red.append(Peice('red', row, column, color))
                        peice = self.red[len(self.white) - 1]
                    if row > 4:
                        self.white.append(Peice('white', row, column, color))
                        peice = self.white[len(self.white) - 1]

                self.squares[row].append(Tile(self, row, column, color, self, peice))
                self.squares[row][column].grid(row=row, column=column, padx=0, pady=0)

        self.turnLabel = Label(self, text='Turn:', font=('Courier New', 18))
        self.turnLabel.grid(row=10, column=3)
        self.turnsquare = Tile(self, 10, 4, 'white', self, None)
        self.turnsquare.grid(row=10, column=4)
        self.aLabel = Label(self, text='You are:', font=('Courier New', 18))
        self.aLabel.grid(row=11, column=2,columnspan=2)
        colors = ['white', 'red']
        self.asquare = Tile(self, 11, 4,"white", self, None)
        self.asquare.grid(row=11, column=4)
        self.asquare.create_oval(10, 10, 60, 60, fill=colors[turn])
        self.turnsquare.create_oval(10, 10, 60, 60, fill='white')
        self.asquare.unbind('<Button-1>')
        self.turnsquare.unbind('<Button-1>')
        self.redLabel = Label(self, text='12', font=('Courier New', 18))
        self.redLabel.grid(row=10, column=1)
        self.redsquare = Tile(self, 10, 0, 'white', self, None)
        self.redsquare.create_oval(10, 10, 60, 60, fill='red')
        self.redsquare.grid(row=10, column=0)
        self.whiteLabel = Label(self, text='12', font=('Courier New', 18))
        self.whiteLabel.grid(row=10, column=6)
        self.whitesquare = Tile(self, 10, 7, 'white', self, None)
        self.whitesquare.create_oval(10, 10, 60, 60, fill='white')
        self.whitesquare.grid(row=10, column=7)
        for i in range(len(self.white)):
            peice = self.white[i]
            peice.set_board(self, 'white')

        for i in range(len(self.red)):
            peice = self.red[i]
            peice.set_board(self, 'red')
        if self.playablet==1:
            start_new_thread(self.waiting,())
    def bindall(self):
        for x in range(8):
            for y in range(8):
                self.squares[x][y].bindu()

    def unbindall(self):
        for x in range(8):
            for y in range(8):
                self.squares[x][y].unbind('<Button-1>')

    def waiting(self):
        self.unbindall()
        run=True
        move=""
        while run:
            time.sleep(1)
            move=self.net.send("GET")
            if move!="waiting":
                run=False
            if move=="left":
                print("Your opponnent disconnected")
                self.master.destroy()
                break
        self.clicklist=read_move(move)
        self.squares[0][0].click2()
        self.bindall()


class Tile(Canvas):
    "represents a square"

    def __init__(self, master, x, y, color, board, peice):
        self.board = board
        self.x = x
        self.y = y
        self.peice = peice
        Canvas.__init__(self, master, width=60, height=60, bg=color,
                        relief=FLAT, borderwidth=5)
        self.bind('<Button-1>', self.click)  # when clicked go to selef.click

    def bindu(self):
        self.bind('<Button-1>', self.click)

    def click2(self):
        colors = ['white', 'red']
        y=self.board.clicklist[1][1]
        x=self.board.clicklist[1][0]
        self.board.squares[self.board.clicklist[0][0]][self.board.clicklist[0][1]].peice.move(y, x)
        legal = True
        if legal:
            self.board.turnsquare.create_oval(10, 10, 60, 60, fill=colors[(self.board.turn + 1) % 2])
            self.board.turn = (self.board.turn + 1) % 2
        self.board.clicklist = []


    def click(self, event):
        (self.board.clicklist).append([self.x, self.y])
        # print(self.y,self.x)
        colors = ['white', 'red']
        self['relief'] = SOLID
        self.board.turnsquare.create_oval(10, 10, 60, 60, fill=colors[self.board.turn])
        if len(self.board.clicklist) > 1:
            legal = False
            for i in range(len(self.board.clicklist)):
                squarec = (self.board.clicklist[i])
                x = squarec[0]
                y = squarec[1]
                (self.board.squares[x][y])['relief'] = FLAT

            if self.board.squares[self.board.clicklist[0][0]][self.board.clicklist[0][1]].peice != None:
                if self.board.squares[self.board.clicklist[0][0]][self.board.clicklist[0][1]].peice.color == colors[self.board.turn]:
                    places = self.board.squares[self.board.clicklist[0][0]][self.board.clicklist[0][1]].peice.can_move()
                    if self.board.clicklist[1] in places:
                        self.board.squares[self.board.clicklist[0][0]][self.board.clicklist[0][1]].peice.move(y, x)
                        legal = True
            if legal:
                self.board.turnsquare.create_oval(10, 10, 60, 60, fill=colors[(self.board.turn + 1) % 2])
                self.board.turn = (self.board.turn + 1) % 2
                rep=self.board.net.send(make_move(self.board.clicklist))
                if rep!="recieved":
                    if rep!="left":
                        print("lost connection to server, please check your internet connection")
                    else:
                        print("Your opponnent disconnected")
                    self.board.unbindall()
                    self.board.master.destroy()
                else:
                    self.board.clicklist = []
                    start_new_thread(self.board.waiting,())
            self.board.clicklist = []


class Peice:
    def __init__(self, color, row, column, sq):
        self.c = column  # the column
        self.r = row  # the row
        self.isking = False

    def set_board(self, board, color):
        self.board = board
        row = self.r
        column = self.c
        self.color = color
        canvas = board.squares[row][column]
        if canvas['bg'] == 'dark green':
            self.color = color
            self.p = canvas.create_oval(10, 10, 60, 60, fill=color)

    def can_move(self):
        move = []
        row = self.r
        colum = self.c
        color = self.color
        if color == 'white' or self.isking == True:
            if colum - 2 > -1 and row - 2 > -1:
                if self.board.squares[row - 2][colum - 2].peice == None and self.board.squares[row - 1][
                    colum - 1].peice != None:
                    if self.board.squares[row - 1][colum - 1].peice.color != self.color:
                        move.append([row - 2, colum - 2])
            if colum + 2 < 8 and row - 2 > -1:
                if self.board.squares[row - 2][colum + 2].peice == None and self.board.squares[row - 1][
                    colum + 1].peice != None:
                    if self.board.squares[row - 1][colum + 1].peice.color != self.color:
                        move.append([row - 2, colum + 2])
        if color == 'red' or self.isking == True:
            if colum - 2 > -1 and row + 2 < 8:
                if self.board.squares[row + 2][colum - 2].peice == None and self.board.squares[row + 1][
                    colum - 1].peice != None:
                    if self.board.squares[row + 1][colum - 1].peice.color != self.color:
                        move.append([row + 2, colum - 2])
            if colum + 2 < 8 and row + 2 < 8:
                if self.board.squares[row + 2][colum + 2].peice == None and self.board.squares[row + 1][colum + 1].peice != None:
                    if self.board.squares[row + 1][colum + 1].peice.color != self.color:
                        move.append([row + 2, colum + 2])

        if (color == 'white' or self.isking == True):
            if colum - 1 > -1 and row - 1 > -1:
                if self.board.squares[row - 1][colum - 1].peice == None:
                    move.append([row - 1, colum - 1])

            if colum + 1 < 8 and row - 1 > -1:
                if self.board.squares[row - 1][colum + 1].peice == None:
                    move.append([row - 1, colum + 1])

        if (color == 'red' or self.isking == True):
            if colum - 1 > -1 and row + 1 < 8:
                if self.board.squares[row + 1][colum - 1].peice == None:
                    move.append([row + 1, colum - 1])

            if colum + 1 < 8 and row + 1 < 8:
                if self.board.squares[row + 1][colum + 1].peice == None:
                    move.append([row + 1, colum + 1])
        return move

    def move(self, rn, cn):
        # rn and cn stand for row cand column new places
        self.board.squares[self.r][self.c].peice = None
        self.board.squares[cn][rn].peice = None
        dele = self.board.squares[self.r][self.c].find_all()
        for i in dele:
            self.board.squares[self.r][self.c].delete(i)
        cd = rn - self.c
        rd = cn - self.r
        if cd % 2 == 0 and rd % 2 == 0:
            self.board.squares[int(self.r + rd/2)][int(self.c + cd/2)].peice.destroy()
        self.r = cn
        self.c = rn
        self.p = self.board.squares[cn][rn].create_oval(10, 10, 60, 60, fill=self.color)
        self.board.squares[cn][rn].peice = self
        if self.r == 7 and self.color == 'red':
            self.isking = True
        if self.r == 0 and self.color == 'white':
            self.isking = True
        if self.isking == True:
            self.board.squares[cn][rn].create_text(35, 40, fill="black", font='Times 20 italic',
                                                   text="*")

    def destroy(self):
        if self.color == 'white':
            self.board.squares[self.r][self.c].peice = None
            self.board.white.remove(self)
            dele = self.board.squares[self.r][self.c].find_all()
            for i in dele:
                self.board.squares[self.r][self.c].delete(i)
            self.board.whiteLabel['text'] = str(len(self.board.white))
        else:
            self.board.squares[self.r][self.c].peice = None
            self.board.red.remove(self)
            dele = self.board.squares[self.r][self.c].find_all()
            for i in dele:
                self.board.squares[self.r][self.c].delete(i)
            self.board.redLabel['text'] = str(len(self.board.red))
        if len(self.board.red) == 0:
            self.board.unbindall()
            messagebox.showinfo('Chechers', 'Congratulations -- white won!', parent=self.board.master)
            self.board.master.destroy()
        if len(self.board.white) == 0:
            self.board.unbindall()
            messagebox.showinfo('Chechers', 'Congratulations -- red won!', parent=self.board.master)
            self.board.master.destroy()
