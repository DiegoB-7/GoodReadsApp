from jinja2 import Template
from modules import search_book

def get_404_page():
    jinja_template = open("templates/404.html").read()
    template = Template(jinja_template)
    html_content = template.render()
    
    return html_content

def get_index(query_search:str):
    
    jinja_template = open("templates/index.html").read()
    template = Template(jinja_template)
    books = search_book(query_search)
    html_content = template.render(books=books)
    
    return html_content


