#!/usr/bin/python3
import tornado.netutil
import tornado.options
import tornado.process
from tornado.httpserver import HTTPServer
import tornado.ioloop
from tornado.options import options

import controllers.bugs

from app.application import Application


def main():
    tornado.options.parse_command_line()
    app = Application()
    app.load()
    server = HTTPServer(app)
    server.listen(3000, '127.0.1.4')
    tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
    main()