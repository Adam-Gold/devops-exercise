from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

post_counter = 0


def increment_counter():
    global post_counter
    post_counter += 1


class MyServer(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write("<html><body><h1>amount of POST requests: %s</h1></body></html>" % post_counter)

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        self._set_headers()
        self.wfile.write("<html><body><h1>POST!</h1></body></html>")
        increment_counter()


def run(server_class=HTTPServer, handler_class=MyServer, port=8090):
    server_address = ('0.0.0.0', port)
    smart_panda = server_class(server_address, handler_class)
    print 'Starting smart-panda...'
    smart_panda.serve_forever()


if __name__ == "__main__":
    run()
