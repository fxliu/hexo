---
title: cfb
tags: 
  - cfb
categories: 
  - PHP
description: cfb
date: 2022-12-14 13:01:27
updated: 2022-12-14 13:01:27
---

## CFB

```php
header("Content-Type: text/html; charset=UTF-8");
// 
define('__AES_TEST_KEY__','mehbf4xdswc3vzkg');
define('__AES_TEST_IV__','jpufq5ez18dit6b3');

// ----------------------------------------------------------------------------
/*
 * AES/CFB/NOPadding 加密
 */
function cfbEncode($text,$key,$iv){
	$cipher="AES-128-CFB";
	$text = openssl_encrypt($text, $cipher, $key, $options=OPENSSL_ZERO_PADDING, $iv);
	return $text;
}

/**
 * AES/CFB/NOPadding 解密
 */
function cfbDecode($text,$key,$iv){
	$cipher="AES-128-CFB";
	$text = openssl_decrypt($text, $cipher, $key, $options=OPENSSL_ZERO_PADDING, $iv);
	return $text;
}

/**
 * 生成随机字符串
 */
function getrandstr($length){
	$str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890';
	//打乱字符串
	$randStr = str_shuffle($str);
	//substr(string,start,length);返回字符串的一部分
	$rands= substr($randStr,0,$length);
	return $rands;
}

// Json加密测试 - 前置16B随机数
function cfbTest() {
	$str=getrandstr(16);
	$src = array(
		"errno" => "0",
		"error" => "",
		"time" => date("Y-m-d H:i:s")
	);
	$json=json_encode($src);
	echo "src=".$json."<br>";

	$json=$str.json_encode($src);
	$json=cfbEncode($json,__AES_TEST_KEY__,__AES_TEST_IV__);
	echo "enc=".$json."<br>";

	$str=str_replace(" ", "+", $json);
	$json=cfbDecode($str,__AES_TEST_KEY__,__AES_TEST_IV__);
	$json=substr($json, 16);
	echo "dec=".$json."<br>";
}

//------FOR TEST-------------------------------------
// 直接请求该PHP，运行测试代码
if (strcasecmp(basename($_SERVER['SCRIPT_NAME']), basename(__FILE__)) == 0)
{
    // 直接请求该PHP，运行如下测试代码
    // 作为模块被include，则不运行
    cfbTest();
}

```
