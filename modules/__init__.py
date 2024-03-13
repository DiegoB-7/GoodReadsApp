import re
import redis

db = redis.StrictRedis(host="localhost", port=6379, db=0)

def get_path_formated(url:str):
    if(url == "/favicon.ico"):
        return ("/favicon.ico", {})
    mapping = [
            (r'^/Book/(?P<book_id>\d+)$', 'get_book_page'),
            (r'^/$', 'get_index')   
    ]
    
    for pattern, method in mapping:
            match = re.match(pattern, url)
            if match:
                
                return (method, match.groupdict())
            
    
def get_book_page(id:int):
    html = db.get(id)
    return html.decode("utf-8")

def get_index():
    html = """
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.tailwindcss.com"></script>
        <link rel="stylesheet" href="https://unpkg.com/aos@next/dist/aos.css" />
        <title>Home</title>
    </head>

    <body>

        <div class="flex flex-col min-h-screen">
            <header class="flex items-center h-[60px] border-b px-4 sm:px-6">
                <div class="flex items-center gap-4" data-aos="fade-down"><a class="flex items-center gap-2 font-semibold" href="#" ><svg
                            class="h-10 w-10" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
                            height="800px" width="800px" version="1.1" id="Icons" viewBox="0 0 32 32" xml:space="preserve">

                            <path
                                d="M28.9,9.4C28.9,9.4,28.9,9.4,28.9,9.4C28.9,9.3,29,9.2,29,9.1c0,0,0,0,0-0.1c0,0,0,0,0-0.1c0-0.1,0-0.2,0-0.3c0,0,0,0,0-0.1  c0-0.1-0.1-0.2-0.1-0.3c0,0,0,0,0,0c-0.1-0.1-0.1-0.1-0.2-0.2l-11-7c-0.3-0.2-0.8-0.2-1.1,0l-13,9c0,0-0.1,0.1-0.1,0.1  c0,0,0,0-0.1,0c-0.1,0.1-0.1,0.2-0.2,0.3c0,0,0,0,0,0.1C3,10.8,3,10.9,3,11c0,0,0,0,0,0v6v6c0,0.3,0.2,0.7,0.5,0.8l11,7  c0.2,0.1,0.4,0.2,0.5,0.2c0.2,0,0.4-0.1,0.6-0.2l13-9c0.2-0.2,0.4-0.4,0.4-0.7s-0.1-0.6-0.3-0.8c-0.9-0.9-1.1-2.2-0.5-3.4l0.7-1.5  c0-0.1,0.1-0.2,0.1-0.3c0,0,0-0.1,0-0.1c0,0,0,0,0,0c0-0.1,0-0.3-0.1-0.4c0,0,0-0.1,0-0.1c0-0.1-0.1-0.2-0.2-0.3c0,0,0,0,0,0  c-0.9-0.9-1.1-2.2-0.5-3.4L28.9,9.4z M26.6,14.8l-11.6,8L5,16.5v-3.6l9.5,6c0.2,0.1,0.4,0.2,0.5,0.2c0.2,0,0.4-0.1,0.6-0.2l10.3-7.1  C25.8,12.8,26,13.8,26.6,14.8z M15,28.8L5,22.5v-3.6l9.5,6c0.2,0.1,0.4,0.2,0.5,0.2c0.2,0,0.4-0.1,0.6-0.2l10.3-7.1  c-0.1,1.1,0.1,2.2,0.7,3.1L15,28.8z" />
                        </svg><span class="sr-only">Home</span></a>
                    <nav class="hidden items-center gap-4 font-bold text-sm lg:flex">好本书</nav>
                </div>

            </header>
            <main class="flex-1">
                <section class="py-12 md:py-16 xl:py-24">
                    <div class="container px-4 grid gap-6 md:gap-8 lg:gap-10" data-aos="fade-down">
                        <div class="space-y-2">
                            <h1 class="text-4xl font-bold tracking-tighter sm:text-5xl">
                                Discover new books
                            </h1>
                            <p data-aos="fade-down"
                                class="max-w-[900px] text-gray-500 md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed dark:text-gray-400">
                                Search our library of over 10,000 books. Enter a title, author,
                                or genre to get started.
                            </p>
                        </div>

                    </div>
                </section>
                <section class="bg-gray-100 py-12 lg:py-16 xl:py-24 dark:bg-gray-800">
                    <div class="container px-4 grid gap-6 md:gap-8 lg:gap-10">
                        <div class="grid gap-2 md:gap-4">
                            <h2 class="text-3xl font-bold tracking-tighter sm:text-4xl text-white">
                                Featured Books
                            </h2>
                            <p
                                class="max-w-[800px] text-gray-500 md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed dark:text-gray-400">
                                Handpicked by our team. These are the books everyone is
                                talking about.
                            </p>
                        </div>
                        <div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
                            <div class="flex flex-col rounded-lg overflow-hidden " data-aos="fade-down"><img
                                    src="https://m.media-amazon.com/images/I/414GhW3ZqML._SY445_SX342_.jpg" width="300"
                                    height="300" alt="Cover" class="aspect-[3/4]  object-cover object-center rounded-md">
                                <div class="p-4 flex-1">
                                    <h3 class="font-bold text-lg leading-none text-white">
                                        The Midnight Library
                                    </h3>
                                    <p class="text-sm text-gray-500">By Matt Haig</p>
                                </div>
                            </div>
                            <div class="flex flex-col rounded-lg overflow-hidden" data-aos="fade-down"><img
                                    src="https://m.media-amazon.com/images/I/414GhW3ZqML._SY445_SX342_.jpg" width="300"
                                    height="300" alt="Cover" class="aspect-[3/4]  object-cover object-center rounded-md">
                                <div class="p-4 flex-1">
                                    <h3 class="font-bold text-lg leading-none text-white">
                                        The Midnight Library
                                    </h3>
                                    <p class="text-sm text-gray-500">By Matt Haig</p>
                                </div>
                            </div>
                            <div class="flex flex-col rounded-lg overflow-hidden" data-aos="fade-down"><img
                                    src="https://m.media-amazon.com/images/I/414GhW3ZqML._SY445_SX342_.jpg" width="300"
                                    height="300" alt="Cover" class="aspect-[3/4]  object-cover object-center rounded-md">
                                <div class="p-4 flex-1">
                                    <h3 class="font-bold text-lg leading-none text-white">
                                        The Midnight Library
                                    </h3>
                                    <p class="text-sm text-gray-500">By Matt Haig</p>
                                </div>
                            </div>
                            <div class="flex flex-col rounded-lg overflow-hidden" data-aos="fade-down"><img
                                    src="https://m.media-amazon.com/images/I/414GhW3ZqML._SY445_SX342_.jpg" width="300"
                                    height="300" alt="Cover" class="aspect-[3/4]  object-cover object-center rounded-md">
                                <div class="p-4 flex-1">
                                    <h3 class="font-bold text-lg leading-none text-white">
                                        The Midnight Library
                                    </h3>
                                    <p class="text-sm text-gray-500">By Matt Haig</p>
                                </div>
                            </div>
                            <div class="flex flex-col rounded-lg overflow-hidden" data-aos="fade-down"><img
                                    src="https://m.media-amazon.com/images/I/414GhW3ZqML._SY445_SX342_.jpg" width="300"
                                    height="300" alt="Cover" class="aspect-[3/4]  object-cover object-center rounded-md">
                                <div class="p-4 flex-1">
                                    <h3 class="font-bold text-lg leading-none text-white">
                                        The Midnight Library
                                    </h3>
                                    <p class="text-sm text-gray-500">By Matt Haig</p>
                                </div>
                            </div>

                        </div>
                    </div>
                </section>
            </main>
        </div>
    </body>
    <script src="https://unpkg.com/aos@next/dist/aos.js"></script>
    <script>
        AOS.init();
    </script>

    </html>
    """
    
    return html

def get_index():
    html = """ 
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.tailwindcss.com"></script>
        <link rel="stylesheet" href="https://unpkg.com/aos@next/dist/aos.css" />
        <title>404 Error</title>
    </head>

    <body>
        <div class="flex items-center justify-center w-full min-h-[calc(100vh_-_theme(safeArea))_] text-center py-6" data-aos="fade-right">
            <div class="container flex flex-col items-center gap-3 px-4 text-center">
                <div class="space-y-2">
                    <h1 class="text-4xl font-bold tracking-tighter sm:text-5xl">
                        Oops! Page Not Found
                    </h1>
                    <p
                        class="max-w-[600px] text-gray-500 md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed dark:text-gray-400">
                        Sorry, the page you're looking for could not be found. Please
                        check the URL in the address bar and try again.
                    </p>
                </div>
                
            </div>
        </div>
    </body>
    <script src="https://unpkg.com/aos@next/dist/aos.js"></script>
    <script>
        AOS.init();
    </script>
    </html>
    """
    
    return html

def get_404_page():
    html = """ 
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.tailwindcss.com"></script>
        <link rel="stylesheet" href="https://unpkg.com/aos@next/dist/aos.css" />
        <title>404 Error</title>
    </head>

    <body>
        <div class="flex items-center justify-center w-full min-h-[calc(100vh_-_theme(safeArea))_] text-center py-6" data-aos="fade-right">
            <div class="container flex flex-col items-center gap-3 px-4 text-center">
                <div class="space-y-2">
                    <h1 class="text-4xl font-bold tracking-tighter sm:text-5xl">
                        Oops! Page Not Found
                    </h1>
                    <p
                        class="max-w-[600px] text-gray-500 md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed dark:text-gray-400">
                        Sorry, the page you're looking for could not be found. Please
                        check the URL in the address bar and try again.
                    </p>
                </div>
                
            </div>
        </div>
    </body>
    <script src="https://unpkg.com/aos@next/dist/aos.js"></script>
    <script>
        AOS.init();
    </script>
    </html>
    """
    
    return html