import socket
from time import strftime,gmtime
import tkinter
import tkinter.messagebox
import sys

HOST='127.0.0.1'
PORT = 110
ADDR = (HOST, PORT)

BUF_SIZE = 4096
class pop3client:

    def __init__(self):
        self.s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(ADDR)
        self.top2 = tkinter.Tk()
        self.top2.title("hagai mail")
        self.top2.geometry('400x200')
        tkinter.Label(self.top2,text = "enter your username: ").grid(column=0,row = 0)
        self.username = tkinter.StringVar()
        e1 =tkinter.Entry(self.top2,textvariable=self.username).grid(column=5,row=5)
        b1 =tkinter.Button(self.top2,text = "enter",bd = 4,width = 4, command =self.start1).grid(column=6,row=5)
        self.top2.mainloop()

    def start1(self):#login
        self.s.sendall('USER '+str(self.username.get())+'\r\n')
        Response=self.s.recv(BUF_SIZE)
        if not Response:
            self.top2.destroy()
            return
        if Response[:3]!='+OK':
            tkinter.messagebox.showerror("error","ERROR1:" + Response)
            print('ERROR 1: '+Response)
            self.top2.destroy()
            return
        else:
            self.top2.destroy()
            self.top3 = tkinter.Tk()
            self.top3.title("hagai mail")
            self.top3.geometry('400x200')
            tkinter.Label(self.top3,text = "enter your password: ").grid(column=0,row = 0)
            self.password = tkinter.StringVar()
            e2 =tkinter.Entry(self.top3,textvariable=self.password).grid(column=5,row=5)
            c1 =tkinter.Button(self.top3,text = "enter",bd = 4,width = 4, command =self.start2).grid(column=6,row=5)
            self.top3.mainloop()
    def start2(self):#login password
        self.s.sendall('PASS '+str(self.password.get())+'\r\n')
        Response=self.s.recv(BUF_SIZE)
        if not Response:
            self.top3.destroy()
            return
        if Response[:3]!='+OK':
            tkinter.messagebox.showerror("error","ERROR2:" + Response)
            print('ERROR 2: '+Response)
            self.top3.destroy()
            return
        else:
            self.top3.destroy()
            self.menu1()
        
    def menu1(self):
        self.top4 = tkinter.Tk()
        self.top4.title("hagai mail")
        self.top4.geometry('300x300')
        c2 =tkinter.Button(self.top4,text = "status",bd = 5,width = 20, command = self.stats1).grid(column=18,row=3)
        c3 =tkinter.Button(self.top4,text = "list of mails",bd = 5,width = 20, command = self.list1).grid(column=18,row=4)
        c4 =tkinter.Button(self.top4,text = "read mail",bd = 5,width = 20, command = self.read1).grid(column=18,row=5)
        c5 =tkinter.Button(self.top4,text = "delete mail",bd = 5,width = 20, command = self.delete1).grid(column=18,row=6)
        c6 =tkinter.Button(self.top4,text = "quit",bd = 5,width = 20, command = self.quit1).grid(column=18,row=7)

    def stats1(self):
        self.top4.destroy()
        self.s.sendall('STAT\r\n')
        Response=self.s.recv(BUF_SIZE)
        if not Response:
            print("no connection")
            self.menu1()
        if Response[:3]!='+OK':
            print('ERROR 4: '+Response)
            tkinter.messagebox.showerror("error","ERROR4:" + Response)
            self.menu1()    
        else:
            print(Response)
            self.top5 = tkinter.Tk()
            self.top5.title("hagai mail")
            self.top5.geometry('400x400')
            tkinter.Label(self.top5,text = ""+ Response).grid(column=0,row = 0)
            d1 =tkinter.Button(self.top5,text = "ok",bd = 5,width = 20, command = self.destroy5).grid(column=18,row=7)
            

    def destroy5(self):
        self.top5.destroy()
        self.menu1()
        
    def list1(self):
        self.top4.destroy()
        self.s.sendall('LIST\r\n')
        Response=self.s.recv(BUF_SIZE)
        if not Response:
            self.menu1()
        if Response[:3]!='+OK':
            print('ERROR 5: '+Response)
            tkinter.messagebox.showerror("error","ERROR5:" + Response)
            self.menu1()
        else:
            print(Response)
            self.top5 = tkinter.Tk()
            self.top5.title("hagai mail")
            self.top5.geometry('400x400')
            tkinter.Label(self.top5,text = ""+Response).grid(column=0,row = 0)
            d2 =tkinter.Button(self.top5,text = "ok",bd = 5,width = 20, command = self.destroy5).grid(column=18,row=7)

    def read1(self):
        self.top4.destroy()
        self.top5 = tkinter.Tk()
        self.top5.title("hagai mail")
        self.top5.geometry('600x600')
        tkinter.Label(self.top5,text = "please enter the number of the email:").grid(column=0,row = 0)
        self.num = tkinter.StringVar()
        e3 =tkinter.Entry(self.top5,textvariable=self.num).grid(column=5,row=5)
        d3 =tkinter.Button(self.top5,text = "ok",bd = 5,width = 20, command = self.read2).grid(column=18,row=7)
        d7 =tkinter.Button(self.top5,text = "back",bd = 5,width = 20, command = self.destroy5).grid(column=18,row=9)

    def read2(self):
        self.s.sendall('RETR '+str(self.num.get())+'\r\n')
        
        Response=self.s.recv(BUF_SIZE)
        if not Response:
            self.menu1()
        if Response[:3]!='+OK':
            print('ERROR 6: '+Response)
            tkinter.messagebox.showerror("error","ERROR6:" + Response)
            self.destroy5()
        else:
            self.top5.destroy()
            self.top5 = tkinter.Tk()
            self.top5.title("hagai mail")
            self.top5.geometry('600x600')
            tkinter.Label(self.top5,text = ""+ Response).grid(column=0,row = 0)
            d4 =tkinter.Button(self.top5,text = "ok",bd = 5,width = 20, command = self.destroy5).grid(column=18,row=7)
 
    def delete1(self):
        self.top4.destroy()
        self.top5 = tkinter.Tk()
        self.top5.title("hagai mail")
        self.top5.geometry('600x600')
        tkinter.Label(self.top5,text = "please enter the number of the email:").grid(column=0,row = 0)
        self.num2 = tkinter.StringVar()
        e5 =tkinter.Entry(self.top5,textvariable=self.num2).grid(column=3,row=3)
        d5 =tkinter.Button(self.top5,text = "ok",bd = 5,width = 20, command = self.delete2).grid(column=18,row=7)
        d6 =tkinter.Button(self.top5,text = "back",bd = 5,width = 20, command = self.destroy5).grid(column=18,row=9)
    def delete2(self):
        nummail = self.num2.get()
        print("nummail:" + nummail)
         
        self.s.sendall('DELE '+ nummail +'\r\n')
        Response=self.s.recv(BUF_SIZE)
        if not Response:
            self.menu()            
        if Response[:3]!='+OK':
            print('ERROR 7: '+Response)
            tkinter.messagebox.showerror("error","ERROR7:" + Response)
            self.destroy5()
        else:
            self.top5.destroy()
            self.top5 = tkinter.Tk()
            self.top5.title("hagai mail")
            self.top5.geometry('600x600')
            tkinter.Label(self.top5,text = ""+ Response).grid(column=0,row = 0)
            z1 =tkinter.Button(self.top5,text = "ok",bd = 5,width = 20, command = self.destroy5).grid(column=18,row=7)

    def quit1(self):
        self.s.sendall('QUIT\r\n')
        Response=self.s.recv(BUF_SIZE)
        self.top4.destroy()
        self.s.close()
        return


if __name__ == '__main__':
    audi = pop3client()








         
