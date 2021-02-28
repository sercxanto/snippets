#!/usr/bin/env python3
# vim: set fileencoding=utf-8 :
""" mocked_http_server.py

    Simple http server mock"""

# The MIT License (MIT)
#
# Copyright (c) 2021 Georg Lutz
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


# Standard library imports:
import http.server
import multiprocessing
import os
import socketserver
import time


class HttpServer():
    '''Simple http server'''

    def __init__(self, folder):
        self.port = 0
        self.process = None
        self.folder = folder

    def _runner(self):
        '''Starts the http server'''
        server_address = ('localhost', self.port)
        server_class = http.server.HTTPServer
        os.chdir(self.folder)
        handler_class = http.server.SimpleHTTPRequestHandler
        httpd = server_class(server_address, handler_class)
        httpd.serve_forever()

    def start(self):
        '''Starts the http server in a background process'''

        with socketserver.TCPServer(("localhost", 0), None) as server:
            self.port = server.server_address[1]
        self.process = multiprocessing.Process(target=self._runner, args=())
        self.process.start()
        # Sleep a bit to make sure port is actually served
        time.sleep(0.1)

    def stop(self):
        '''Stops the http background server'''
        self.process.terminate()
        self.process = None
        self.port = 0


def main():
    '''main function, called when script file is executed directly'''

    duration = 60
    my_server = HttpServer("/")
    my_server.start()
    print("Server running on port {} start for {}s".format(my_server.port, duration))
    time.sleep(duration)
    print("stop now")
    my_server.stop()


if __name__ == "__main__":
    main()
