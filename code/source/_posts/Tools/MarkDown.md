---
title: MarkDown
tags: 
  - MarkDown
categories: 
  - Tools
description: MarkDown, md
date: 2019-09-02 13:27:37
updated: 2019-09-02 13:27:37
---

## 常用规则

### 标题系列

```md
# 大标题
## 二标题
###### 六标题也可以

主标题
======

副标题
------
```

### 字体

+ **这是加粗的文字**`**这是加粗的文字**`
+ *这是倾斜的文字*`*这是倾斜的文字*`
+ ***这是斜体加粗的文字***`***这是斜体加粗的文字***`
+ ~~这是加删除线的文字~~`~~这是加删除线的文字~~`

```md
`背景色突出`
`单行代码`
代码块
```

### 引用

> 引用内容1
>> 引用内容2

### 列表

```md
* 无序列表
+ 无序列表
- 无序列表
```

```md
1. 有序列表，注意空格
2. 有序列表，会自动计算序号
   + 嵌套
   + 列表
```

```md
- [x] 任务列表
- [x] 已完成
- [ ] 未完成
```

### 分割线

```md
分割线
- - - （推荐）
---
***
* * *
```

分割线
- - -

### 图片

```md
![图片alt](图片地址 "图片title")

图片alt就是显示在图片下面的文字，相当于对图片内容的解释。
图片title是图片的标题，当鼠标移到图片上时显示的内容。title可加可不加
```

![blockchain](https://upload-images.jianshu.io/upload_images/6860761-fd2f51090a890873.jpg "区块链")

### 超链接

```md
[link](URL "注释")
```

[百度](https://wwww.baidu.com "百度超链接")
[简书](http://jianshu.com)
<a href="https://www.jianshu.com" target="_blank">新页面打开</a>

### 表格

Item     | Value
-------- | ---
Computer | $1600
Phone    | $12
Pipe     | $1

#### 表格：指定对齐方式

| Item     | Value | Qty   |
| :------- | ----: | :---: |
| Computer | $1600 |  5    |
| Phone    | $12   |  12   |
| Pipe     | $1    |  234  |

## 扩展

### 流程图

```flow
st=>start: 开始
op=>operation: My Operation
cond=>condition: Yes or No?
e=>end
st->op->cond
cond(yes)->e
cond(no)->op
```

### 自动生成目录

```md
[TOC]自动生成目录
```

## 编辑器

+ Nodepad++
  + 新版安装后就支持颜色处理，可扩展MarkDown插件展示效果
+ Visual Studio Code (VS Code)
