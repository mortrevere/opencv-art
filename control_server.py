import socket
import threading

HELP_STRING = """
Commands :
- ls : list services. '*' = bypassed, '~' = currently deploying
- bypass X : next deployment of X will be direct
- nobypass X : next deployment of X will be normal
- abort X : abort running deployment
"""


class ControlServer:
    def __init__(self, port, canaries):
        self.port = port
        self.canaries = canaries
        self.server_thread = threading.Thread(target=self.server)
        self.server_thread.start()
        # self.server_thread.join()
        # print("AdminServer crashed")

    def server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(("127.0.0.1", self.port))
            s.listen(1)

            while True:
                self.conn, self.addr = s.accept()
                with self.conn:
                    print("[AdminServer] Connection from", self.addr)
                    # self.reply(HELP_STRING, prompt=False)
                    # self.reply("List of services : ", prompt=False)
                    # self.send_list()
                    while True:
                        data = self.conn.recv(1024)
                        if not data:
                            print("[AdminServer] Disconnect :", self.addr)
                            break
                        self.handle(data)

    def reply(self):
        self.conn.sendall(data.encode("utf-8"))

    def handle(self, data):
        data = data.strip().decode()
        self.canaries = data
        chunks = data.split()
        if not len(chunks):
            self.reply()
            return

        self.reply(data)
