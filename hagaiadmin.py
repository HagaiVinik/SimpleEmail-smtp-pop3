import ast #to convert string to dictionary
import os
import sys
import tkinter
import shutil


class admin:
    def __init__(self):
        self.getDBfromfile()
        self.top1 = tkinter.Tk()
        self.top1.title("hagai mail")
        self.top1.geometry('450x350')
        tkinter.Label(self.top1,text = "hello admin! please choose an option: ").grid(column=0,row = 0)
        tkinter.Label(self.top1,text = "").grid(column=5,row = 10)
        tkinter.Label(self.top1,text = "").grid(column=5,row = 11)
        self.c2 = tkinter.Button(self.top1,text = "add new user",bd = 5,width = 20,command = self.add1).grid(column=5,row=5)
        self.c3 = tkinter.Button(self.top1,text = "remove user",bd = 5,width = 20,command = self.removeuser1).grid(column=5,row=6)
        self.c4 = tkinter.Button(self.top1,text = "get password for user",bd = 5,width = 20,command = self.getpassword1).grid(column=5,row=7)
        self.c5 = tkinter.Button(self.top1,text = "see all users ",bd = 5,width = 20,command = self.printallusers1).grid(column=5,row=8)
        self.c6 = tkinter.Button(self.top1,text = "exit",bd = 5,width = 20,command = self.exit1).grid(column=5,row=9)
        self.c1 = tkinter.Button(self.top1,text = "delete all dictionary",bd = 5,width = 20,command = self.delete1).grid(column=5,row=12)
        self.top1.mainloop()
        



        
    def delete1(self):
        self.top1.destroy()
        self.top2 = tkinter.Tk()
        self.top2.title("hagai mail")
        self.top2.geometry('550x300')
        tkinter.Label(self.top2,text = "are you sure? this act will delete all users and mails in the system!").grid(column=0,row = 0)
        n1 = tkinter.Button(self.top2,text = "yes",bd = 5,width = 20,command = self.delete2).grid(column=8,row=1)
        n101 = tkinter.Button(self.top2,text = "no, go back",bd = 5,width = 20,command = self.destroy2).grid(column=8,row=2)
        self.top2.mainloop()

    def delete2(self):
        self.top2.destroy()
        
        self.d={}
        self.saveDBtoFile()
        self.deletemails()

        self.top2 = tkinter.Tk()
        self.top2.title("hagai mail")
        self.top2.geometry('400x400')
        tkinter.Label(self.top2,text = "all users and mails deleted").grid(column=0,row = 0)
        n1 = tkinter.Button(self.top2,text = "ok",bd = 5,width = 20,command = self.destroy2).grid(column=8,row=8)
        self.top2.mainloop()


    def add1(self):
        self.top1.destroy()
        self.top2 = tkinter.Tk()
        self.top2.title("hagai mail")
        self.top2.geometry('400x400')
        tkinter.Label(self.top2,text = "enter the details: ").grid(column=0,row = 0)
        tkinter.Label(self.top2,text = "username: ").grid(column=0,row = 1)
        tkinter.Label(self.top2,text = "password: ").grid(column=0,row = 2)
        self.username = tkinter.StringVar()
        self.password = tkinter.StringVar()
        e2 =tkinter.Entry(self.top2,textvariable=self.username,width = 20).grid(column=2,row=1)
        e3 =tkinter.Entry(self.top2,textvariable=self.password,width = 20).grid(column=2,row=2)
        r2 =tkinter.Button(self.top2,text = "enter",bd = 3,width = 10, command = self.add2).grid(column=8,row=8)
        r2 =tkinter.Button(self.top2,text = "back",bd = 3,width = 10, command = self.destroy2).grid(column=8,row=9)
        self.top2.mainloop()

    def add2(self):
            
        self.d[str(self.username.get())]=str(self.password.get())
        self.saveDBtoFile()

        self.top2.destroy()
        self.top2 = tkinter.Tk()
        self.top2.title("hagai mail")
        self.top2.geometry('400x400')
        tkinter.Label(self.top2,text = "user added.").grid(column=0,row = 0)
        n1 = tkinter.Button(self.top2,text = "ok",bd = 5,width = 20,command = self.destroy2).grid(column=8,row=8)
        self.top2.mainloop()


    def removeuser1(self):
        self.top1.destroy()
        self.top2 = tkinter.Tk()
        self.top2.title("hagai mail")
        self.top2.geometry('500x500')
        self.username3 = tkinter.StringVar()
        tkinter.Label(self.top2,text = "enter username: ").grid(column=0,row = 0)
        e10 =tkinter.Entry(self.top2,textvariable=self.username3,width = 40).grid(column=2,row=1)
        r10 =tkinter.Button(self.top2,text = "enter",bd = 3,width = 5, command = self.removeuser2).grid(column=3,row=3)
        r11 =tkinter.Button(self.top2,text = "back",bd = 3,width = 5, command = self.destroy2).grid(column=3,row=4) 

    def removeuser2(self):
        x = str(self.username3.get())
        self.top2.destroy()
        
        if x in self.d:
            self.d.pop(x)
            self.saveDBtoFile()
        else:
            self.top2 = tkinter.Tk()
            self.top2.title("hagai mail")
            self.top2.geometry('400x400')
            tkinter.Label(self.top2,text = "user not found.").grid(column=0,row = 0)
            n1 = tkinter.Button(self.top2,text = "ok",bd = 5,width = 20,command = self.destroy2).grid(column=8,row=8)
            self.top2.mainloop()
                    
        self.top2 = tkinter.Tk()
        self.top2.title("hagai mail")
        self.top2.geometry('400x400')
        tkinter.Label(self.top2,text = "user removed.").grid(column=0,row = 0)
        n1 = tkinter.Button(self.top2,text = "ok",bd = 5,width = 20,command = self.destroy2).grid(column=8,row=8)
        self.top2.mainloop()


    def getpassword1(self):
        self.top1.destroy()
        
        self.top2 = tkinter.Tk()
        self.top2.title("hagai mail")
        self.top2.geometry('500x500')
        self.username2 = tkinter.StringVar()
        tkinter.Label(self.top2,text = "enter username: ").grid(column=0,row = 0)
        e7 =tkinter.Entry(self.top2,textvariable=self.username2,width = 40).grid(column=2,row=1)
        r7 =tkinter.Button(self.top2,text = "enter",bd = 3,width = 5, command = self.getpassword2).grid(column=3,row=3)
        r8 =tkinter.Button(self.top2,text = "back",bd = 3,width = 5, command = self.destroy2).grid(column=3,row=4)
    def getpassword2(self):
        user2 = str(self.username2.get())
        self.top2.destroy()
        if user2 in self.d:
            self.top2 = tkinter.Tk()
            self.top2.title("hagai mail")
            self.top2.geometry('400x400')
            tkinter.Label(self.top2,text = "password is: "+self.d[user2]).grid(column=0,row = 0)
            n1 = tkinter.Button(self.top2,text = "ok",bd = 5,width = 20,command = self.destroy2).grid(column=8,row=8)
            self.top2.mainloop()
        
        else:
            self.top2 = tkinter.Tk()
            self.top2.title("hagai mail")
            self.top2.geometry('400x400')
            tkinter.Label(self.top2,text = "user not found.").grid(column=0,row = 0)
            n1 = tkinter.Button(self.top2,text = "ok",bd = 5,width = 20,command = self.destroy2).grid(column=8,row=8)
            self.top2.mainloop()
        


    def printallusers1(self):
        print(list(self.d.items()))
        self.top1.destroy()
        self.top2 = tkinter.Tk()
        self.top2.title("hagai mail")
        self.top2.geometry('450x450')
        tkinter.Label(self.top2,text = ""+str(list(self.d.items()))).grid(column=0,row = 0)
        tkinter.Label(self.top2,text = "").grid(column=1,row = 1)
        n1 = tkinter.Button(self.top2,text = "ok",bd = 5,width = 15,command = self.destroy2).grid(column=5,row=5)
            
        self.top2.mainloop()






    def getDBfromfile(self):
        if os.path.exists('users&passwords.txt'):
            f=open('users&passwords.txt','rb')
            self.d=ast.literal_eval(f.read())

        else:
            self.d={}


        

    def saveDBtoFile(self):
        f=open('users&passwords.txt','wb')
        f.write(str(self.d))


    def exit1(self):
        self.top1.destroy()
        sys.exit()



    def destroy2(self):
        self.top2.destroy()
        admin()


    def deletemails(self):
        if os.path.exists('hagaimails'):
            shutil.rmtree('D:\hagaimails')
            

if __name__ == '__main__':
    mercedes = admin()


            
