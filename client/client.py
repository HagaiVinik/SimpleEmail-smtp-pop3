import tkinter

import hagaismtp
import hagaipop3


class Client:

    def __init__(self):
        print("starting app")

        self.top = tkinter.Tk()

        self.top.title("hagai mail")
        self.top.geometry('500x500')
        tkinter.Label(self.top, text="Welcome to simple smtp/pop3 email").pack()
        tkinter.Label(self.top, text="Created by Hagai Vinik (c) 2023").pack()
        tkinter.Label(self.top, text="").pack()
        tkinter.Label(self.top, text="Please choose: ").pack()
        b1 = tkinter.Button(self.top, text="Sign in", bd=4, width=20, command=self.smtp).pack()
        b2 = tkinter.Button(self.top, text="Sign up", bd=4, width=20, command=self.pop3).pack()
        b3 = tkinter.Button(self.top, text="Exit", bd=4, width=20, command=self.exit_app).pack()

        self.top.mainloop()

    def sign_in(self):
        print("starting smtp client")
        self.top.destroy()
        hagaismtp.smtpclient()


    def sign_up(self):
        print("starting pop3 client")
        self.top.destroy()

        hagaipop3.pop3client()


    def exit_app(self):
        self.top.destroy()


if __name__ == '__main__':
    Client()
