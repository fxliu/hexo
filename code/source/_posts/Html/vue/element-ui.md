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
import './element.css'
import Vue from 'vue'
import Element from 'element-ui'
// Vue.use(Element);
// 按需引用
import {
    Button,
    Tag,
    Input,
    Loading,
    Message,
    Notification,
    InfiniteScroll,
    MessageBox,
    Icon,
} from 'element-ui'

Vue.component(Button.name, Button);
Vue.component(Tag.name, Tag);
Vue.component(Input.name, Input);
Vue.component(Icon.name, Icon);

Vue.prototype.$message = Message;
Vue.prototype.$notify = Notification;

Vue.prototype.$msgbox = MessageBox;
Vue.prototype.$alert = MessageBox.alert;
Vue.prototype.$confirm = MessageBox.confirm;
Vue.prototype.$prompt = MessageBox.prompt;

Vue.use(InfiniteScroll);

// loading 效果默认值
Vue.prototype.$loading = function (options) {
    options = options || {};
    return Loading.service({
        text: '拼命加载中',
        spinner: 'el-icon-loading',
        background: 'rgba(0, 0, 0, 0.7)',
        ...options
    });
};
```
