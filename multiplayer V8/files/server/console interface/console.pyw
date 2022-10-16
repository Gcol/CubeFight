# =============================================================================================
# "console.pyw" - dedicated for start the modules 
#
#  UPBGE Multiplayer online - 8.0                                        
#
#      ---INFORMATION---                                          
#      created by: Henrique Rodrigues (HenryQFX)                  
#      channel: youtube.com/channel/UCc39h8udpdOLwfU-u-X8Bbg   
#      github:  https://github.com/HenryQFX                    
# =============================================================================================

try:
    import threading, logging, datetime, time, sys, os, psutil
    import tkinter as tk 
    import tkinter.ttk as ttk
    import tkinter.scrolledtext as ScrolledText

    from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu
    from PyQt5.QtGui import QIcon

    from modules import authentication as authentication
    from modules import blue as blue
except ImportError as error:
    print(error)

global console_information, current_time
console_information = {"STARTED":0, "CPU":0, "RAM":0, "PID":0}

now = datetime.datetime.now()
current_time = "({}-{}-{}-{}:{}:{})".format(now.day,now.month,now.year, now.hour,now.minute,now.second)

class TextHandler(logging.Handler):
    def __init__(self, text):
        logging.Handler.__init__(self)
        self.text = text

    def emit(self, record):
        msg = self.format(record)

        try:
            def append():
                self.text.configure(state="normal")
                self.text.insert(tk.END, current_time + " " + msg + "\n")
                self.text.configure(state="disabled")
                self.text.yview(tk.END)
            self.text.after(0, append)
        except:
            sys.exit(0)
            print("[TEXTHANDLER/EMIT] Fatal error!")

class GUI(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.logs()
        self.widgets()
        self.build_GUI()

        theme = ttk.Style()
        theme.theme_use("clam")
        
    def build_GUI(self):
        self.root.title("LION Console (beta) | created by: HenryQFX")
        self.root.option_add("*tearOff", "FALSE")
        self.grid(column=0, row=0, sticky="ew")
        self.grid_columnconfigure(0, weight=1, uniform="a")
        self.grid_columnconfigure(1, weight=1, uniform="a")
        self.grid_columnconfigure(2, weight=1, uniform="a")
        self.grid_columnconfigure(3, weight=1, uniform="a")
        
        # add text widget to display logging info
        st = ScrolledText.ScrolledText(self, state="disabled", fg="black")
        st.configure(font="TkFixedFont")
        st.grid(column=0, row=1, sticky="w", columnspan=4)

        # create textLogger
        text_handler = TextHandler(st)

        # add the handler to logger
        logger = logging.getLogger()        
        logger.addHandler(text_handler)

    def widgets(self):
        try:
            def command(value):
                PREFIX = "/"
                COMMANDS = ["/help", "/?", "/clear", "/log_clear", "/log_lines"]

                if str(value).startswith(PREFIX):
                    if value in COMMANDS:
                        # for (/help)
                        if value == "/help": logging.info("[CONSOLE] results: {} ".format(COMMANDS))

                        # for (/?)
                        if value == "/?": logging.info("[CONSOLE] results: {} ".format(COMMANDS))
                        
                        # for (/clear)
                        if value == "/clear":
                            self.build_GUI()
                            logging.info("{}[GUI] reseted!".format(current_time))

                        # for (/log_clear)
                        if value == "/log_clear":
                            try:
                                file = open("logs/logs.txt", "w")

                                file.truncate(0)
                                logging.info("[LOG] clear!")

                            except:
                                file = open("server/logs/logs.txt", "w")
                            
                                file.truncate(0)
                                logging.info("[LOG] clear!")

                        # for (/log_lines)
                        if value == "/log_lines":
                             try:
                                file = open("logs/logs.txt", "r")
                                lines = 0
                                for line in file:
                                    lines += 1
                                logging.info("[LOG] lines: {}".format(lines))

                             except:
                                file = open("server/logs/logs.txt", "r")
                                lines = 0
                                for line in file:
                                    lines += 1
                                logging.info("[LOG] lines: {}".format(lines))
                                    
                    else:
                        logging.info("[CONSOLE] unknow command, use '/help or /?' for help")
                else:
                    logging.info("[CONSOLE] use '/' for commands!")
                
            def widget_command():
                # add entry
                entry = tk.Entry(self, width=25)
                entry.grid(column=0, row=2, sticky="w", columnspan=4)

                # add button
                button = tk.Button(self, text="submit", width=5, command=lambda:command(entry.get()))
                button.grid(column=1, row=2, sticky="w", columnspan=4)
            
            widget_command()

            def widget_1():
                while True:
                    time.sleep(3.0)
                    w1 = tk.Label(self, text="connections: {}".format(blue.info["players-online"]))
                    w1.grid(column=0, row=3, sticky="w", columnspan=4, padx=1, pady=0)

            def widget_2():
                with psutil.Process().oneshot():
                    epoch = psutil.Process().create_time()

                    started = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch)))
                    console_information["STARTED"] = started
                
                while True:
                    time.sleep(1.0)

                    CPU = psutil.cpu_percent()
                    console_information ["CPU"] = CPU

                    RAM = psutil.virtual_memory().percent
                    console_information ["RAM"] = RAM

                    PID = os.getpid()
                    console_information["PID"] = PID

                    w1 = tk.Label(self, text="({}) | CPU: ({}) | RAM: ({}) | PID: ({})".format(started, CPU, RAM, PID))
                    w1.grid(column=3, row=3, sticky="w", columnspan=4, padx=2, pady=0)

            thread_widget_1 = threading.Thread(target=widget_1, args=[], daemon=True)
            thread_widget_2 = threading.Thread(target=widget_2, args=[], daemon=True)
            
            thread_widget_1.start()
            thread_widget_2.start()

        except:
            sys.exit(0)
            print("[GUI/WIDGETS] Fatal error!")

    def logs(self):
        try:
            logging.basicConfig(filename="logs/logs.txt",
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s')
        except:
            logging.basicConfig(filename="server/logs/logs.txt",
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s')

# application engine
class Application():
    def __init__(self):
        self.root = tk.Tk()
        self.root.resizable(False, False)

        self.thread_modules_authentication = threading.Thread(target=self.module_authentication, args=[], daemon=True)
        self.thread_modules_blue = threading.Thread(target=self.module_blue, args=[], daemon=True)

        # tray
        self.thread_tray = threading.Thread(target=self.tray, args=[], daemon=True)
        self.thread_tray.start()

        self.update()
           
    def tray(self):
        # windowsOS only
        
        app = QApplication(sys.argv)
        
        tray_icon = QSystemTrayIcon(QIcon("icon.png"), parent=app)
        tray_icon.setToolTip(("LION Console | started as: ({})".format(console_information["STARTED"])))
        tray_icon.show()

        menu = QMenu()
        
        close = menu.addAction("close console")
        close.triggered.connect(exit)

        tray_icon.setContextMenu(menu)

        sys.exit(app.exec_())

    def module_authentication(self):
        time.sleep(2.5)
        authentication.Authentication()
    
    def module_blue(self):
        time.sleep(3)
        blue.Blue()
             
    def update(self):
        GUI(self.root)
        logging.info("---------------------------------------")
        logging.info("created by: HenryQFX")
        logging.info("github:  https://github.com/HenryQFX")
        logging.info("---------------------------------------\n")

        try:
            self.root.tk.call("wm", "iconphoto", self.root._w, tk.PhotoImage(file="icon.png"))
        except:
            self.root.tk.call("wm", "iconphoto", self.root._w, tk.PhotoImage(file="server/icon.png"))
        
        self.thread_modules_authentication.start()
        self.thread_modules_blue.start()

        print("application running")
        self.root.mainloop() 
     
        sys.exit()
        ### self.thread_modules_authentication.join()
        ### self.thread_modules_blue.join()        
       
Application()


