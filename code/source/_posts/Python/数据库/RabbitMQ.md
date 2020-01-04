---
title: RabbitMQ
tags: 
  - RabbitMQ
categories: 
  - Python
description: RabbitMQ
date: 2019-11-11 14:27:12
updated: 2020-01-04 17:09:24
---

## 封装

### 封装-生产者

```py
# -*- coding: utf8 -*-
"""
RabbitMQ 生产者
"""
import pika
import time
import threading


class EsPublish(object):
    """生产者"""
    def __init__(self, db):
        self.cfg = db
        credentials = pika.PlainCredentials(self.cfg['user'], self.cfg['password'])
        self.conn_param = pika.ConnectionParameters(
            host=self.cfg['ip'], port=int(self.cfg['port']),
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

    def get_length(self, queue=None):
        if queue is None:
            return self.queue_declare.method.message_count
        if self.queue_declare and (queue == self.queue_declare.method.queue):
            return self.queue_declare.method.message_count
        queue_declare = self.channel.queue_declare(queue=queue, durable=True)
        return queue_declare.method.message_count

    def send(self, queue, exchange, body):
        # 发布一条数据 - 到指定交换机
        return self.channel.basic_publish(exchange=exchange, routing_key=queue, body=body, mandatory=True)

    def close(self):
        self.connection.close()


class EsConsume(EsPublish):
    def __init__(self, db, queue, callback):
        """消费者"""
        super(EsConsume, self).__init__(db)
        self.queue = queue
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
            self.channel.basic_consume(self.on_consume, queue=self.queue, no_ack=False,
                                       consumer_tag='consumer_%s' % self.queue)
        except TypeError:
            self.channel.basic_consume(queue=self.queue, on_message_callback=self.on_consume, auto_ack=False,
                                       consumer_tag='consumer_%s' % self.queue)
        if auto_stop > 0:
            tee = threading.Thread(target=self.thread_stop_consume, args=(auto_stop,))
            tee.setDaemon(True)  # 设置跟随父线程
            tee.start()
        self.channel.start_consuming()

    def stop_consume(self):
        self.channel.stop_consuming(consumer_tag='consumer_%s' % self.queue)

    def thread_stop_consume(self, auto_stop):
        while auto_stop > 0:
            time.sleep(1)
            auto_stop -= 1
        self.channel.stop_consuming(consumer_tag='consumer_%s' % self.queue)


def test():
    db = {
        'ip': '127.0.0.1',
        'port': '5672',
        'user': 'user',
        'password': 'password',
    }
    t = EsPublish(db)
    t.blocking_connect()
    t.check_queue('test_queue', 'test_exchange')
    t.send('test_queue', 'test_exchange', 'test_value')
    print t.get_length()
    t.close()


if __name__ == '__main__':
    test()

```

### 封装-消费者

```py
# -*- coding: utf8 -*-
"""
rabbitmq 消费者
"""
import json
import time
from test_rabbitmq_publish import EsConsume


class RabbitMQRead(object):
    def __init__(self, db, queue, exchange):
        self.queue = queue
        self.exchange = exchange
        self.time_start = int(time.time())
        self.rabbitmq = EsConsume(db, queue=queue, callback=self.on_consume)
        self.auto_stop = 3600*6      # 每6h, 重启一次

    def on_consume(self, channel, method, properties, body):
        """消息回调：重写此函数即可"""
        # print channel, method, properties
        print body
        # 处理完成后一定要返回True，标记消息处理完成
        return True

    def connect(self):
        self.rabbitmq.blocking_connect()
        self.rabbitmq.check_queue(self.queue, self.exchange)
        return self.rabbitmq.get_length(self.queue)

    def start(self):
        self.rabbitmq.basic_consume(self.auto_stop)


def test():
    db = {
        'ip': '127.0.0.1',
        'port': '5672',
        'user': 'user',
        'password': 'password',
    }
    rr = RabbitMQRead(db, 'test_queue', 'test_exchange')
    rr.auto_stop = 3
    rr.connect()
    rr.start()


if __name__ == '__main__':
    test()

```

### HTTPAPI

```py

# coding=utf8
"""
RabbitMQ
无效队列: RabbitMQ 会自动清理长时间不使用的队列
    猜测：所谓的持久队列仅仅是数据持久，如果队列无数据且无消费者/生产者，还是会被自动清理掉的
"""
import requests
import json
import datetime


class RabbitMQHttp:
    def __init__(self):
        self.host = 'http://127.0.0.1:15672'
        self.auth = ('***', '***')

    def request_api(self, name):
        r = requests.get(self.host + '/api/' + name, auth=self.auth)
        return json.loads(r.content)

    def request_vhosts(self):
        return self.request_api('vhosts')

    def request_queues(self):
        return self.request_api('queues')

    def request_connections(self):
        return self.request_api('connections')


class EsClear:
    def __init__(self):
        self.rh = RabbitMQHttp()

    def get_invalid_queues(self):
        d = datetime.datetime.now() - datetime.timedelta(days=1)
        d = d.strftime('%Y-%m-%d %H:%M:%S')
        queues = self.rh.request_queues()
        re = []
        for q in queues:
            # 自动清理的越过
            if q['auto_delete']:
                # print 'auto_delete', q
                continue
            # 存在消费者的越过
            if q['consumers'] > 0:
                # print 'consumers: name=%(name)s, consumers=%(consumers)s, messages=%(messages)s' % q
                continue
            # 最近使用过的越过
            if q['idle_since'] > d:
                print 'idle_since: name=%(name)s, idle_since=%(idle_since)s, messages=%(messages)s' % q
                continue
            re.append(q)
            print json.dumps(q, sort_keys=True, indent=4)
        return re


if __name__ == '__main__':
    ec = EsClear()
    ec.get_invalid_queues()

```
