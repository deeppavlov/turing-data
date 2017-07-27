#!/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer


# HTTPRequestHandler class
class RequestHandler(BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Send message back to client
        message = "Please use POST request to send your submission."
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))

    def do_POST(self):
        # Doesn't do anything with posted data
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself
        self.wfile.write("<html><body><h1>POST!</h1></body></html>")


def run():
    print('starting server...')

    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http server, you need root access
    server_address = ('127.0.0.1', 8081)
    httpd = HTTPServer(server_address, RequestHandler)
    print('running server...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
