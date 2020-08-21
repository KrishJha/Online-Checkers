from tkinter import *
from board import CheckerBoard,Peice
from network import Network
import time
global x
x=0
from _thread import *
def ready(n,root):
    global x
    run = True
    move = ""
    while run:
        time.sleep(1)
        move = n.send("ready")
        if move == "y":
            run = False
        try:
            if not(root.state()=="normal"):
                x=1
                break
        except:
            x=1
            break

    print('found player')
    root.destroy()

def play():
    global x
    n = Network()
    turn=n.getP()
    root=Tk()
    label = Label(root, text='waiting', font=('Courier New', 30))
    label.pack(padx=100,pady=100)
    start_new_thread(ready, (n, root))
    root.mainloop()
    time.sleep(2)
    if x==0:
        game = CheckerBoard(int(turn),n)
        game.mainloop()


play()
