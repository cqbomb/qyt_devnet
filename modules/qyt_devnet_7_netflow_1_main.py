#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

import logging
import sys
import socketserver
from qyt_devnet_7_netflow_0_collector import ExportPacket

logging.getLogger().setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(message)s')
ch.setFormatter(formatter)
logging.getLogger().addHandler(ch)


class SoftflowUDPHandler(socketserver.BaseRequestHandler):
    # We need to save the templates our NetFlow device
    # send over time. Templates are not resended every
    # time a flow is sent to the collector.
    TEMPLATES = {}

    @classmethod
    def get_server(cls, host, port):
        logging.info("Listening on interface {}:{}".format(host, port))
        server = socketserver.UDPServer((host, port), cls)
        return server

    def handle(self):
        data = self.request[0]
        host = self.client_address[0]
        s = "Received data from {}, length {}".format(host, len(data))
        logging.debug(s)
        # 使用类ExportPacket处理数据,并返回实例export,这是整个处理的开始!
        export = ExportPacket(data, self.TEMPLATES)
        # 把实例export(类ExportPacket)中的属性templates更新到类SoftflowUDPHandler的属性templates,用于保存模板数据
        self.TEMPLATES.update(export.templates)
        s = "Processed ExportPacket with {} flows.".format(export.header.count)
        logging.debug(s)


if __name__ == "__main__":
    # createdb()
    server = SoftflowUDPHandler.get_server('0.0.0.0', 9999)

    logging.getLogger().setLevel(logging.DEBUG)

    try:
        logging.debug("Starting the NetFlow listener")
        server.serve_forever(poll_interval=0.5)
    except (IOError, SystemExit):
        raise
    except KeyboardInterrupt:
        raise
