---
title: RabbitMQ
tags: 
  - RabbitMQ
categories: 
  - RabbitMQ
description: RabbitMQ, httpapi
date: 2019-11-25 14:32:34
updated: 2019-11-25 14:32:34
---

## Demo

```py
# -*- coding: utf8 -*-
"""
RabbitMQ 操作
"""
import pika
import time
import threading
from tools import estools
from tools.eslogging import *


class EsPublish(object):
    """生产者"""

    def __init__(self):
        self.cfg = estools.get_cfg()
        self.rm_cfg = self.cfg['rabbitmq']
        credentials = pika.PlainCredentials(self.rm_cfg['user'], self.rm_cfg['password'])
        self.conn_param = pika.ConnectionParameters(
            host=self.rm_cfg['ip'], port=int(self.rm_cfg['port']),
            virtual_host='/', credentials=credentials, heartbeat=60)
        self.connection = None
        self.channel = None
        self.queue_declare = None

    def blocking_connect(self):
        self.connection = pika.BlockingConnection(self.conn_param)
        self.channel = self.connection.channel()

    def check_queue(self, queue, exchange):
        # 声明一个持久队列
        self.queue_declare = self.channel.queue_declare(queue=queue, durable=True)
        self.channel.confirm_delivery()
        # 声明一个持久交换机
        self.channel.exchange_declare(exchange=exchange, exchange_type="direct", durable=True)
        self.channel.queue_bind(queue=queue, exchange=exchange, routing_key=queue)

    def get_length(self, queue=None, exchange=None):
        if self.queue_declare is None:
            self.check_queue(queue, exchange)
        else:
            if self.queue_declare.method.queue != queue:
                self.check_queue(queue, exchange)
        return self.queue_declare.method.message_count

    def send(self, queue, exchange, body):
        # 发布一条数据 - 到指定交换机
        return self.channel.basic_publish(exchange=exchange, routing_key=queue, body=body, mandatory=True)

    def close(self):
        self.connection.close()


class EsConsume(EsPublish):
    def __init__(self, name, callback):
        """
        :type name: str
        :param callback
        """
        super(EsConsume, self).__init__()
        self.name = name
        self.cb = callback

    def on_consume(self, channel, method, properties, body):
        """消息回调"""
        if self.cb(channel, method, properties, body):
            # 消息完成标记
            channel.basic_ack(method.delivery_tag)

    def basic_consume(self, auto_stop=0):
        # 每次消费1条消息 - 多消费者时, 避免某个消费者一次性获取太多消息
        self.channel.basic_qos(prefetch_count=1)
        # 消费者标签: consumer_test - 用于明确关闭消费者
        try:
            self.channel.basic_consume(self.on_consume, queue=self.name, no_ack=False,
                                       consumer_tag='consumer_%s' % self.name)
        except TypeError:
            self.channel.basic_consume(queue=self.name, on_message_callback=self.on_consume, auto_ack=False,
                                       consumer_tag='consumer_%s' % self.name)
        if auto_stop > 0:
            tee = threading.Thread(target=self.thread_stop_consume, args=(auto_stop,))
            tee.setDaemon(True)  # 设置跟随父线程
            tee.start()
        self.channel.start_consuming()

    def stop_consume(self):
        self.channel.stop_consuming(consumer_tag='consumer_%s' % self.name)

    def thread_stop_consume(self, auto_stop):
        time.sleep(auto_stop)
        eslogger.info("auto stop: %s" % auto_stop)
        self.channel.stop_consuming(consumer_tag='consumer_%s' % self.name)


if __name__ == '__main__':
    configlogging()
    t = EsPublish()
    t.blocking_connect()
    # t.check_queue('olcustomer', 'shengyibao')
    print t.get_length('olcustomer', 'shengyibao')
    print t.get_length('funit', 'shengyibao')
    # t.send()
    t.close()

```
