from functools import cached_property
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qsl, urlparse
from modules import (
    get_path_formated,
    get_book_page,
    get_404_page,
    get_index
)

        
class WebRequestHandler(BaseHTTPRequestHandler):
    
    @cached_property
    def url(self):
        return urlparse(self.path)

    @cached_property
    def query_data(self):
        return dict(parse_qsl(self.url.query))

    @cached_property
    def post_data(self):
        content_length = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(content_length)

    @cached_property
    def form_data(self):
        return dict(parse_qsl(self.post_data.decode("utf-8")))

    @cached_property
    def cookies(self):
        return SimpleCookie(self.headers.get("Cookie"))
    
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(self.get_response().encode("utf-8"))

    def get_response(self):
        result = get_path_formated(self.path)
        print(result)
        if result:
            if result[0] == "get_index":
                return get_index()
            elif result[0] == "get_book_page":
                return get_book_page(int(result[1]["book_id"]))
            elif result[0] == "/favicon.ico":
                pass
            else:
                return get_404_page()
            
        


if __name__ == "__main__":
    print("Server starting...")
    #server = HTTPServer(("0.0.0.0", 8000), WebRequestHandler)
    server = HTTPServer(("localhost", 8000), WebRequestHandler)
    server.serve_forever()
