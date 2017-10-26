import SimpleHTTPServer
import SocketServer
import os
import sys
import threading
from random import choice


extension_to_content_type = {
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "png": "image/png",
    "gif": "image/gif"
}


def content_type(filename):
    return extension_to_content_type[filename[filename.rfind(".") + 1:].lower()]


def is_image(filename):
    return filename[filename.rfind(".") + 1:] in extension_to_content_type


def random_image(directory):
    images = [image for image in os.listdir(directory) if is_image(image)]
    return directory + os.sep + choice(images)


class MyHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        self.path_to_image = random_image(os.path.dirname(sys.argv[0]) + os.sep + 'resources')
        statinfo = os.stat(self.path_to_image)
        self.image_size = statinfo.st_size
        self.content_type = content_type(self.path_to_image)
        SimpleHTTPServer.SimpleHTTPRequestHandler.__init__(self, request, client_address, server)

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", self.content_type)
        self.send_header("Content-length", self.image_size)
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", self.content_type)
        self.send_header("Content-length", self.image_size)
        self.end_headers()
        f = open(self.path_to_image, 'rb')
        self.wfile.write(f.read())
        f.close()


class MyServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    def __init__(self, server_address, RequestHandlerClass):
        self.allow_reuse_address = True
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass, False)


if __name__ == "__main__":
    host, port = "0.0.0.0", 8070
    print 'Starting img-panda...'
    img_panda = MyServer((host, port), MyHandler)
    img_panda.server_bind()
    img_panda.server_activate()
    server_thread = threading.Thread(target=img_panda.serve_forever())
    server_thread.start()
