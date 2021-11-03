---
title: vue-axios
tags: 
  - vue-axios
categories: 
  - JS
  - vue
description: vue-axios
date: 2019-12-02 10:56:59
updated: 2019-12-02 10:56:59
---

## 基础

[vue-axios](https://www.npmjs.com/package/vue-axios)

## 加载

```js
import 'esbase/assets/css/esbase-pc.css'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'
import VueAxios from 'vue-axios'

const app = createApp(App);
app.use(VueAxios, axios);
app.use(router).mount('#app');
```

## 基础使用

```js
this.axios.get('./api/idcard_info', {
  timeout: 2000,
}).then(function (response) {
  console.log(response["data"]);
}.bind(this)).finally(function () {
  console.log('finally');
}.bind(this));
```
