# =============================================================================================
# "blue.py" - dedicated for start (players update) 
#
#  UPBGE Multiplayer online - 8.0                                        
#
#      ---INFORMATION---                                          
#      creator: Henrique Rodrigues (HenryQFX)                  
#      channel: youtube.com/channel/UCc39h8udpdOLwfU-u-X8Bbg   
#      github:  https://github.com/HenryQFX                    
# =============================================================================================

import json, select, socket, threading, traceback, time 


class Blue():
    def __init__(self):
        self.HOST = ("127.0.0.1", 8181)
        self.static = {"BUFFER":8192, "TIMEOUT":0.1, "PREFIX":"$"}

        """SOCKET"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(self.HOST)
        self.socket.listen(1)

        self.players = {}
        
        self.update()
        
    def info(self, lvl, content):
        if lvl == "N": print("[BLUE/INFO] ({})".format(content))
        
        if lvl == "E": print("[BLUE/ERROR] ({})".format(content))

        if lvl == "W": print("[BLUE/WARNING] ({})".format(content))

    def enter(self, client, username):
        self.info("N", "player {} connected!".format(username))

        client.send(str("WELCOME{}{}".format(self.static["PREFIX"], "welcome: {}".format(username))).encode())
        self.players[username] = {}

    def on_disconnected(self, client, address, username):
        try:
            del self.players[username]
            
            time.sleep(self.static["TIMEOUT"])
            client.close()

            self.info("N", "player: {} [{}] disconnected!".format(username, address))
        
        except:
            time.sleep(self.static["TIMEOUT"])
            client.close()
            
            self.info("E", "was forced to disconnect from: [{}]".format(address))

    def on_connected(self, client, address):
        username = None
        
        try:
            inputs, outputs = [client], []
            while inputs:
                r, w, e = select.select(inputs, outputs, inputs, self.static["TIMEOUT"])
                for connection in r:
                    if connection is client:
                        data = json.loads(connection.recv(self.static["BUFFER"]))

                        if "username" in data:
                            username = str(data["username"])
                            
                            if username in list(self.players.keys()):
                                # check if the name is being used
                                self.info("W", "client: [{}] username ({}) in use!".format(address, username))
            
                                client.send(str("ERROR{}{}".format(self.static["PREFIX"], "username: ({}) in use!".format(username))).encode())
                                
                                client.close()
                            else:
                                self.enter(client, username)
                        
                        if data:
                            # update: position/rotation
                            position, rotation = None, None
                    
                            if "position" in data: position = data["position"]
                            if "rotation" in data: rotation = data["rotation"]
                            self.players.update({username:{"position":position, "rotation":rotation}})

                            if position == None:
                                time.sleep(0.1)
                            else:
                                client.sendall(str("INFO{}{}".format(self.static["PREFIX"], self.players)).encode())

                        else: 
                            client.close()

        except: 
            self.on_disconnected(client, address, username)

    def update(self):
        print("[BLUE/START] listening on: {}:{}\n".format(self.HOST[0], self.HOST[1]))

        while True:

            client, address = self.socket.accept()
            t = threading.Thread(target=self.on_connected, args=(client, address))
            t.start()

blue = Blue()





