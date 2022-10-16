# =============================================================================================
# "authentication.py" - dedicated for start (AUT) server 
#
#  UPBGE Multiplayer online - 8.0                                        
#
#      ---INFORMATION---                                          
#      creator: Henrique Rodrigues (HenryQFX)                  
#      channel: youtube.com/channel/UCc39h8udpdOLwfU-u-X8Bbg   
#      github:  https://github.com/HenryQFX                    
# =============================================================================================

import sqlite3, json, select, socket, threading, traceback, time

class Authentication():
    def __init__(self):
        self.HOST = ("127.0.0.1", 8282)
        self.static = {"BUFFER":8192, "TIMEOUT":0.1, "PREFIX":"$"}

        """SOCKET"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(self.HOST)
        self.socket.listen(0)
    
        self.update()

    def info(self, lvl, content):
        if lvl == "N": print("[AUTHENTICATION/INFO] ({})".format(content))
        
        if lvl == "E": print("[AUTHENTICATION/ERROR] ({})".format(content))

        if lvl == "W": print("[AUTHENTICATION/WARNING] ({})".format(content))

    def login(self, client, address, username, password):
        self.info("N", "address: ({}:{}) username: [{}] connected!".format(address[0], address[1], username))

        try:
            database = sqlite3.connect("../database.db")
        except:
            client.send(str("ERROR{}{}".format(self.static["PREFIX"], "[SERVER]: Account query error!")).encode())
            

        cursor = database.cursor()
        cursor.execute("SELECT * FROM accounts WHERE username = '{}';".format(username))
        
        user = cursor.fetchall()

        if user:
            if password == user[0][2]:
                client.send(str("LOGGED{}({})".format(self.static["PREFIX"], user[0][1])).encode())
                self.info("W", "address: ({}:{}) username: [{}] in queue!\n".format(address[0], address[1], username))
            else:
                client.send(str("ERROR{}{}".format(self.static["PREFIX"], "[SERVER]: Invalid password!")).encode())
        else:
            client.send(str("ERROR{}{}".format(self.static["PREFIX"], "[SERVER]: Invalid username!")).encode())

    def on_disconnected(self, client, address):
        client.close()

    def on_connected(self, client, address):
        username = None
        password = None

        try:
            inputs, outputs = [client], []
            while inputs:
                r, w, e = select.select(inputs, outputs, inputs, self.static["TIMEOUT"])
                for connection in r:
                    if connection is client:
                        data = json.loads(connection.recv(self.static["BUFFER"]))
                        
                        if "login" in data:
                            username = data["login"][0]
                            password = data["login"][1]

                            self.login(client, address, username, password)
                        else:
                            self.on_disconnected(client, address)
                                                        
        except:
            ### print(traceback.format_exc())
            self.on_disconnected(client, address)

    def update(self):
        print("[AUTHENTICATION/START] listening on: {}:{}".format(self.HOST[0], self.HOST[1]))
        
        while True:
            client, address = self.socket.accept()
            
            t = threading.Thread(target=self.on_connected, args=(client, address))
            t.start()

authentication = Authentication()


