import socket
import os
import ast  # to convert string to dictionary
import threading
from threading import Thread

HOST = '127.0.0.1'
PORT_SMTP = 25
PORT_POP3 = 110
ADDR_SMTP = (HOST, PORT_SMTP)
ADDR_POP3 = (HOST, PORT_POP3)
SERVERNAME = 'SN'
BUF_SIZE = 4096

USERS_PASSWORDS_FILE = "users&passwords.txt"
SEPERATOR = "/"


class ServerSMTP_and_POP3:
    def __init__(self):
        self.running = True

        Thread(target=self.main_smtp).start()
        Thread(target=self.main_pop3).start()

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

    # --------------------smtp server functions---------------------

    def handle_smtp_client(self, conn, addr):
        Domains = []

        # wait for connection for the client
        msg_to_all = '220 ' + SERVERNAME + ' ESMTP Postfix'
        conn.sendall(msg_to_all.encode())
        request = conn.recv(BUF_SIZE)
        request = request.decode()

        if not request:
            conn.close()
            return
        if request.split()[0] != 'HELO' and request.split()[0] != 'EHLO':
            conn.close()
            return
        hello_res = '250 Hello ' + request.split()[1] + ' , I am glad to meet you'

        conn.sendall(hello_res.encode())

        request = conn.recv(BUF_SIZE).decode()

        if not request:
            conn.close()
            return
        if request[:9] != 'MAIL FROM':
            conn.close()
            return

        user_name = request[10:-1]
        hello_res = '250 Hello ' + request.split()[1] + ' , I am glad to meet you'

        conn.sendall(hello_res.encode())
        request = conn.recv(BUF_SIZE).decode()
        if not request:
            conn.close()
            return

        if request[:9] == 'RCPT TO:<':
            Domains = (request[9:-3]).split(',')

            print('domains:', Domains)

            ok_msg = '250 OK'
            conn.sendall(ok_msg.encode())
            request = conn.recv(BUF_SIZE).decode()

            if not request:
                conn.close()
                return

        if request[:4] != 'DATA':
            conn.close()
            return

        msg_354 = '354 End data with <CR><LF>.<CR><LF>'
        conn.sendall(msg_354.encode())
        DATA = conn.recv(BUF_SIZE).decode()

        if not DATA:
            conn.close()
            return
        BodyMail = user_name + DATA

        while DATA[-5:] != '\r\n.\r\n':
            DATA = conn.recv(BUF_SIZE).decode()
            if not DATA:
                print("error in parsing data from smtp client")
                conn.close()
                return

            BodyMail += DATA
        print('-----The all mail: -----')
        print(BodyMail)
        print('------------------------')

        self.SaveMailInDominsBoxes(BodyMail, Domains)

        ok_250 = '250 Ok'
        conn.sendall(ok_250.encode())

        request = conn.recv(BUF_SIZE).decode()

        if not request:
            conn.close()
            return
        if request[:4] != 'QUIT':
            conn.close()
            return

        bye_221 = '221 Bye'
        conn.sendall(bye_221.encode())
        # close the connection to the specific client
        conn.close()

    def handle_pop3_client(self, conn, addr):
        # wait for connection for the client

        client_msg = conn.recv(BUF_SIZE).decode()  # wait for client send username
        if not client_msg:
            print("error in handle_pop3_client didn't receive client username")
            conn.close()
            return
        if client_msg[:5] != 'USER ':
            msg = 'data did not recieve correctly'
            conn.sendall(msg.encode())
            conn.close()
            return
        if len(client_msg) < 6:
            msg = 'did not get the username'
            conn.sendall(msg.encode())
            conn.close()
            return
        if client_msg[:5] == 'USER ' and len(client_msg) > 5:
            username = client_msg[5:-2]
            print(username + ' try get in')
            text, IsFound = self.find_user_in_DB(username)

            text_msg = text + '\r\n'
            conn.sendall(text_msg.encode())

            if not IsFound:
                print(text)
                return

        client_msg = conn.recv(BUF_SIZE).decode()  # wait for client send password
        if not client_msg:
            conn.close()
            return
        if client_msg[:5] != 'PASS ':
            err_msg = '-ERR data did not recieve correctly'
            conn.sendall(err_msg.encode())
            conn.close()
            return
        if len(client_msg) < 6:
            err_msg = '-ERR did not get the password'
            conn.sendall(err_msg.encode())
            conn.close()
            return
        if client_msg[:5] == 'PASS ' and len(client_msg) > 5:
            password = client_msg[5:-2]
            text, IsPass = self.is_password(username, password)

            text_msg = text + '\r\n'
            conn.sendall(text_msg.encode())
            if not IsPass:
                print("error: " + text)
                return

        print(username + ' got in')

        client_msg = conn.recv(BUF_SIZE).decode()  # wait for client send command
        if not client_msg:
            print("error - No msg received from client")
            conn.close()
            return

        while client_msg != 'QUIT':
            if client_msg[:4] != 'STAT' and client_msg[:4] != 'LIST' and client_msg[:5] != 'RETR ' and client_msg[
                                                                                                       :5] != 'DELE ':
                err_msg = 'error command'
                conn.sendall(err_msg.encode())
                conn.close()
                return
            if client_msg[:4] == 'STAT':
                conn.sendall(self.stat(username).encode())
            if client_msg[:4] == 'LIST':
                conn.sendall(self.List(username).encode())
            if client_msg[:5] == 'RETR ':
                if (len(client_msg) > 5):
                    numMail = int(client_msg[5:-2])
                else:
                    numMail = 0
                conn.sendall(self.retr(username, numMail).encode())
            if client_msg[:5] == 'DELE ':
                if (len(client_msg) > 5):
                    numMail = int(client_msg[5:-2])
                else:
                    numMail = 0
                conn.sendall(self.delete_mail(username, numMail).encode())
            client_msg = conn.recv(BUF_SIZE).decode()  # wait for client send command
            if not client_msg:
                conn.close()
                return

        ok_msg = '+OK POP3 server signing off\r\n'
        conn.sendall(ok_msg.encode())

    def SaveMailInDominsBoxes(self, BodyMail, Domains):
        if not os.path.exists('mails'):
            os.makedirs('mails')
        for D in Domains:
            if self.is_user_domain_exist_in_DB(D):
                directory = 'mails' + SEPERATOR + D
                if not os.path.exists(directory):
                    os.makedirs(directory)
                i = 1
                mail_name = str(i) + '.txt'
                path_mail = directory + SEPERATOR + mail_name
                while os.path.isfile(path_mail):
                    i += 1
                    mail_name = str(i) + '.txt'
                    path_mail = directory + SEPERATOR + mail_name
                f = open(path_mail, 'w')
                f.write(BodyMail)
                f.close()

                print('mail saved as: ' + path_mail)
            else:
                print('user domain not exist - so the mail did not send')

    def is_user_domain_exist_in_DB(self, UserName):
        if os.path.exists(USERS_PASSWORDS_FILE):
            f = open(USERS_PASSWORDS_FILE)
            d = ast.literal_eval(f.read())  # get all users
            print(d)
        else:
            d = {}
        if UserName in d:
            print('yes')
            return True
        print('no')
        return False

    # ---------------------pop3 server functions--------------------

    def find_user_in_DB(self, username):
        if os.path.exists(USERS_PASSWORDS_FILE):
            f = open(USERS_PASSWORDS_FILE)
            d = ast.literal_eval(f.read())
            if username in d:
                return '+OK User accepted', True
            else:
                return 'user not found', False
        else:
            return 'error in DB', False

    def is_password(self, username, password):
        if os.path.exists(USERS_PASSWORDS_FILE):
            f = open(USERS_PASSWORDS_FILE)
            d = ast.literal_eval(f.read())
            if d[username] == password:
                return '+OK Pass accepted', True
            else:
                return '-ERR wrong password', False
        else:
            return '-ERR error in DB', False

    def delete_mail(self, username, numMail):
        UserDirectory = 'mails' + SEPERATOR + username
        if not os.path.exists(UserDirectory):
            os.makedirs(UserDirectory)
        file_to_delete = UserDirectory + SEPERATOR + str(numMail) + '.txt'
        if not os.path.isfile(file_to_delete):
            return '-ERR mail not found'
        os.remove(file_to_delete)

        print("file got deleted: ", file_to_delete)
        # so now must change names of all the upper files to their name -1
        # so over all files and give them new names
        count = 0  # count how much mails in his box mail
        for dirpath, dirnames, filenames in os.walk(UserDirectory):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                count += 1
                os.rename(fp, dirpath + SEPERATOR + str(count) + '.txt')
        return '+OK message ' + str(numMail) + ' deleted\r\n'

    def retr(self, username, numMail):
        UserDirectory = 'mails' + SEPERATOR + username
        if not os.path.exists(UserDirectory):
            os.makedirs(UserDirectory)
        TheFile = UserDirectory + SEPERATOR + str(numMail) + '.txt'
        if not os.path.isfile(TheFile):
            return '-ERR mail not found'
        size = os.path.getsize(TheFile)
        f = open(TheFile)
        BodyMail = f.read()
        f.close()
        str1 = '+OK ' + str(size) + ' octets\r\n'
        str2 = '<the POP3 server sends message ' + str(numMail) + '>\r\n'
        return str1 + str2 + BodyMail

    def List(self, username):
        user_dir = 'mails' + SEPERATOR + username
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)
        count = 0  # count how much mails in his box mail
        total_size = 0
        MailsParameters = ''
        for dirpath, dirnames, filenames in os.walk(user_dir):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                size = os.path.getsize(fp)
                total_size += size
                count += 1
                MailName = os.path.basename(f)[:-4]  # without '.txt'
                MailsParameters += MailName + '         ' + str(size) + '\r\n'
        return '+OK ' + str(count) + ' messages (' + str(total_size) + ' octets)\r\n' + MailsParameters + '.\r\n'

    def stat(self, username):
        UserDirectory = 'mails' + SEPERATOR + username
        if not os.path.exists(UserDirectory):
            os.makedirs(UserDirectory)
        list_dir = []
        list_dir = os.listdir(UserDirectory)
        count = 0  # count how much mails in his box mail
        for file in list_dir:
            count += 1
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(UserDirectory):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return '+OK ' + str(count) + ' ' + str(total_size) + '\r\n'


if __name__ == '__main__':
    ServerSMTP_and_POP3()
