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
        self.s = None

        try:
            self.s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect(ADDR)
        except:
            tkinter.messagebox.showerror("Error", "Couldn't connect to server")
            exit()

        res = self.s.recv(BUF_SIZE).decode()
        if res[:3]!='220':
            tkinter.messagebox.showerror("error","ERROR:" + res)
            print('ERROR 1: '+res)
            return

        self.top = tkinter.Tk()
        self.top.title("hagai mail")
        self.top.geometry('450x450')
        tkinter.Label(self.top,text = "a new mail ? (yes/no) : ").pack()
        b =tkinter.Button(self.top, text = "yes", bd = 4, width = 8, command =self.get_username).pack()
        c =tkinter.Button(self.top, text = "no", bd = 4, width = 8, command = self.close_prog).pack()
        self.top.mainloop()

    def get_username(self):
        self.top.destroy()

        self.top = tkinter.Tk()
        self.top.title("hagai mail")
        self.top.geometry('450x450')
        tkinter.Label(self.top, text="enter your name: ").pack()
        self.username = tkinter.StringVar()
        e1 = tkinter.Entry(self.top, textvariable=self.username).pack()
        b = tkinter.Button(self.top, text="OK", bd=4, width=8, command=self.start_msg).pack()

        self.top.mainloop()

    def start_msg(self):

        global USERNAME
        USERNAME = str(self.username.get()) + '@127.0.0.1'

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

        self.enter_domain()
    
    def close_prog (self):
        self.s.close()
        self.top.destroy()

    def on_send (self):
        print(self.name.get())
        self.top.destroy()

        msg = 'From:<'+USERNAME+'>\r\nsubject: '+str(self.subject1.get())+'\r\n\r\n'+str(self.bodymail1.get())+'\r\n.\r\n'
        self.s.sendall(msg.encode())

        try:
            response = self.s.recv(BUF_SIZE).decode()
            if response[:3]!='250':
                tkinter.messagebox.showerror("error","error in receiving response from server after sending email.")
                print('ERROR 7: '+response)
                return

            quit_msg = 'QUIT\r\n'.encode()

            self.s.send(quit_msg)
            response = self.s.recv(BUF_SIZE).decode()

            print(response)

            if response[:3]!='221':
                tkinter.messagebox.showerror("error","Error received from server after sending QUIT message.")
                print('ERROR 8: '+response)
                return

        except:
            tkinter.messagebox.showerror("error", "received incorrect response from server")

        self.s.close()

        smtpclient()

    def send_data(self):
        data_msg = 'DATA\r\n'.encode()
        self.s.send(data_msg)

        response=self.s.recv(BUF_SIZE).decode()

        if response[:3]!='354':
            tkinter.messagebox.showerror("error","ERROR 6:" + response)
            print('ERROR 6: '+response)
            return

        self.top = tkinter.Tk()
        self.top.title("hagai mail")
        self.top.geometry('500x500')
        tkinter.Label(self.top, text ="enter the details: ").pack()
        tkinter.Label(self.top, text ="subject: ").pack()
        tkinter.Label(self.top, text ="bodymail: ").pack()
        self.subject1 = tkinter.StringVar()
        self.bodymail1 = tkinter.StringVar()
        e2 =tkinter.Entry(self.top, textvariable=self.subject1, width = 40).pack()
        e3 =tkinter.Entry(self.top, textvariable=self.bodymail1, width = 40).pack()
        c2 =tkinter.Button(self.top, text ="enter", bd = 3, width = 5, command = self.on_send).pack()
        self.top.mainloop()

    def sendto_domain(self):
       
        print('name:' + self.name.get())
        rcpt_msg = 'RCPT TO:<' + str(self.name.get()) + '>\r\n'
        self.s.send(rcpt_msg.encode())

        Response=self.s.recv(BUF_SIZE).decode()

        if Response[:3]!='250':
            tkinter.messagebox.showerror("error","ERROR5:" + Response)
            print('ERROR 5: '+Response)
            return

        self.top2.destroy()
        self.send_data()

    def enter_domain(self):
        self.top.destroy()
        self.top2 = tkinter.Tk()
        self.top2.title("hagai mail")
        self.top2.geometry('500x500')
        tkinter.Label(self.top2,text = "enter the domains adresses:  : ").pack()
        self.name = tkinter.StringVar()
        e1 =tkinter.Entry(self.top2, textvariable=self.name).pack()
        c1 =tkinter.Button(self.top2, text = "enter", bd = 4, width = 4, command =self.sendto_domain).pack()
        self.top2.mainloop()

if __name__ == '__main__':
    bmw = smtpclient()

    










