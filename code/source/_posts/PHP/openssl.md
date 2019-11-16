---
title: 加解密
tags: 
  - openssl
  - SM2
  - SM4
categories: 
  - PHP
description: openssl, SM2, SM4
date: 2019-10-03 16:03:34
updated: 2019-10-03 16:03:34
---

## openssl(1.1.1)

```PHP
// 版本号以及支持的内容
printf("Versoin : %s", OPENSSL_VERSION_TEXT);
echo "<br>";echo "<br>";
$digests = openssl_get_md_methods(false);
echo "Digests : ";
foreach ($digests as $digest) {
    echo $digest.",";
}

echo "<br>";echo "<br>";
$ciphers = openssl_get_cipher_methods(false);
echo "Ciphers : ";
foreach ($ciphers as $cipher) {
    echo $cipher.",";
}
echo "<br>";echo "<br>";

$curves = openssl_get_curve_names();
echo "Curves : ";
foreach ($curves as $curve) {
    echo $curve.",";
}
echo "<br>";echo "<br>";
```

```PHP
// SM4 加解密
$key = openssl_random_pseudo_bytes(16);
$ivlen = openssl_cipher_iv_length("sm4");
// $iv = openssl_random_pseudo_bytes($ivlen);
$iv = str_repeat("\0", $ivlen);
$plaintext = "message to be encrypted";
$ciphertext = openssl_encrypt($plaintext, "sm4", $key, $options=0, $iv);
$original_plaintext = openssl_decrypt($ciphertext, "sm4", $key, $options=0, $iv);

printf("sms4enc(\"%s\") = %s\n", $plaintext, bin2hex($ciphertext));
printf("sms4dec(%s) = \"%s\"\n", bin2hex($ciphertext), $original_plaintext);
```

```PHP
// ------------------------------------------------
// 证书加载：RM2 pkcs8格式证书
$private_content = file_get_contents(__DIR__.'\lfx.pkcs8.pem');
$prikey = openssl_pkey_get_private($private_content);

$pubkeypem = openssl_pkey_get_details($prikey)["key"];
$pubkey = openssl_pkey_get_public($pubkeypem);

$ec = openssl_pkey_get_details($prikey)["ec"];
echo "<br>";
// $ec["d"] <==> 证书明文
printf("SM2 Private Key: \nd:%s, \nx:%s, \ny:%s\n", bin2hex($ec["d"]), bin2hex($ec["x"]), bin2hex($ec["y"]));
echo "<br>";echo "<br>";

// 证书签名/验签
$msg = "abc";
$signature = "";
openssl_sign($msg, $signature, $prikey);            // 签名
$ok = openssl_verify($msg, $signature, $pubkey);    // 签名校验
echo "<br>";echo "<br>";
printf("verify(\"%s\", %s) = %s\n", $msg, bin2hex($signature), $ok ? "OK" : "Failure");
```
