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

        self.top = tkinter.Tk()
        self.top.title("hagai mail")
        self.top.geometry('400x200')
        tkinter.Label(self.top, text ="enter your username: ").pack()
        self.username = tkinter.StringVar()
        e1 =tkinter.Entry(self.top, textvariable=self.username).pack()
        b1 =tkinter.Button(self.top, text ="enter", bd = 4, width = 10, command =self.start).pack()
        self.top.mainloop()

    def start(self):#login

        login_msg = 'USER '+str(self.username.get())+'\r\n'
        self.s.sendall(login_msg.encode())

        res = self.s.recv(BUF_SIZE).decode()
        if not res:
            self.top.destroy()
            return

        if res[:3]!='+OK':
            tkinter.messagebox.showerror("error","ERROR1:" + res)
            print('ERROR 1: '+res)
            self.top.destroy()
            return

        else:
            self.top.destroy()
            self.top = tkinter.Tk()
            self.top.title("hagai mail")
            self.top.geometry('400x200')
            tkinter.Label(self.top, text ="enter your password: ").pack()
            self.password = tkinter.StringVar()
            e2 =tkinter.Entry(self.top, textvariable=self.password).pack()
            c1 =tkinter.Button(self.top, text ="enter", bd = 4, width = 10, command =self.login).pack()
            self.top.mainloop()

    def login(self):#login password

        pass_msg = 'PASS '+str(self.password.get())+'\r\n'
        self.s.sendall(pass_msg.encode())

        res = self.s.recv(BUF_SIZE).decode()
        if not res:
            self.top.destroy()
            return

        if res[:3]!='+OK':
            tkinter.messagebox.showerror("error","received malformed message from server." + res)
            print('ERROR 2: '+res)
            self.top.destroy()
            return

        else:
            self.top.destroy()
            self.menu()
        
    def menu(self):
        self.top = tkinter.Tk()
        self.top.title("hagai mail")
        self.top.geometry('300x300')
        tkinter.Label(self.top, text="choose option: ").pack()
        tkinter.Button(self.top, text ="status", bd = 5, width = 20, command = self.show_status).pack()
        tkinter.Button(self.top, text ="list of mails", bd = 5, width = 20, command = self.show_list).pack()
        tkinter.Button(self.top, text ="read mail", bd = 5, width = 20, command = self.read_mail).pack()
        tkinter.Button(self.top, text ="delete mail", bd = 5, width = 20, command = self.delete_mail).pack()
        tkinter.Button(self.top, text ="quit", bd = 5, width = 20, command = self.quit_app).pack()

    def show_status(self):
        self.top.destroy()

        stat_msg = 'STAT\r\n'
        self.s.sendall(stat_msg.encode())

        res = self.s.recv(BUF_SIZE).decode()
        if not res:
            print("no connection")
            self.menu()
        if res[:3]!='+OK':
            print('ERROR 4: '+res)
            tkinter.messagebox.showerror("error","ERROR4:" + res)
            self.menu()
        else:
            print(res)
            self.top = tkinter.Tk()
            self.top.title("hagai mail")
            self.top.geometry('400x400')
            tkinter.Label(self.top, text ="" + res).pack()
            d1 =tkinter.Button(self.top, text ="ok", bd = 5, width = 20, command = self.go_back_menu).pack()
            

    def go_back_menu(self):
        self.top.destroy()
        self.menu()
        
    def show_list(self):
        self.top.destroy()

        list_msg = 'LIST\r\n'
        self.s.sendall(list_msg.encode())

        res = self.s.recv(BUF_SIZE).decode()
        if not res:
            self.menu()
        if res[:3]!='+OK':
            print('ERROR 5: '+res)
            tkinter.messagebox.showerror("error","ERROR5:" + res)
            self.menu()

        else:
            print(res)
            self.top = tkinter.Tk()
            self.top.title("hagai mail")
            self.top.geometry('400x400')
            tkinter.Label(self.top, text ="number:      size:").pack()
            tkinter.Label(self.top, text ="" + res.split(')')[1]).pack()
            tkinter.Button(self.top, text ="ok", bd = 5, width = 20, command = self.go_back_menu).pack()

    def read_mail(self):
        self.top.destroy()
        self.top = tkinter.Tk()
        self.top.title("hagai mail")
        self.top.geometry('600x600')
        tkinter.Label(self.top, text ="please enter the number of the email:").pack()
        self.num = tkinter.StringVar()
        e3 = tkinter.Entry(self.top, textvariable=self.num).pack()
        d3 = tkinter.Button(self.top, text ="ok", bd = 5, width = 20, command = self.show_mail).pack()
        d7 = tkinter.Button(self.top, text ="back", bd = 5, width = 20, command = self.go_back_menu).pack()

    def show_mail(self):
        retr_msg = 'RETR '+str(self.num.get())+'\r\n'
        self.s.sendall(retr_msg.encode())
        
        res = self.s.recv(BUF_SIZE).decode()
        if not res:
            self.menu()
        if res[:3]!='+OK':
            print('ERROR 6: '+res)
            tkinter.messagebox.showerror("error","ERROR6:" + res)
            self.go_back_menu()
        else:
            self.top.destroy()
            self.top = tkinter.Tk()
            self.top.title("hagai mail")
            self.top.geometry('600x600')
            tkinter.Label(self.top, text ="" + res).pack()
            d4 = tkinter.Button(self.top, text ="ok", bd = 5, width = 20, command = self.go_back_menu).pack()
 
    def delete_mail(self):
        self.top.destroy()
        self.top = tkinter.Tk()
        self.top.title("hagai mail")
        self.top.geometry('600x600')
        tkinter.Label(self.top, text ="please enter the number of the email:").pack()
        self.num = tkinter.StringVar()
        e5 = tkinter.Entry(self.top, textvariable=self.num).pack()
        d5 = tkinter.Button(self.top, text ="ok", bd = 5, width = 20, command = self.on_delete).pack()
        d6 = tkinter.Button(self.top, text ="back", bd = 5, width = 20, command = self.go_back_menu).pack()

    def on_delete(self):
        nummail = self.num.get()
        print("nummail:" + nummail)

        dele_msg = 'DELE '+ nummail +'\r\n'
        self.s.sendall(dele_msg.encode())

        res = self.s.recv(BUF_SIZE).decode()
        if not res:
            self.menu()

        if res[:3]!='+OK':
            print('ERROR 7: '+res)
            tkinter.messagebox.showerror("error","ERROR7:" + res)
            self.go_back_menu()
        else:
            self.top.destroy()
            self.top = tkinter.Tk()
            self.top.title("hagai mail")
            self.top.geometry('600x600')
            tkinter.Label(self.top, text ="" + res).pack()
            z1 =tkinter.Button(self.top, text ="ok", bd = 5, width = 20, command = self.go_back_menu).pack()

    def quit_app(self):
        quit_msg = 'QUIT\r\n'
        self.s.sendall(quit_msg.encode())

        res=self.s.recv(BUF_SIZE).decode()
        self.top.destroy()
        self.s.close()
        return


if __name__ == '__main__':
    pop3client()








         
