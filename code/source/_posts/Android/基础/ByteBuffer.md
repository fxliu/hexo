---
title: ByteBuffer
tags: 
    - ByteBuffer
categories: 
    - Android
description: ByteBuffer
date: 2022-07-23 13:47:18
updated: 2022-07-23 13:47:18
---

## 基础属性

```java
position  // 当前读取的位置。
mark      // 为某一读过的位置做标记，便于某些时候回退到该位置。
capacity  // 初始化时候的容量。
limit     // limit一般和capacity相等，代表可读写上线。
```

```java
ByteBuffer allocate(int capacity) //创建一个指定capacity的ByteBuffer。
ByteBuffer allocateDirect(int capacity) //创建一个direct的ByteBuffer，这样的ByteBuffer在参与IO操作时性能会更好
// wrap：地址引用
ByteBuffer wrap(byte [] array)
ByteBuffer wrap(byte [] array, int offset, int length)
// get: 从ByteBuffer中读取
// put: 写入到ByteBuffer
```

```java
clear()   把position设为0，把limit设为capacity，一般在把数据写入Buffer前调用。
flip()    把limit设为当前position，把position设为0，一般在从Buffer读出数据前调用。
rewind()  把position设为0，limit不变，一般在把数据重写入Buffer前调用。
compact() 将position与limit之间的数据复制到buffer的开始位置
mark() & reset()     通过调用Buffer.mark()方法，可以标记Buffer中的一个特定position。之后可以通过调用Buffer.reset()方法恢复到这个position。
          未标记mark，不能调用reset，会触发异常
```

```java
ByteBuffer.remaining()  此方法最给力，返回剩余可读长度
```

## 基础转换

```java
// byte[] -> ByteBuffer
ByteBuffer buffer=ByteBuffer.allocate(bytes.length);
buffer.put(bytes);
buffer.put(bytes, 0, 10);   // bytes从0开始提取10个字节写入到buffer
// ByteBuffer -> byte[]
byte[] bytes = new byte[byteBuffer.remaining()];
byteBuffer.get(bytes);
byteBuffer.get(bytes, 0, 10);// 提取10个字节到bytes的0位置
```


