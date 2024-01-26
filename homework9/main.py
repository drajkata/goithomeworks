import mimetypes
import pathlib
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import socket
from time import sleep
import threading
from datetime import datetime
import json


UDP_IP = "127.0.0.1"
UDP_PORT = 5000
APP_IP = 3000

class HttpHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        # print(data)
        socket_run_client(UDP_IP, UDP_PORT, data)
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()

    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_html_file("./index.html")
        elif pr_url.path == '/message':
            self.send_html_file("./message.html")
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file("./error.html", 404)

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        with open(f'.{self.path}', 'rb') as file:
            self.wfile.write(file.read())


def run(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = ('', APP_IP)
    http_server = server_class(server_address, handler_class)
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()

def socket_run_client(ip = UDP_IP, port = UDP_PORT, data = b""):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = ((ip, port))
    for i in range(0, len(data), 1024):
        data_part = data[i: i + 1024]
        sock.sendto(data_part, (ip, port))
    sock.sendto(b"END", server)
    sock.close()

def socket_run_server(ip = UDP_IP, port = UDP_PORT):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = ((ip, port))
    sock.bind(server)
    to_save = b""
    file_name = './storage/data.json'
    try:
        while True:
            data, address = sock.recvfrom(1024)
            if data == b"END":
                to_save_parse = urllib.parse.unquote_plus(to_save.decode())
                # print(to_save_parse)
                data_dict = {key: value for key, value in [el.split('=') for el in to_save_parse.split('&')]}
                with open(file_name, "r") as fh:
                    json_dict = json.load(fh)
                json_dict[str(datetime.now())] = data_dict
                with open(file_name, "w") as fh:
                    json.dump(json_dict, fh)
                to_save = b""
            else:
                to_save += data
    except KeyboardInterrupt:
        print(f'Destroy server')
    finally:
        sock.close()

def main():
    http_server = threading.Thread(target=run)
    socket_server = threading.Thread(target=socket_run_server, args=(UDP_IP, UDP_PORT))
    socket_server.start()
    http_server.start()
    socket_server.join()
    http_server.join()  

if __name__ == '__main__':
    main()
