---
title: Vue
tags: 
  - Vue
categories: 
  - JS
description: Vue
date: 2019-12-02 10:56:59
updated: 2019-12-02 10:56:59
---

## 基础

```HTML
<!-- 嵌套: 三元表达式 -->
<div :class="[isActive ? 'active' : '', ...]"></div>
```

## 绑定(class | style)

```HTML
<div
  class="static"
  v-bind:class="{ active: isActive, 'text-danger': hasError }"
></div>
<script>
// HTML对象形式
data: {
  isActive: true,
  hasError: false
}
</script>
```

```HTML
<div
  class="static"
  v-bind:class="classObject"
></div>
<script>
// JS对象形式
data: {
  classObject: {
    active: true,
    'text-danger': false
  }
}
</script>
```

```HTML
<div v-bind:class="[active, error]"></div>
<script>
// 数组形式
data: {
  active: 'active',
  isActive: true,
  error: 'text-danger'
}
</script>

<div v-bind:class="[{ active: isActive }, error]"></div>
<script>
// 数组对象交叉
data: {
  isActive: true,
  error: 'text-danger'
}
</script>
```

## 插件

```js
// utils.js
export default {
  getUrlKey:function(name){
    let parames = new RegExp('[?|&]' + name + '=' + '([^&;]+?)(&|#|;|$)').exec(location.href);
    if(parames)
        return decodeURIComponent(parames[1].replace(/\+/g, '%20'));
    return "";
  }
}
// 引入
import utils from './components/utils'
Vue.prototype.$utils = utils;
// .vue使用
let code = this.$utils.getUrlKey('code');
```
