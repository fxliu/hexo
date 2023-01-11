---
title: CryptoJS
tags: 
  - CryptoJS
categories: 
  - JS
description: CryptoJS
date: 2023-01-11 11:23:31
updated: 2023-01-11 11:23:31
---

## 基础

```js
CryptoJS.MD5('待加密字符串').toString()
CryptoJS.SHA256('待加密字符串').toString()

// str -> word
CryptoJS.enc.Utf8.parse(utf8String)
CryptoJS.enc.Utf8.stringify(utf8String)

CryptoJS.enc.Latin1.parse(latin1String)
// hex -> bin
CryptoJS.enc.Hex.parse(hexString)
```

## Base64

```js
CryptoJS.enc.Base64.stringify(CryptoJS.enc.Utf8.parse('待加密字符串'))
CryptoJS.enc.Base64.parse("待解密字符串").toString(CryptoJS.enc.Utf8)

function Base64Enc(data) {
    return CryptoJS.enc.Base64.stringify(CryptoJS.enc.Utf8.parse(data));
}
function Base64Dec(data) {
    return CryptoJS.enc.Base64.parse(data);
    // return CryptoJS.enc.Base64.parse(data).toString(CryptoJS.enc.Utf8);
}
```

## AES

```js
CryptoJS.AES.encrypt('待加密字符串', '秘钥').toString()
CryptoJS.AES.decrypt('待解密字符串', '秘钥').toString(CryptoJS.enc.Utf8)

// 加密, 返回Base64
function CfbEnc(data) {
    let key = CryptoJS.enc.Utf8.parse('7a2bowijta9j3t1f');
    let iv = CryptoJS.enc.Utf8.parse('aldd8tp4cfgf7juk');
    return CryptoJS.AES.encrypt(data, key, {
        iv: iv,
        mode: CryptoJS.mode.CFB,
        padding: CryptoJS.pad.ZeroPadding
    }).toString();
}
// 解密, 传入Base64
function CfbDec(data) {
    let key = CryptoJS.enc.Utf8.parse('7a2bowijta9j3t1f');
    let iv = CryptoJS.enc.Utf8.parse('aldd8tp4cfgf7juk');
    return CryptoJS.AES.decrypt(data, key, {
        iv: iv,
        mode: CryptoJS.mode.CFB,
        padding: CryptoJS.pad.ZeroPadding
    }).toString(CryptoJS.enc.Utf8);
}
console.log(CfbEnc('1234567812345678'));
console.log(CfbDec(CfbEnc('1234567812345678')));

```

## ApiPost

```js
# 预执行脚本
const reqData = {
   "username": "13210001000", 
   "password": "123456",
   "equip": "Android VOG-AL00"
};
const str = randomStr(16);
let req = str + JSON.stringify(reqData);
let info = CfbEnc(req);

console.error('上报原文：' + req);
console.error('上报密文：' + info)

// 动态添加一个键为info 值为 加密字符串 的body参数
apt.setRequestBody("info", info);

function randomStr(length=16) {
   var result           = '';
   var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
   var charactersLength = characters.length;
   for ( var i = 0; i < length; i++ ) {
      result += characters.charAt(Math.floor(Math.random() * charactersLength));
   }
   return result;
}
```
