#!/usr/bin/env python3
# vim: set fileencoding=utf-8 :
""" http_client_test.py

    Tests for simple http dummy client"""

# Standard library imports:
import os
import tempfile
import time
import unittest

# Own imports:
import http_server_mock
import http_client


class TestExample(unittest.TestCase):
    '''Test examples'''

    def __init__(self, *args, **kwargs):
        self.http_server = None
        self.port = None
        super().__init__(*args, **kwargs)

    def start_server(self, folder):
        '''Starts the mock server for the given folder'''
        self.http_server = http_server_mock.HttpServer(folder)
        self.http_server.start()
        self.port = self.http_server.port
        print(f"Port: {self.port}")

    def tearDown(self):
        self.http_server.stop()
        self.http_server = None

    def test_fetch_file_over_http(self):
        '''Test fetch_file_over_http'''
        testfolder = os.path.join(os.path.dirname(__file__), "testfolder")
        self.start_server(testfolder)
        url = f"http://localhost:{self.port}/test1.txt"
        with tempfile.NamedTemporaryFile(delete=False) as file_:
            downloaded_file = file_.name

        http_client.fetch_file_over_http(url, downloaded_file)

        with open(downloaded_file, "r") as file_:
            line = file_.readline().strip()
            self.assertEqual("test1", line)

        os.unlink(downloaded_file)

    def test_fetch_file_over_http2(self):
        '''Test fetch_file_over_http'''
        testfolder = os.path.join(os.path.dirname(__file__), "testfolder")
        self.start_server(testfolder)
        url = f"http://localhost:{self.port}/test2.txt"

        with tempfile.NamedTemporaryFile(delete=False) as file_:
            downloaded_file = file_.name

        http_client.fetch_file_over_http(url, downloaded_file)

        with open(downloaded_file, "r") as file_:
            line = file_.readline().strip()
            self.assertEqual("test2", line)

        os.unlink(downloaded_file)


if __name__ == '__main__':
    unittest.main()
