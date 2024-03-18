import re
import redis
from jinja2 import Template
from bs4 import BeautifulSoup

db = redis.StrictRedis(host="localhost", port=6379, db=0)

def add_book_to_session(session_id: str, book_id: int):
    # Add a new book ID to the list stored in the Redis hash
    db.sadd(f"session:{session_id}", book_id)
     
def get_all_keys():
    keys = db.keys()
    return keys

def get_books_from_session(session_id: str):
    # Get the list of book IDs stored in the Redis hash
    book_ids = db.smembers(f"session:{session_id}")
    books = []
     
    for book_id in book_ids:
        tmp_book = get_book_preview(int(book_id))
        books.append(tmp_book)
    
    return books

def get_book_page(id:int):
    html = db.get(id)
    return html.decode("utf-8")
  
def get_path_formated(url:str):
    mapping = [
            (r'^/Book/(?P<book_id>\d+)$', 'get_book_page'),
            (r'^/(?:(?:\?.*)?)?$', 'get_index')   
    ]
    
    for pattern, method in mapping:
            match = re.match(pattern, url)
            if match:
                return (method, match.groupdict())
            
def search_book(query:str):
    books = []
    query = query.lower()
    
    # Check if the query is contained within the author or title
    for key in db.keys():
        key_str = key.decode('utf-8')
        if not key_str.startswith('author:') and not key_str.startswith('title:') and not key_str.startswith('session:'):
            # Get the book details using the key
            tmp_book = get_book_preview(key_str)
            
            # Check if the query is contained in the author or title
            if query in tmp_book['author'].lower() or query in tmp_book['title'].lower():
                books.append(tmp_book)
    
    return books

      
def get_book_preview(bookID:int):
  html = db.get(bookID)
  soup = BeautifulSoup(html, 'html.parser')
  
  # Extracting the image
  image_src = soup.find('img')['src']
  # Extracting the title
  title = soup.find('h1').text
  # Extracting the author
  author = soup.find('p', class_='text-gray-500').text
  
  return {"title": title, "author": author, "image": image_src,"id": bookID}
  
  