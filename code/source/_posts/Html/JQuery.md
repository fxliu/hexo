---
title: JQuery
tags: 
  - JQuery
categories: 
  - JS
description: JQuery
date: 2019-11-14 19:04:37
updated: 2019-11-14 19:04:37
---

## 基础

```js
function ajaxGet(url, data) {
    const _this = this;
    $.get(url, data, function (data, status) {
        myPrint("状态：" + status);
        myPrint("数据：" + data);
        // 这里的this是ajax的this, 要使用外层this需要自己定义变量保存
        _this.content = data;
    }, "json")  // 指定 dataType: "json"
}

function ajaxPost(url, data, param={}) {
    if(param)
        url += "?" + $.param(param);
    $.post(url, data, function (data, status) {
        myPrint("状态：" + status);
        myPrint("数据：" + data);
    }, "json")
}
let d = {
    a: "1",
    b: "2",
};
ajaxGet('/uri', d);
```

```js
// 重写，达到事件拦截的效果
/** 简单封装: 仅失败处理
 * 成功: 打印顺序 -> success -> done
 * 失败: 打印顺序 -> error -> --fail-- -> fail
 */
(function ($) {
    $._ajax = $.ajax;    // 备份
    $.ajax = undefined;
    $.ajax = function (url, options) {    // 重写
        return $._ajax(url, options).fail( function () {
            console.log("--fail--");
        });
    };
})(jQuery);

/** 事件封装
 * 成功顺序: _beforeSend -> _success -> success -> done -> _complete
 * 失败顺序: _beforeSend -> _error -> error -> fail -> _complete
*/
(function ($) {
    //首先备份下jquery的ajax方法
    const _ajax = $.ajax;

    //重写jquery的ajax方法
    $.ajax = function (opt) {
        const success = opt.success;
        const error = opt.error;
        const _opt = $.extend(opt, {
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                console.log('_error');
                if (error)
                    error(XMLHttpRequest, textStatus, errorThrown);
            },
            success: function (data, textStatus) {
                console.log('_success');
                if (success)
                    success(data, textStatus);
            },
            beforeSend: function (XHR) {
                // 提交前回调方法
                console.log('_beforeSend');
            },
            complete: function (XHR, TS) {
                // 请求完成后回调函数 (请求成功或失败之后均调用)。
                console.log('_complete');
            }
        });
        return _ajax(_opt);
    };
})(jQuery);

/**
 * ajax 事件处理
 * 失败顺序: fail -> document -> window
*/
$(window).ajaxError(function (event, XMLHttpRequest, ajaxOptions) {
    console.log('ajaxError this === window', this === window);
});
$(document).ajaxError(function (event, XMLHttpRequest, ajaxOptions) {
    console.log('ajaxError this === document', this === document);
});

$.ajax('test.php').fail(function () {
    console.log("fail");
});

$.ajax({
    url: "../test.php",
    type: "GET",
    success: function () {
        console.log('success');
    },
    error: function () {
        console.log('error');
    }
}).done(function () {
    console.log('done');
}).fail(function () {
    console.log('fail');
});
```
