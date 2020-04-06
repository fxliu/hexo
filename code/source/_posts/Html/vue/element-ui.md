---
title: element-ui
tags: 
  - element-ui
categories: 
  - JS
  - vue
description: element-ui
date: 2020-04-04 20:59:46
updated: 2020-04-04 20:59:46
---

## 饿了么组件

[element-ui](https://element.eleme.cn/#/zh-CN/component/installation)

## 按需加载

+ 安装babel编译插件
  + `npm i babel-plugin-component -D`

### 插件配置

```js
module.exports = {
  "presets": [...],
  "plugins": [
    [
      "component",
      {
        "libraryName": "element-ui",
        "styleLibraryName": "theme-chalk"
      }
    ]
  ]
};
```

### 插件加载

```js
import 'element-ui/lib/theme-chalk/index.css'
import Vue from 'vue'
import Element from 'element-ui'
// Vue.use(Element);
// 按需引用
import {
    Button,
    Loading,
    Message,
    InfiniteScroll,
} from 'element-ui'

Vue.component(Button.name, Button);

Vue.prototype.$loading = Loading.service;
Vue.prototype.$message = Message;

Vue.use(InfiniteScroll);
```
