from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, unquote_plus
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import pathlib
import mimetypes
import json


DATA_FILE = "storage/data.json"
# Set up Jinja2 template environment
env = Environment(loader=FileSystemLoader("."))


class WebHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        pr_url = urlparse(self.path)
        path = pr_url.path

        if path == "/":
            self.send_html_file("index.html")
        elif path == "/message.html":
            self.send_html_file("message.html")
        elif path == "/read":
            self.send_read_page()
        elif pathlib.Path().joinpath(path[1:]).exists():
            self.send_static()
        else:
            self.send_html_file("error.html", 404)

    def do_POST(self):
        if self.path == "/message":
            length = int(self.headers.get("Content-Length", 0))
            data = self.rfile.read(length)
            data_str = unquote_plus(data.decode())
            data_dict = dict(el.split("=") for el in data_str.split("&"))

            timestamp = str(datetime.now())

            with open(DATA_FILE, "r+", encoding="utf-8") as f:
                messages = json.load(f)
                messages[timestamp] = data_dict
                f.seek(0)
                json.dump(messages, f, indent=2, ensure_ascii=False)
                f.truncate()

            self.send_response(302)
            self.send_header("Location", "/")
            self.end_headers()

    def send_html_file(self, filename, status=200):
        try:
            with open(filename, "rb") as f:
                self.send_response(status)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(f.read())
        except FileNotFoundError:
            self.send_html_file("error.html", 404)

    def send_static(self):
        mt = mimetypes.guess_type(self.path)[0] or "text/plain"
        try:
            with open(f".{self.path}", "rb") as f:
                self.send_response(200)
                self.send_header("Content-type", mt)
                self.end_headers()
                self.wfile.write(f.read())
        except FileNotFoundError:
            self.send_html_file("error.html", 404)

    def send_read_page(self):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            messages = json.load(f)

        template = env.get_template("read.html")
        content = template.render(messages=messages)

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(content.encode("utf-8"))


def run(server_class=HTTPServer, handler_class=WebHandler):
    server_address = ("", 3000)
    httpd = server_class(server_address, handler_class)
    print("Server started on port 3000...")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
