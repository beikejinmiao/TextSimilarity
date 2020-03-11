#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import threading
import traceback
import socketserver
from libs.logger import get_logger


logger = get_logger(_file_=__file__)


socket_host = "127.0.0.1"
socket_port = 8989
socketserver.TCPServer.allow_reuse_address = True


class Server(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class RequestHandler(socketserver.StreamRequestHandler):
    def handle(self):
        while True:
            results = list()
            rcv_data = ""
            try:
                rcv_data = self.request.recv(32768).strip("\r\n ")
                if rcv_data:
                    data = json.loads(rcv_data)
                    results = {}
            except ValueError as e:
                logger.warning("ValueError: '%s' for received data '%s'" % (e, rcv_data))
            except:
                logger.error("Exception: {0}".format(traceback.format_exc()))
                logger.error("Data that has received is: {0}".format(rcv_data))
            finally:
                try:
                    self.request.sendall(json.dumps(results))
                except:
                    logger.warning(traceback.format_exc())
                    break       # 向客户端发送数据出问题，可能客户端已主动断开连接，须释放该连接


class ThreadServer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        server = Server((socket_host, socket_port), RequestHandler)
        server.serve_forever()

