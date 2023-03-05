---
title: Tools
tags: 
    - Tools
categories: 
    - Android
description: Tools
date: 2022-08-15 11:47:07
updated: 2022-08-15 11:47:07
---

## 常用小工具

## 
```java
public class Tools {
    static public void sleep(long millis) {
        try {
            Thread.sleep(millis);
        } catch (InterruptedException ignored) {
        }
    }
}
```

## 单数据缓冲区 - 线程安全

```java
import java.util.concurrent.TimeUnit;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

/**
 * 单数据缓冲区 - 线程安全
 *
 * @param <E> 指定缓冲数据类型
 */

public abstract class EsSingleObject<E> {
    private final E buf;
    private volatile boolean empty;    // 有效数据标记
    private final Lock lock = new ReentrantLock();
    private final long lockTimeMs;

    public EsSingleObject(E e) {
        buf = e;
        empty = true;
        this.lockTimeMs = 10;
    }

    public EsSingleObject(E e, long lockTimeMs) {
        buf = e;
        empty = true;
        this.lockTimeMs = lockTimeMs;
    }

    /**
     * 数据处理
     */
    abstract public boolean copy(E src, E des);

    public boolean isEmpty() {
        return empty;
    }

    // ---------------------------------------------------------------------------------------------
    // 核心函数 - 确保线程安全
    // ---------------------------------------------------------------------------------------------
    public interface setImpl<SE> {
        boolean run(SE obj);
    }

    /**
     * 保存数据到缓冲区
     *
     * @param si 必须在回调中处理数据, 确保安全
     * @return 数据处理结果
     */
    public boolean set(setImpl<E> si, long waitTimeMs) {
        if (!empty)     // 前置判断, 优化逻辑
            return false;
        try {
            if (waitTimeMs == -1)
                lock.lock();
            else if (!lock.tryLock(waitTimeMs, TimeUnit.MILLISECONDS))
                return false;
            try {
                if (!empty)
                    return false;
                if (si.run(buf)) {
                    empty = false;
                    return true;
                }
            } finally {
                lock.unlock();
            }
            return true;
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        return false;
    }

    // 保存数据到缓冲区, 默认10ms
    public boolean set(setImpl<E> si) {
        return set(si, 10);
    }

    public interface getImpl<GE> {
        boolean run(GE bytes);
    }

    /**
     * 从缓冲区获取数据
     *
     * @param gi         必须在回调中处理数据, 确保安全
     * @param waitTimeMs 无数据时, 延迟等待时长
     * @return 数据处理结果
     */
    public boolean get(getImpl<E> gi, long waitTimeMs) {
        if (empty)     // 前置判断, 优化逻辑
            return false;
        try {
            if (waitTimeMs == -1)
                lock.lock();
            else if (!lock.tryLock(waitTimeMs, TimeUnit.MILLISECONDS))
                return false;
            try {
                if (empty)
                    return false;
                if (gi.run(buf)) {
                    empty = true;
                    return true;
                }
            } finally {
                lock.unlock();
            }
            return true;
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        return false;
    }

    public boolean get(getImpl<E> gi) {
        return get(gi, 10);
    }

    /**
     * 获取原始对象, 非安全, 谨慎使用
     *
     * @return 原始对象
     */
    public E getUnsafe() {
        return buf;
    }

    // ---------------------------------------------------------------------------------------------
    // 功能函数 - 数据处理
    // ---------------------------------------------------------------------------------------------

    /**
     * 复制 src 数据到缓冲区
     *
     * @param src 源数据
     * @return 是否复制成功, 若缓冲区已满, 认为失败
     */
    public boolean copyFrom(E src, long waitTimeMs) {
        return set(des -> copy(src, des), waitTimeMs);
    }

    public boolean copyFrom(E src) {
        return set(des -> copy(src, des), lockTimeMs);
    }

    /**
     * 复制缓冲区数据 到 目标对象
     *
     * @param des 目标对象
     * @return 是否复制成功, 若缓冲区为空, 认为失败
     */
    public boolean copyTo(E des, long waitTimeMs) {
        return get(src -> copy(src, des), waitTimeMs);
    }

    public boolean copyTo(E des) {
        return get(src -> copy(src, des), lockTimeMs);
    }

    /**
     * 对象拷贝
     *
     * @param srcSingleBytes 源数据
     * @return 是否复制成功
     */
    public boolean copyFrom(EsSingleObject<E> srcSingleBytes, long waitTimeMs) {
        return srcSingleBytes.get(src -> this.set(des -> copy(src, des)), waitTimeMs);
    }

    public boolean copyFrom(EsSingleObject<E> srcSingleBytes) {
        return srcSingleBytes.get(src -> this.set(des -> copy(src, des)), lockTimeMs);
    }

    /**
     * 对象拷贝
     *
     * @param desSingleBytes 源数据
     * @return 是否复制成功
     */
    public boolean copyTo(EsSingleObject<E> desSingleBytes, long waitTimeMs) {
        return this.get(src -> desSingleBytes.set(des -> copy(src, des)), waitTimeMs);
    }

    public boolean copyTo(EsSingleObject<E> desSingleBytes) {
        return this.get(src -> desSingleBytes.set(des -> copy(src, des)), lockTimeMs);
    }
}
```

```java
// 非阻塞-线程安全 byte[] 缓冲区
public class EsSingleBytes extends EsSingleObject<byte[]> {
    public EsSingleBytes(int size) {
        super(new byte[size]);
    }

    @Override
    public boolean copy(byte[] src, byte[] des) {
        int len = Math.min(src.length, des.length);
        System.arraycopy(src, 0, des, 0, len);
        return true;
    }
}
// 定义
EsSingleBytes singleBytes = new EsSingleBytes(8);
// 缓存
byte[] src = {1, 2, 3, 4, 5, 6, 7, 8};
singleBytes.copyFrom(src);
// 读取
byte[] des = new byte[8];
singleBytes.copyTo(des);
```
