from functools import cached_property
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qsl, urlparse
import uuid
from urllib.parse import urlparse, parse_qs, urlencode
from modules import (
    get_path_formated,
    get_book_page
)
from routes import (
    get_index,
    get_404_page
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
        if self.path:
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            
            if self.query_data and 'q' in self.query_data:
                self.wfile.write(self.get_response(self.query_data['q']).encode("utf-8"))
            else:
                self.wfile.write(self.get_response().encode("utf-8"))
            
   
    def get_response(self,query_search=""):
        result = get_path_formated(self.path)
        
        if result:
            if  result[0] == "get_index":
                print(query_search)
                return get_index(query_search)
            elif result[0] == "get_book_page":
                return get_book_page(int(result[1]["book_id"]))
            
        else:
            return get_404_page()
        
            
if __name__ == "__main__":
    print("Server starting...")
    #server = HTTPServer(("0.0.0.0", 8000), WebRequestHandler)
    server = HTTPServer(("localhost", 8000), WebRequestHandler)
    server.serve_forever()
