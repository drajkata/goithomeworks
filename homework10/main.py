import platform
import sys
import aiohttp
import asyncio
from datetime import datetime, timedelta
import mimetypes
import pathlib
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
from http import HTTPStatus
import template_index

APP_IP = 3000

class HttpHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        self.send_response(HTTPStatus.FOUND.value)
        self.send_header('Location', '/')
        self.end_headers()

    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            asyncio.run(get_data())
            self.send_html_file("./index.html")
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file("./error.html", HTTPStatus.NOT_FOUND.value)

    def send_html_file(self, filename, status=HTTPStatus.OK.value):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def send_static(self):
        self.send_response(HTTPStatus.OK.value)
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

async def get_page(url, session):
    try:
        async with session.get(url) as response:
            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])
            if response.status == HTTPStatus.OK.value:
                html = await response.text()
                return html
            else:
                print(f"Error status: {response.status} for {url}")
    except aiohttp.ClientConnectionError as error:
        print(f"Connection error: {url}", str(error))


def generate_url(currency, delta):
    currency=currency
    end=datetime.now()
    start=end-timedelta(days=int(delta))
    start_date = start.date()
    end_date = end.date()
    url = f'http://api.nbp.pl/api/exchangerates/rates/A/{currency}/{start_date.isoformat()}/{end_date.isoformat()}/'
    return url

async def get_data():
    async with aiohttp.ClientSession() as session:
        results = await asyncio.gather(get_page(generate_url("EUR", sys.argv[1]), session), get_page(generate_url("USD", sys.argv[1]), session))
        template_index.main(results)

def isValid_argv(arg):
    if int(arg) > 10:
        return False
    else:
        return True

if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    if isValid_argv(sys.argv[1]):
        run()
    else:
        print(f"\nInvalid period entered. You can see the exchange rate summary for a maximum of 10 days.\n")

