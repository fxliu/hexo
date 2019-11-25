---
title: RabbitMQ
tags: 
  - RabbitMQ
  - httpapi
categories: 
  - RabbitMQ
description: RabbitMQ, httpapi
date: 2019-11-23 15:41:11
updated: 2019-11-23 15:41:11
---

## HTTP API

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
