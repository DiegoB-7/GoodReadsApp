from functools import cached_property
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qsl, urlparse
import uuid
from urllib.parse import urlparse, parse_qs, urlencode
from modules import (
    get_path_formated,
    get_book_page,
    add_book_to_session   
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
    
    def get_book_session(self):
        c = self.cookies
        if not c:
            c = SimpleCookie()
            c["session"] = uuid.uuid4()
            c["session"]["max-age"] = 86400
        return c.get("session").value

    def set_book_cookie(self, session_id, max_age=86400):
        c = SimpleCookie()
        c["session"] = session_id
        c["session"]["max-age"] = max_age
        self.send_header('Set-Cookie', c.output(header=''))
    
    def do_GET(self):
        if self.path:
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            session_id = self.get_book_session()
            if session_id:
                self.set_book_cookie(session_id)
            self.end_headers()
            
            if self.query_data and 'q' in self.query_data:
                self.wfile.write(self.get_response(self.query_data['q']).encode("utf-8"))
            else:
                self.wfile.write(self.get_response().encode("utf-8"))
            
    def get_response(self, query_search=""):
        result = get_path_formated(self.path)
        session_id = self.get_book_session()
        if result:
            if result[0] == "get_index":
                return get_index(query_search,session_id)
            elif result[0] == "get_book_page":
                
                add_book_to_session(self.get_book_session(), int(result[1]["book_id"]))
                return get_book_page(int(result[1]["book_id"]))
        else:
            return get_404_page()
            
if __name__ == "__main__":
    print("Server starting...")
    #server = HTTPServer(("0.0.0.0", 8000), WebRequestHandler)
    server = HTTPServer(("localhost", 8000), WebRequestHandler)
    server.serve_forever()
