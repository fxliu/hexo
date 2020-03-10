---
title: MongoDB
tags: 
    - MongoDB
categories: 
    - VC
description: MongoDB
date: 2020-03-03 10:27:37
updated: 2020-03-03 10:27:37
---

## 官网

+ [MongoDB](https://www.sqlite.org/download.html)
+ [mongo-c-driver](https://github.com/mongodb/mongo-c-driver)
  + 下载Release版，zip包，包含需要的libbson等
+ [libbson.git](https://github.com/mongodb/libbson.git)
+ 客户端
  + [Robo 3T](https://robomongo.org/download)
+ 编译工具
  + [cmake](https://cmake.org/)

## 客户端编译

+ [官网引导文档](http://mongoc.org/libmongoc/current/installing.html)
+ [cmake-gui]
  + Configure
    + `Source Code`: `D:/mongo-c-driver-1.16.2`
    + `build the binaries`: `D:/mongo-c-driver-1.16.2/build`
    + Configure按钮
      + 选择VS编译器版本
    + 错误处理
      + BUILD_VERSION: 1.0.0.0
      + CMAKE_INSTALL_PREFIX: 路径要预先创建`D:/mongo-c-driver`
      + 配置调整完成后，重新点击Configure按钮
  + Generate
  + `D:/mongo-c-driver-1.16.2/build`目录找到`ALL_BUILD.vcxproj`使用VS打开即可
    + 编译`INSTALL`工程
      + 内容生成到`D:/mongo-c-driver`，包含静态lib，include头文件等

## 简单使用

[API](http://mongoc.org/libmongoc/current/api.html)

```C++
// .h
mongoc_uri_t *m_uri;
mongoc_client_t *m_client;
mongoc_collection_t *m_collection;
mongoc_collection_t *m_collConfig;
// 初始化
mongoc_init();
// 释放
mongoc_cleanup();
// 连接
bson_error_t error;
CStringA strMongoDB = "mongodb://127.0.0.1:27017/";
m_uri = mongoc_uri_new_with_error(strMongoDB, &error);
if (!m_uri)
{
    Log()->LogA("failed to parse URI: %s\n;error message: %s;\n", CW2A(strMongoDB).m_psz, error.message);
    return;
}
m_client = mongoc_client_new_from_uri(m_uri);
if (!m_client)
{
    Log()->LogA("mongoc_client_set_error_api error;\n");
    return;
}
// 简便方法，不使用uri
// m_client = mongoc_client_new(strMongoDB);
// 释放连接
mongoc_uri_destroy(m_uri);
mongoc_client_destroy(m_client);

// 集合
mongoc_client_set_error_api(m_client, 2);
m_collection = mongoc_client_get_collection(m_client, "sync", "pic");
if (!m_collection)
{
    Log()->LogA("mongoc_client_get_collection error: sync.pic;\n");
    return false;
}
// 释放集合
mongoc_collection_destroy(m_collection);

// 创建索引：不存在则创建
bson_t keys;
bson_init(&keys);
BSON_APPEND_INT32(&keys, "account", 1);
BSON_APPEND_INT32(&keys, "last_user_time", -1);
mongoc_index_opt_t opt;
mongoc_index_opt_init(&opt);
opt.name = "user_sync_time";    // 指定索引名称
if (!mongoc_collection_create_index(m_collection, &keys, &opt, &error))
{
    Log()->LogA("mongoc_collection_create_index error: %s;", error.message);
    bson_destroy(&keys);
    return false;
}
// bson_t 对象需要释放
bson_destroy(&keys);
```

```C++
// 插入
bson_t item;
bson_init(&item);
BSON_APPEND_SYMBOL(&item, "_id", pic_md5.GetBuffer());
BSON_APPEND_BINARY(&item, "sn", BSON_SUBTYPE_BINARY, (const uint8_t*)strFeature.c_str(), strFeature.length());
BSON_APPEND_SYMBOL(&item, "account", account.GetBuffer());

bson_error_t error;
if (mongoc_collection_insert(m_collection, MONGOC_INSERT_CONTINUE_ON_ERROR, &item, NULL, &error))
    Log()->LogA("mongoc_collection_insert: %s", pic_md5);
else
    Log()->LogA("mongoc_collection_insert error: %s", pic_md5);
bson_destroy(&item);
```

```C++
// 查询
mongoc_cursor_t* CMongoClient::Query()
{
    bson_t filter;
    bson_init(&filter);
    // 设置查询字段
    bson_t opts;
    bson_init(&opts);
    // 设置显示字段
    bson_t opts_project;
    BSON_APPEND_DOCUMENT_BEGIN(&opts, "projection", &opts_project);
    BSON_APPEND_INT32(&opts_project, "_id", 0);
    bson_append_document_end(&opts, &opts_project);
    // 设置索引
    bson_t opts_sort;
    BSON_APPEND_DOCUMENT_BEGIN(&opts, "sort", &opts_sort);
    BSON_APPEND_INT32(&opts_sort, "last_user_time", 1);
    bson_append_document_end(&opts, &opts_sort);
    mongoc_cursor_t* cursor = mongoc_collection_find_with_opts(m_collection, &filter, &opts, NULL);

    bson_destroy(&filter);
    bson_destroy(&opts);
    bson_destroy(&opts_project);
    return cursor;
}
const bson_t* CMongoClient::GetNext(mongoc_cursor_t* cursor)
{
    const bson_t* doc = NULL;
    if (mongoc_cursor_next(cursor, &doc)) {
        //char* str = bson_as_canonical_extended_json(doc, NULL);
        //printf("%s\n", str);
        //bson_free(str);
        return doc;
    }
    return false;
}
CStringA GetStringValue(const bson_t* doc, CStringA key)
{
    bson_iter_t iter;
    if (bson_iter_init_find(&iter, doc, key))
    {
        uint32_t len = 0;
        const char *value = bson_iter_symbol(&iter, &len);
        return CStringA(value);
    }
    return "";
}
CStringA GetBinaryValue(const bson_t* doc, CStringA key)
{
    bson_iter_t iter;
    if (bson_iter_init_find(&iter, doc, key))
    {
        bson_subtype_t subType;
        uint32_t len = 0;
        uint8_t *data = NULL;
        bson_iter_binary(&iter, &subType, &len, &data);
        return CStringA((char*)data, len);
    }
    return "";
}
void FreeQuery(mongoc_cursor_t* cursor)
{
    mongoc_cursor_destroy(cursor);
}
```
