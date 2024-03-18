from jinja2 import Template
from modules import (search_book,get_books_from_session,get_all_keys,get_book_preview)
import random

def get_404_page():
    jinja_template = open("templates/404.html").read()
    template = Template(jinja_template)
    html_content = template.render()
    
    return html_content

def get_index(query_search:str, session_id:str = ""):
    jinja_template = open("templates/index.html").read()
    template = Template(jinja_template)
    books = search_book(query_search)
    visited_books = get_books_from_session(session_id)
    recomended_book = None
    
    if(len(visited_books) >= 3):
        books_list = get_all_keys()
        while True:
            random_book = random.choice(books_list).decode('utf-8')
            if not random_book.startswith('author:') and not random_book.startswith('title:') and not random_book.startswith('session:') and not random_book in visited_books:
                recomended_book = get_book_preview(random_book)
                break
            
    html_content = template.render(books=books,visited_books=visited_books,recomended_book=recomended_book)
    
    return html_content


