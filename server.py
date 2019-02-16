#!/usr/bin/env python3
import sys, os, socket
from socketserver import ThreadingMixIn
from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl
import json
import datetime
import uuid

HOST = socket.gethostname()

from database import CPDatabase

cp_database = CPDatabase()

class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        # pick apart request
        print(self.request)
        self.send_response(200)
        self.send_header("Content-Type","application/json")
        self.end_headers()
        payload = {
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "Test Text",
                    "playBehavior": "REPLACE_ENQUEUED"
                },
                "shouldEndSession": true
            }
        }
        Reelf.wfile.write(json.dumps(payload).encode())

class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass

def main():
    '''
    This sets the listening port, default port 8080
    '''
    if sys.argv[1:]:
        PORT = int(sys.argv[1])
    else:
        PORT = 8080

    '''
    This sets the working directory of the HTTPServer, defaults to directory where script is executed.
    '''
    if sys.argv[2:]:
        os.chdir(sys.argv[2])
        CWD = sys.argv[2]
    else:
        CWD = os.getcwd()

    cp_database.get_update()
    server = ThreadingSimpleServer(('0.0.0.0', PORT), Handler)
    print("Serving HTTP traffic from", CWD, "on", HOST, "using port", PORT)
    server.socket = ssl.wrap_socket(server.socket, keyfile="./key.pem", certfile="./cert.pem", server_side=True)
    try:
        while 1:
            sys.stdout.flush()
            server.handle_request()
    except KeyboardInterrupt:
        print("\nShutting down server per users request.")

if __name__ == "__main__":
    main()
