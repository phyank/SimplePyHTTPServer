# SimplePyHTTPServer

This is a simple http server for personal use. It enriched the http.server in the standard library so that we can quickly create dynamic web pages with multiple types of files in the way we work with django. 
Actually, The key to make use of the http.server in Py3 is to customize the BaseHTTPRequestHandler.This project is an example of this.
It has successfully served Web-GUI at localhost in a project: https://github.com/phyank/LuckyParis 

features:
1.Pure Python: This is a simple HTTP server based on Python 3.x standard library. 
2.Lightweight: It can serve dynamic pages, multiple types of files ,and deal with AJAX interaction, with only 300+ lines of codes. 
3.Django-like: It is quite like django so that we can easily use it: Pages are described as a function, and the implement of HTTP response are object-oriented.

The customization of BaseHTTPRequestHandler is in server.py
To create a dynamic page, see views.py, which is implemented in django-style.
