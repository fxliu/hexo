---
title: HTTP
tags: 
  - HTTP
categories: 
  - QT
description: HTTP
date: 2020-09-30 09:28:48
updated: 2020-09-30 09:28:48
---

### HTTP

```c++
#include <QNetworkAccessManager>
#include <QNetworkRequest>
#include <QNetworkReply>
#include <QSslError>
#include <QStringList>
#include <QTimer>
#include <QUrl>

QNetworkAccessManager m_accessManager;

QObject::connect(&m_accessManager, SIGNAL(finished(QNetworkReply*)), this, SLOT(finishedSlot(QNetworkReply*)));
QNetworkRequest* request = new QNetworkRequest();

// QSslConfiguration config = request->sslConfiguration();

request->setUrl(QUrl("http://t.dnndo.com/eid_tcp_server/post_lfx_test.php?reqID=C18ABF3F2518080100000241F&machine=123"));
m_accessManager.get(*request);
qDebug() << "QNetworkRequest:-----------------------------------------";

void ******::finishedSlot(QNetworkReply* reply)
{
    if (reply->error() == QNetworkReply::NoError)
    {
        qDebug() << "-----------------------------------------";
        QByteArray bytes = reply->readAll();
        qDebug() << bytes;
        qDebug() << "-----------------------------------------";
    }
    else
    {
        qDebug() << "-----------------------------------------";
        qDebug() << "handle errors here";
        QVariant statusCodeV = reply->attribute(QNetworkRequest::HttpStatusCodeAttribute);
        //statusCodeV是HTTP服务器的相应码，reply->error()是Qt定义的错误码，可以参考QT的文档
        qDebug("found error ....code: %d %d\n", statusCodeV.toInt(), (int)reply->error());
        qDebug(qPrintable(reply->errorString()));
        qDebug() << "-----------------------------------------";
    }
    reply->deleteLater();
}
```
