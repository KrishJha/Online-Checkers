from tkinter import *
global e, master

def show():
    global e, master
    l=[]
    s=e.get()
    for i in range(0,11):
        l.append(str(i))
    l.append('.')
    valid=True
    for i in range(len(s)):
        if not(s[i] in l):
            valid=False
    if valid and len(s)!=0:
        handle = open('settings.txt', 'w')
        handle.write(s)
        handle.close()

        handle = open('settings.txt', 'r')
        print(handle.read())
        handle.close()
        master.destroy()
    else:
        e.delete(0, END)
        e.insert(21,'Enter a valid address')


master = Tk()
f = Frame(master)
f.pack()
e = Entry(f,font=('Courier New', 40))
e.pack(padx=10,pady=10)
button = Button(f, command=show,text='Sumbit',font=('Courier New', 30))
button.pack(padx=10,pady=10)
master.mainloop()
