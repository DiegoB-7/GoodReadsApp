import requests 
from bs4 import BeautifulSoup
from jinja2 import Template  # Jinja2 template engine
import redis  # Redis client library

# Base URL for Goodreads
url:str = "https://www.goodreads.com"

# Connect to Redis database
db = redis.StrictRedis(host="localhost", port=6379, db=0)

def load_books():
    """
    Fetches book data from Goodreads and saves it to a Redis database.
    """
    # Send a GET request to the Goodreads URL containing the list of recent hit books
    response = requests.get(url+"/blog/show/2743-hot-new-81-very-recent-hit-books-across-genres?ref=RecentHits_eb")
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all elements with attribute 'data-resource-type="Book"'
        book_elements = soup.find_all(attrs={"data-resource-type": "Book"})
        
        # Counter to keep track of fetched books
        book_count = 0
        for element in book_elements:
            # Extract the 'href' attribute from the 'a' element
            href = element.find('a')['href']
            
            # Concatenate the 'href' with the base URL
            full_url = url + href
            
            # Send a GET request to the concatenated URL
            book_response = requests.get(full_url)
            
            # Check if the request was successful (status code 200)
            if book_response.status_code == 200:
                # Parse the HTML content of the book page
                book_soup = BeautifulSoup(book_response.content, 'html.parser')
                
                # Extract relevant book information
                autor = book_soup.find(class_='ContributorLink__name')
                image = book_soup.find(class_='ResponsiveImage')
                description = book_soup.find(class_='Formatted')
                title = book_soup.find(class_='Text Text__title1')
                book_id = href.split("/")[3]  # Extract book ID from URL
                
                # Save the book data to the Redis database
                save_book(title.text, description.text, autor.text, image['src'], book_id)
            else:
                print("Failed to fetch URL:", full_url)
            
            # Increment book counter and print status
            book_count += 1
            print(f"Book {book_count} fetched")
   
def save_book(title:str, description:str, autor:str, image:str, book_id:str):
    """
    Saves book data to a Redis database.
    
    Parameters:
    - title: Title of the book
    - description: Description of the book
    - autor: Author of the book
    - image: URL of the book cover image
    - book_id: ID of the book
    """
    # Read the Jinja2 template for book HTML content
    jinja_template = open("templates/book_template.html").read()
    
    # Create a Jinja2 template object
    template = Template(jinja_template)
    
    # Render the HTML content using the template and book data
    html_content = template.render(title=title, description=description, autor=f"By {autor}", image=image)
    
    book_id = book_id.split("-")[0]  # Extract book ID from URL (remove the '-' and the rest of the URL)
    # Save the HTML content to the Redis database with the book ID as the key
    db.set(book_id, html_content)
    
    # Store title and book ID mapping
    db.set(f"title:{title.lower()}", book_id)
    
    # Store book ID under the author's key
    # If the key already exists, add the book ID to the set
    db.sadd(f"author:{autor.lower()}", book_id)

load_books()