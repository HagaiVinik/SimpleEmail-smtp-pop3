import socket
from time import strftime,gmtime
import tkinter
import tkinter.messagebox
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
        print("starting smtp client")

        self.s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(ADDR)
        res = self.s.recv(BUF_SIZE).decode()
        if res[:3]!='220':
            tkinter.messagebox.showerror("error","ERROR:" + res)
            print('ERROR 1: '+res)
            return
        self.top = tkinter.Tk()
        self.top.title("hagai mail")
        self.top.geometry('450x450')
        tkinter.Label(self.top,text = "a new mail ? (yes/no) : ").grid(column=0,row = 0)
        b =tkinter.Button(self.top, text = "yes", bd = 4, width = 8, command =self.start_msg).grid(column=5, row=5)
        c =tkinter.Button(self.top, text = "no", bd = 4, width = 8, command = self.close_prog).grid(column=6, row=5)
        self.top.mainloop()

    def start_msg (self):
        ehlo_proto_msg = 'EHLO smtp.gmx.com\r\n'.encode()
        self.s.send(ehlo_proto_msg)

        res = self.s.recv(BUF_SIZE).decode()
        if res[:3]!='250':
            tkinter.messagebox.showerror("error","ERROR 2:" + res)
            print('ERROR 2: '+res)
            return

        mail_from_proto_msg = ('MAIL FROM:<'+USERNAME+'>\r\n').encode()
        self.s.send(mail_from_proto_msg)

        res=self.s.recv(BUF_SIZE).decode()
        if res[:3]!='250':
            tkinter.messagebox.showerror("error","ERROR 4:" + res)
            print('ERROR 4: '+res)
            return
        self.domain()
    
    def close_prog (self):
        self.s.close()
        self.top.destroy()

    def start5 (self):
        print(self.name1.get())
        self.top4.destroy()
        print(1)
        self.s.sendall('From:<'+USERNAME+'>\r\nsubject: '+str(self.subject1.get())+'\r\n\r\n'+str(self.bodymail1.get())+'\r\n.\r\n')
        Response=self.s.recv(BUF_SIZE)
        if Response[:3]!='250':
            tkinter.messagebox.showerror("error","ERROR 7:" + Response) 
            print('ERROR 7: '+Response)
            return
        self.s.send('QUIT\r\n')
        Response=self.s.recv(BUF_SIZE)
        print(Response)
        if Response[:3]!='221':
            tkinter.messagebox.showerror("error","ERROR 8:" + Response)
            print('ERROR 8: '+Response)
            return
        self.s.close()
        smtpclient()
    def start3 (self):
        self.s.send('DATA\r\n')
        Response=self.s.recv(BUF_SIZE)
        if Response[:3]!='354':
            tkinter.messagebox.showerror("error","ERROR 6:" + Response)
            print('ERROR 6: '+Response)
            return
        self.top4 = tkinter.Tk()
        self.top4.title("hagai mail")
        self.top4.geometry('500x500')
        tkinter.Label(self.top4,text = "enter the details: ").grid(column=0,row = 0)
        tkinter.Label(self.top4,text = "subject: ").grid(column=0,row = 1)
        tkinter.Label(self.top4,text = "bodymail: ").grid(column=0,row = 2)
        self.subject1 = tkinter.StringVar()
        self.bodymail1 = tkinter.StringVar()
        e2 =tkinter.Entry(self.top4,textvariable=self.subject1,width = 40).grid(column=2,row=1)
        e3 =tkinter.Entry(self.top4,textvariable=self.bodymail1,width = 40).grid(column=2,row=2)
        c2 =tkinter.Button(self.top4,text = "enter",bd = 3,width = 5, command = self.start5).grid(column=8,row=8)
        self.top4.mainloop()

    def domain2(self):
       
        print('aaa:'+self.name1.get())

        self.s.send('RCPT TO:<'+str(self.name1.get())+'>\r\n')
        Response=self.s.recv(BUF_SIZE)
        if Response[:3]!='250':
            tkinter.messagebox.showerror("error","ERROR5:" + Response)
            print('ERROR 5: '+Response)
            return
        self.top2.destroy()
        self.start3()

    def domain(self):
        self.top.destroy()
        self.top2 = tkinter.Tk()
        self.top2.title("hagai mail")
        self.top2.geometry('500x500')
        tkinter.Label(self.top2,text = "enter the domains adresses:  : ").grid(column=0,row = 0)
        self.name1 = tkinter.StringVar()
        e1 =tkinter.Entry(self.top2,textvariable=self.name1).grid(column=5,row=5)
        c1 =tkinter.Button(self.top2,text = "enter",bd = 4,width = 4, command =self.domain2).grid(column=6,row=5)
        self.top2.mainloop()

if __name__ == '__main__':
    bmw = smtpclient()

    










