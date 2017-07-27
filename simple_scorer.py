#!/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer
import sys
from base64 import b64decode
from urllib.parse import unquote

from leaderboard import LeaderBoard

lb = None
tokens = None


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)

        self.send_header('Content-type', 'text/html')
        self.end_headers()

        message = "Please use POST request to send your submission."
        self.wfile.write(message)

    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Test\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        auth = self.headers['Authorization']

        if auth is None:
            self.do_AUTHHEAD()
            self.wfile.write(bytes('no auth header received', encoding="utf-8"))
        elif auth.split()[0] == 'Basic':
            auth_token = str(b64decode(auth.split()[1]), encoding="utf-8").split(":")[1].lower()
            if auth_token not in tokens:
                self.do_AUTHHEAD()
                self.wfile.write(bytes('not authenticated', encoding="utf-8"))
            content_length = int(self.headers['Content-Length'])
            post_data = unquote(str(self.rfile.read(content_length), encoding="utf-8"))
            is_valid, scoring = lb.score(post_data.split("\n"))
            if is_valid:
                if tokens[auth_token] > 0:
                    tokens[auth_token] -= 1
                    self.wfile.write(bytes(scoring, encoding="utf-8"))
                else:
                    self.wfile.write(bytes('too many tries', encoding="utf-8"))
            else:
                self.wfile.write(bytes(scoring, encoding="utf-8"))
        else:
            self.do_AUTHHEAD()
            self.wfile.write(bytes('not authenticated', encoding="utf-8"))


def run():
    print('starting server...')

    if len(sys.argv) != 2:
        print("Usage: simple_scorer.py <data.json>", file=sys.stderr)
        exit(1)

    global lb
    with open(sys.argv[1], "rt") as f:
        lb = LeaderBoard(f.read())

    global tokens
    with open("allowed_tokens.txt", "rt") as f:
        tokens = {}
        for line in f:
            tokens[line.strip().lower()] = 10
    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http server, you need root access
    server_address = ('127.0.0.1', 8081)
    httpd = HTTPServer(server_address, RequestHandler)
    print('running server...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
