import socket
import os
import ast #to convert string to dictionary
import threading
from threading import Thread


HOST = '127.0.0.1'
PORT_SMTP = 25
PORT_POP3 = 110
ADDR_SMTP = (HOST, PORT_SMTP)
ADDR_POP3 = (HOST, PORT_POP3)
SERVERNAME='SN'
BUF_SIZE = 4096
USERS_PASSWORDS_FILE= r'../users&passwords.txt'


class ServerSMTP_and_POP3:
    def __init__(self):
        self.running = True

        Thread(target = self.main_smtp).start()
        Thread(target = self.main_pop3).start()

    # ---------------------main-------------------------------------

    def main_smtp(self):
        s_smtp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_smtp.bind(ADDR_SMTP)
        s_smtp.listen(5)
        print('Server is Running @', ADDR_SMTP)
        while self.running:
            conn, addr = s_smtp.accept()
            Thread(target=self.handle_smtp_client, args=(conn, addr)).start()

        s_smtp.close()

    def main_pop3(self):
        s_pop3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_pop3.bind(ADDR_POP3)
        s_pop3.listen(5)
        print('Server is Running @', ADDR_POP3)
        while self.running:
            conn, addr = s_pop3.accept()
            Thread(target=self.handle_pop3_client, args=(conn, addr)).start()

        s_pop3.close()

    #--------------------smtp server functions---------------------

    def handle_smtp_client(self, conn, addr):
        Domains = []

        # wait for connection for the client
        msg_to_all = '220 '+SERVERNAME+' ESMTP Postfix'
        conn.sendall(msg_to_all.encode())
        request = conn.recv(BUF_SIZE)
        request = request.decode()

        if not request:
            conn.close()
            return
        if request.split()[0]!='HELO' and request.split()[0]!='EHLO':
            conn.close()
            return
        conn.sendall('250 Hello '+request.split()[1]+' , I am glad to meet you')
        request = conn.recv(BUF_SIZE)
        if not request:
            conn.close()
            return
        if request[:9]!='MAIL FROM':
            conn.close()
            return
        UserSender=request[10:-1]
        conn.sendall('250 Hello '+request.split()[1]+' , I am glad to meet you')
        request = conn.recv(BUF_SIZE)
        if not request:
            conn.close()
            return

        if request[:9]=='RCPT TO:<':
            Domains=(request[9:-3]).split(',')
            print('domains:',Domains)
            conn.sendall('250 OK')
            request = conn.recv(BUF_SIZE)
            if not request:
                conn.close()
                return
        if request[:4]!='DATA':
            conn.close()
            return
        conn.sendall('354 End data with <CR><LF>.<CR><LF>')                
        DATA = conn.recv(BUF_SIZE)
        if not DATA:
            conn.close()
            return
        BodyMail=UserSender+DATA
        while DATA[-5:] !='\r\n.\r\n':
            DATA = conn.recv(BUF_SIZE)
            if not DATA:
                conn.close()
                return
            BodyMail+=DATA
        print('-----The all mail: -----')
        print(BodyMail)
        print('------------------------')
        self.SaveMailInDominsBoxes(BodyMail, Domains)
        conn.sendall('250 Ok')
        request = conn.recv(BUF_SIZE)
        if not request:
            conn.close()
            return
        if request[:4]!='QUIT':
            conn.close()
            return
        conn.sendall('221 Bye')
        # close the connection to the specific client
        conn.close()

    def handle_pop3_client(self, conn, addr):
        # wait for connection for the client

        x = conn.recv(BUF_SIZE) #wait for client send username
        if not x:
            conn.close()
            return
        if x[:5]!='USER ':
            conn.sendall('data did not recieve correctly')
            conn.close()
            return
        if len(x)<6:
            conn.sendall('did not get the username')
            conn.close()
            return
        if x[:5]=='USER ' and len(x)>5:
            username=x[5:-2]
            print(username+' try get in')
            text,IsFound = self.find_user_in_DB(username)
            conn.sendall(text+'\r\n')
            if not IsFound:
                print(text)
                return
        x = conn.recv(BUF_SIZE) #wait for client send password
        if not x:
            conn.close()
            return
        if x[:5]!='PASS ':
            conn.sendall('-ERR data did not recieve correctly')
            conn.close()
            return
        if len(x)<6:
            conn.sendall('-ERR did not get the password')
            conn.close()
            return
        if x[:5]=='PASS ' and len(x)>5:
            password=x[5:-2]
            text,IsPass = self.is_password(username,password)
            conn.sendall(text+'\r\n')
            if not IsPass:
                print(text)
                return
        print(username+' realy get in')
        x = conn.recv(BUF_SIZE) #wait for client send command
        if not x:
            conn.close()
            return
        while x!='QUIT':
            if x[:4]!='STAT' and x[:4]!='LIST' and x[:5]!='RETR ' and x[:5]!='DELE ':
                conn.sendall('error command')
                conn.close()
                return
            if x[:4]=='STAT':
                conn.sendall(self.stat(username))
            if x[:4]=='LIST':
                conn.sendall(self.List(username))
            if x[:5]=='RETR ':
                if(x>5):
                    numMail=int(x[5:-2])
                else:
                    numMail=0
                conn.sendall(self.retr(username,numMail))
            if x[:5]=='DELE ':
                if(x>5):
                    numMail=int(x[5:-2])
                else:
                    numMail=0
                conn.sendall(self.deleteMail(username, numMail))
            x = conn.recv(BUF_SIZE) #wait for client send command
            if not x:
                conn.close()
                return
        s.sendall('+OK POP3 server signing off\r\n')

    def SaveMailInDominsBoxes(self, BodyMail, Domains):
        if not os.path.exists('mails'):
            os.makedirs('mails')
        for D in Domains:
            if self.is_user_domain_exist_in_DB(D):
                directory='mails\\'+D
                if not os.path.exists(directory):
                    os.makedirs(directory)
                i=1
                MailName=str(i)+'.txt'
                PathMail=directory+'\\'+MailName
                while os.path.isfile(PathMail):
                    i+=1
                    MailName=str(i)+'.txt'
                    PathMail=directory+'\\'+MailName
                f=open(PathMail,'wb')
                f.write(BodyMail)
                f.close()
                print('mail saved as: '+PathMail)
            else:
                print('user domain not exist - so the mail not sent')

    def is_user_domain_exist_in_DB(self,UserName):
        if os.path.exists('../users&passwords.txt'):
            f=open('../users&passwords.txt', 'rb')
            d=ast.literal_eval(f.read()) #get all users
            print(d)
        else:
            d={}
        if UserName in d:
            print('yes')
            return True
        print('no')
        return False

    #---------------------pop3 server functions--------------------

    def find_user_in_DB(self,username):
        if os.path.exists(USERS_PASSWORDS_FILE):
            f=open(USERS_PASSWORDS_FILE,'rb')
            d=ast.literal_eval(f.read())
            if username in d:
                return '+OK User accepted',True
            else:
                return 'user not found',False
        else:
            return 'error in DB',False

    def is_password(self,username,password):
        if os.path.exists(USERS_PASSWORDS_FILE):
            f=open(USERS_PASSWORDS_FILE,'rb')
            d=ast.literal_eval(f.read())
            if d[username]==password:
                return '+OK Pass accepted',True
            else:
                return '-ERR wrong password',False
        else:
            return '-ERR error in DB',False

    def deleteMail(self, username, numMail):
        UserDirectory='mails\\'+username
        if not os.path.exists(UserDirectory):
            os.makedirs(UserDirectory)
        TheFile=UserDirectory+'\\'+str(numMail)+'.txt'
        if not os.path.isfile(TheFile):
            return '-ERR mail not found'
        os.remove(TheFile)
        #so now must change names of all the upper files to their name -1
        #so over all files and give them new names
        count = 0 #count how much mails in his box mail
        for dirpath, dirnames, filenames in os.walk(UserDirectory):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                count+=1
                #print 'old name: '+fp
                #print 'new name: '+dirpath+'\\'+str(count)+'.txt'
                os.rename(fp, dirpath+'\\'+str(count)+'.txt')
        return '+OK message '+str(numMail)+' deleted\r\n'

    def retr(self,username,numMail):
        UserDirectory='mails\\'+username
        if not os.path.exists(UserDirectory):
            os.makedirs(UserDirectory)
        TheFile=UserDirectory+'\\'+str(numMail)+'.txt'
        if not os.path.isfile(TheFile):
            return '-ERR mail not found'
        size = os.path.getsize(TheFile)
        f=open(TheFile,'rb')
        BodyMail=f.read()
        f.close()
        str1='+OK '+str(size)+' octets\r\n'
        str2='<the POP3 server sends message '+str(numMail)+'>\r\n'
        return str1+str2+BodyMail

    def List(self,username):
        UserDirectory='mails\\'+username
        if not os.path.exists(UserDirectory):
            os.makedirs(UserDirectory)
        count = 0 #count how much mails in his box mail
        total_size = 0
        MailsParameters=''
        for dirpath, dirnames, filenames in os.walk(UserDirectory):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                size= os.path.getsize(fp)
                total_size += size
                count+=1
                MailName=os.path.basename(f)[:-4] #without '.txt'
                MailsParameters+=MailName+' '+str(size)+'\r\n'
        return '+OK '+str(count)+' messages ('+str(total_size)+' octets)\r\n'+MailsParameters+'.\r\n'

    def stat(self,username):
        UserDirectory='mails\\'+username
        if not os.path.exists(UserDirectory):
            os.makedirs(UserDirectory)
        list_dir = []
        list_dir = os.listdir(UserDirectory)
        count = 0 #count how much mails in his box mail
        for file in list_dir:
            count+=1
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(UserDirectory):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return '+OK '+str(count)+' '+str(total_size)+'\r\n'



if __name__=='__main__':
    ServerSMTP_and_POP3()
