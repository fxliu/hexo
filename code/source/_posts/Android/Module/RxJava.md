---
title: RxJava
tags: 
    - RxJava
categories: 
    - Android
description: RxJava
date: 2020-03-15 22:00:20
updated: 2020-03-15 22:00:20
---

## 基础应用

+ 创建被观察者`Observable`，并在订阅接口`subscribe`中发布时间

### 被观察者

```java
// Observable。create() 是 RxJava 最基本的创造事件序列的方法
Observable<Integer> observable = Observable.create(new ObservableOnSubscribe<Integer>() {
    // 复写的subscribe，定义需要发送的事件
    @Override
    public void subscribe(ObservableEmitter<Integer> emitter) throws Exception {
        // 通过 ObservableEmitter 对象(事件发布器)产生事件并通知观察者
        if (!observer.isUnsubscribed()) {
            emitter.onNext(1);
            emitter.onNext(2);
            emitter.onNext(3);
        }
        emitter.onComplete();
    }
});

// just
Observable observable = Observable.just("A", "B", "C");
// 将会依次调用：
// onNext("A");
// onNext("B");
// onNext("C");
// onCompleted();

// from(T[]) / from(Iterable<? extends T>) : 遍历传入的数组 / Iterable，依次发送出来
String[] words = {"A", "B", "C"};
Observable observable = Observable.from(words);
// 将会依次调用：
// onNext("A");
// onNext("B");
// onNext("C");
// onCompleted();

// 数组
Integer[] items = { 0, 1, 2, 3, 4 };
Observable observable = Observable.fromArray(items);
// 集合
List<Integer> list = new ArrayList<>();
list.add(1);
Observable observable = Observable.fromIterable(list);

// 下列方法一般用于测试使用
// 仅发送Complete事件
Observable observable1=Observable.empty();
// 仅发送Error事件
Observable observable2=Observable.error(new RuntimeException());
// 该方法创建的被观察者对象发送事件的特点：不发送任何事件
Observable observable3=Observable.never();

// 直到有观察者时，才真正创建 ObservableSource
Observable<Integer> observable = Observable.defer(new Callable<ObservableSource<? extends Integer>>() {
    @Override
    public ObservableSource<? extends Integer> call() throws Exception {
        return Observable.just(i);
    }
});

// 延迟发送事件： 延迟2s后，发送一个long类型数值
Observable.timer(2, TimeUnit.SECONDS);
// 延迟3秒后，每1秒 发送一个long类型数值，从0开始递增1，无限发送
Observable.interval(3,1,TimeUnit.SECONDS);
// 延迟3秒后，第一个事件延迟2秒，之后每1秒 发送一个long类型数值，从0开始递增1，发送10次
Observable.intervalRange(3, 10, 2, 1, TimeUnit.SECONDS);
// 无延迟，从3开始，发送10个事件
Observable.range(3,10);
```

### 观察者 / 订阅者

```java
// 观察者：Observer 抽象类
Observer<Integer> observer = new Observer<Integer>() {
    // 订阅事件通知：观察者接收事件前调用
    @Override
    public void onSubscribe(Disposable d) {
        Log.d(TAG, "开始采用subscribe连接");
    }
    // 被观察者onNext事件响应
    @Override
    public void onNext(Integer value) {
        Log.d(TAG, "对Next事件作出响应" + value);
    }
    // 被观察者Error事件响应
    @Override
    public void onError(Throwable e) {
        Log.d(TAG, "对Error事件作出响应");
    }
    // 被观察者生产onCompleted事件响应
    @Override
    public void onComplete() {
        Log.d(TAG, "对Complete事件作出响应");
    }
};

// 订阅者：Subscriber（内置实现 Observer 的抽象类，并对Observer接口进行了扩展）
Subscriber<Integer> subscriber = new Subscriber<Integer>() {
    @Override
    public void onSubscribe(Subscription s) {
        Log.d(TAG, "开始采用subscribe连接");
    }

    @Override
    public void onNext(Integer value) {
        Log.d(TAG, "对Next事件作出响应" + value);
    }

    @Override
    public void onError(Throwable e) {
        Log.d(TAG, "对Error事件作出响应");
    }

    @Override
    public void onComplete() {
        Log.d(TAG, "对Complete事件作出响应");
    }
};
/**
相同点：二者基本使用方式完全一致
    实质上，在RxJava的 subscribe 过程中，Observer总是会先被转换成Subscriber再使用

不同点：Subscriber抽象类对 Observer 接口进行了扩展，新增了两个方法：
    1. onStart()：在还未响应事件前调用，用于做一些初始化工作
    2. unsubscribe()：用于取消订阅。在该方法被调用后，观察者将不再接收 & 响应事件
    调用该方法前，先使用 isUnsubscribed() 判断状态
*/

// 订阅 / 注册
observable.subscribe(observer);
observable.subscribe(subscriber)；
```

```Java
// RxJava的链式操作
/** 注：整体方法调用顺序：
1. 观察者.onSubscribe()
2. 被观察者.subscribe()
3. 观察者.onNext()
4. 观察者.onComplete()
*/
Observable.create(new ObservableOnSubscribe<Integer>() {
    // 1. 创建被观察者 & 生产事件
    @Override
    public void subscribe(ObservableEmitter<Integer> emitter) throws Exception {
        emitter.onNext(1);
        emitter.onNext(2);
        emitter.onNext(3);
        emitter.onComplete();
    }
})
.observeOn(Schedulers.io())
.subscribeOn(Schedulers.newThread())
.subscribe(new Observer<Integer>() {
    // 2. 通过通过订阅（subscribe）连接观察者和被观察者
    // 3. 创建观察者 & 定义响应事件的行为
    @Override
    public void onSubscribe(Disposable d) {
        Log.d(TAG, "开始采用subscribe连接");
    }
    @Override
    public void onNext(Integer value) {
        Log.d(TAG, "对Next事件"+ value +"作出响应");
    }
    @Override
    public void onError(Throwable e) {
        Log.d(TAG, "对Error事件作出响应");
    }
    @Override
    public void onComplete() {
        Log.d(TAG, "对Complete事件作出响应");
    }
});
// SubscribeOn: 指定Observable自身在哪个调度器上执行
// ObserveOn: 指定一个观察者在哪个调度器上观察这个Observable
// AndroidSchedulers.mainThread()： 主线程
// Schedulers.newThread()： 新建线程
// Schedulers.io(): 内置线程池，优于Schedulers.newThread
// compose: 关联一个继承RxActivity的Activity，从而实现自动释放
```

```java
// 便捷函数式应用：消费者
Observable.just("hello").subscribe(new Consumer<String>() {
    // 每次接收到Observable的事件都会调用Consumer.accept（）
        @Override
        public void accept(String s) throws Exception {
            System.out.println(s);
        }
    });
// 还有其他一些便捷函数式应用
```
