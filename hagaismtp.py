import socket
from time import strftime,gmtime
import Tkinter
import tkMessageBox
import sys

# The address of the server
HOST='127.0.0.1'
PORT = 25
ADDR = (HOST, PORT)
USERNAME='me@127.0.0.1'
PASSWORD='1234'

# recv buffer size
BUF_SIZE = 4096

class smtpclient:

    def __init__(self):
        self.s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(ADDR)
        Response=self.s.recv(BUF_SIZE)
        if Response[:3]!='220':
            tkMessageBox.showerror("error","ERROR:" + Response)
            print 'ERROR 1: '+Response
            return
        self.top = Tkinter.Tk()
        self.top.title("hagai mail")
        self.top.geometry('300x300')
        Tkinter.Label(self.top,text = "a new mail ? (yes/no) : ").grid(column=0,row = 0)
        b =Tkinter.Button(self.top,text = "yes",bd = 4,width = 8, command =self.start1).grid(column=5,row=5)
        c =Tkinter.Button(self.top,text = "no",bd = 4,width = 8, command = self.close1).grid(column=6,row=5)
        self.top.mainloop()

    def start1 (self):
        self.s.send('EHLO smtp.gmx.com\r\n')
        Response=self.s.recv(BUF_SIZE)
        if Response[:3]!='250':
            tkMessageBox.showerror("error","ERROR 2:" + Response)
            print 'ERROR 2: '+Response
            return
        self.s.send('MAIL FROM:<'+USERNAME+'>\r\n')
        Response=self.s.recv(BUF_SIZE)
        if Response[:3]!='250':
            tkMessageBox.showerror("error","ERROR 4:" + Response)
            print 'ERROR 4: '+Response
            return
        self.domain()
    
    def close1 (self):
        self.s.close()
        self.top.destroy()

    def start5 (self):
        print self.name1.get()
        self.top4.destroy()
        print 1
        self.s.sendall('From:<'+USERNAME+'>\r\nsubject: '+str(self.subject1.get())+'\r\n\r\n'+str(self.bodymail1.get())+'\r\n.\r\n')
        Response=self.s.recv(BUF_SIZE)
        if Response[:3]!='250':
            tkMessageBox.showerror("error","ERROR 7:" + Response) 
            print 'ERROR 7: '+Response
            return
        self.s.send('QUIT\r\n')
        Response=self.s.recv(BUF_SIZE)
        print Response
        if Response[:3]!='221':
            tkMessageBox.showerror("error","ERROR 8:" + Response)
            print 'ERROR 8: '+Response
            return
        self.s.close()
        smtpclient()
    def start3 (self):
        self.s.send('DATA\r\n')
        Response=self.s.recv(BUF_SIZE)
        if Response[:3]!='354':
            tkMessageBox.showerror("error","ERROR 6:" + Response)
            print 'ERROR 6: '+Response
            return
        self.top4 = Tkinter.Tk()
        self.top4.title("hagai mail")
        self.top4.geometry('500x500')
        Tkinter.Label(self.top4,text = "enter the details: ").grid(column=0,row = 0)
        Tkinter.Label(self.top4,text = "subject: ").grid(column=0,row = 1)
        Tkinter.Label(self.top4,text = "bodymail: ").grid(column=0,row = 2)
        self.subject1 = Tkinter.StringVar()
        self.bodymail1 = Tkinter.StringVar()
        e2 =Tkinter.Entry(self.top4,textvariable=self.subject1,width = 40).grid(column=2,row=1)
        e3 =Tkinter.Entry(self.top4,textvariable=self.bodymail1,width = 40).grid(column=2,row=2)
        c2 =Tkinter.Button(self.top4,text = "enter",bd = 3,width = 5, command = self.start5).grid(column=8,row=8)
        self.top4.mainloop()

    def domain2(self):
       
        print 'aaa:'+self.name1.get()

        self.s.send('RCPT TO:<'+str(self.name1.get())+'>\r\n')
        Response=self.s.recv(BUF_SIZE)
        if Response[:3]!='250':
            tkMessageBox.showerror("error","ERROR5:" + Response)
            print 'ERROR 5: '+Response
            return
        self.top2.destroy()
        self.start3()
    def domain(self):
        self.top.destroy()
        self.top2 = Tkinter.Tk()
        self.top2.title("hagai mail")
        self.top2.geometry('500x500')
        Tkinter.Label(self.top2,text = "enter the domains adresses:  : ").grid(column=0,row = 0)
        self.name1 = Tkinter.StringVar()
        e1 =Tkinter.Entry(self.top2,textvariable=self.name1).grid(column=5,row=5)
        c1 =Tkinter.Button(self.top2,text = "enter",bd = 4,width = 4, command =self.domain2).grid(column=6,row=5)
        self.top2.mainloop()

if __name__ == '__main__':
    bmw = smtpclient()

    










