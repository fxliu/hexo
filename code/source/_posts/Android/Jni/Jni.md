---
title: jni
tags: 
    - jni
categories: 
    - Android
description: jni
date: 2022-06-01 19:43:10
updated: 2022-06-01 19:43:10
---

## 基础使用

```java
public class MyJni {
    private final static String TAG = MyJni.class.getSimpleName();
    private Context context;
    // ---------------------------------------------------------------------------------------------
    // 单例模式
    private static MyJni INSTANCE = null;
    public static MyJni getInst() {
        if (null == INSTANCE) {
            synchronized (MyJni.class) {
                if (null == INSTANCE) {
                    INSTANCE = new MyJni();
                }
            }
        }
        return INSTANCE;
    }
    private MyJni() {}
    // ---------------------------------------------------------------------------------------------
    // lib_eididcard_sdk.so  ->  C代码编译结果
    static {
        System.loadLibrary("_eididcard_sdk");
    }
    public native String Test();
}
```

```c++
#include <jni.h>
#include <string>
#include <android/log.h>
#define LOGD(...)  __android_log_print(ANDROID_LOG_DEBUG, "native",__VA_ARGS__)
#define LOGE(...)  __android_log_print(ANDROID_LOG_ERROR, "native",__VA_ARGS__)

extern "C" JNIEXPORT jstring JNICALL
Java_com_eseid_sdk_EidJni_Test(JNIEnv *env, jobject ) {
    std::string hello = "Hello from C++";
    return env->NewStringUTF(hello.c_str());
}
```

## 类型转化

```c++
// std::string -> jsting：注意必须是字符串
std::string hello = "Hello from C++";
jstring str = env->NewStringUTF(hello);

// jstring -> char*
// 转化：jstring jStr, 注意这里是有编码处理的
const char* data = env->GetStringUTFChars(jStr, nullptr);
// 释放
env->ReleaseStringUTFChars(jStr, data);

// char* -> jbyteArray: 数组
// 转化：const char *data, int dataLen
jbyteArray arr = env->NewByteArray(dataLen);
env->SetByteArrayRegion(arr, 0, dataLen, (jbyte*)(data));
// 释放
if(arr) env->DeleteLocalRef(arr);

// jbyteArray -> char*
// 转化：jbyteArray data
jbyte* szData = env->GetByteArrayElements(arr, nullptr);
len = env->GetArrayLength(arr);
// 释放
env->ReleaseByteArrayElements(arr, szData, 0);
```

## 回调
```java
public class MyJni {
    public void onLogCB(int level, String msg) {
        switch (level) {
            case Codes.ES_LOG_LEVEL_INFO:
                Log.i(TAG, msg);
                break;
            case Codes.ES_LOG_LEVEL_WARN:
                Log.w(TAG, msg);
                break;
            case Codes.ES_LOG_LEVEL_ERROR:
                Log.e(TAG, msg);
                break;
            default:
                Log.d(TAG, msg);
                break;
        }
    }
}
```
```c++
// Java Jni 单例模式，javaObj固定
static JavaVM *javaVM = nullptr;
static jobject javaObj;
// 初始化时赋值Java虚拟环境句柄
extern "C" JNIEXPORT jboolean JNICALL
Java_com_eseid_sdk_EidJni_init(JNIEnv* env, jobject thiz, jstring flag, jstring type) {
    env->GetJavaVM(&javaVM);
    javaObj = env->NewGlobalRef(thiz);
    return re;
}
// 日志回调
void NATIVE_ES_LogCB(ES_LOG_LEVEL level, const char* szMsg, void*)
{
    if(javaObj == nullptr) return;
    // 绑定到当前虚拟环境
    bool bAttach = false;
    JNIEnv *env = nullptr;
    if(javaVM->GetEnv((void**)&env, JNI_VERSION_1_6) != JNI_OK) {
        if(javaVM->AttachCurrentThread(&env, nullptr) != JNI_OK) {
            LOGE("NATIVE_ES_LogCB: javaVM->AttachCurrentThread Error");
            LOGD("%s", szMsg);
            return;
        }
        bAttach = true;
    }
    // 获取对象函数句柄 - 并执行
    jclass cls = env->GetObjectClass(javaObj);
    jmethodID id = env->GetMethodID(cls, "onLogCB", "(ILjava/lang/String;)V");
    if (id != nullptr){
        jstring str = env->NewStringUTF(szMsg);
        env->CallVoidMethod(javaObj, id, (int)level, str);
        env->DeleteLocalRef(str);
    } else {
        LOGE("env->GetMethodID(onLogCB) Error");
        LOGD("%s", szMsg);
    }
    // 释放对象，解除绑定
    env->DeleteLocalRef(cls);
    if(bAttach)
        javaVM->DetachCurrentThread();
}
```
