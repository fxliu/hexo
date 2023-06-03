---
title: sm3
tags: 
  - sm3
categories: 
  - PHP
description: sm3
date: 2023-06-03 10:38:29
updated: 2023-06-03 10:38:29
---

## sm3

```php
<?php

class Sm3
{
    private $IV      = '7380166f4914b2b9172442d7da8a0600a96f30bc163138aae38dee4db0fb0e4e';
    private $LEN     = 512;
    private $STR_LEN = 64;

    public function sign($str)
    {
        $l   = strlen($str) * 8;
        $k   = $this->getK($l);
        $bt  = $this->getB($k);
        $str = $str . $bt . pack('J', $l);

        $count = strlen($str);
        $l     = $count / $this->STR_LEN;
        $vr    = hex2bin($this->IV);
        for ($i = 0; $i < $l; $i++) {
            $vr = $this->cf($vr, substr($str, $i * $this->STR_LEN, $this->STR_LEN));
            // echo bin2hex($vr)."\n";
        }
        return bin2hex($vr);

    }

    private function getK($l)
    {
        $v = $l % $this->LEN;
        return $v + $this->STR_LEN < $this->LEN
            ? $this->LEN - $this->STR_LEN - $v - 1
            : ($this->LEN * 2) - $this->STR_LEN - $v - 1;
    }

    private function getB($k)
    {
        $arg = [128];
        $arg = array_merge($arg, array_fill(0, intval($k / 8), 0));
        return pack('C*', ...$arg);
    }

    public function signFile($file)
    {
        $l  = filesize($file) * 8;
        $k  = $this->getK($l);
        $bt = $this->getB($k).pack('J', $l);

        $hd  = fopen($file, 'r');
        $vr  = hex2bin($this->IV);
        $str = fread($hd, $this->STR_LEN);
        if ($l > $this->LEN - $this->STR_LEN - 1) {
            do {
                $vr  = $this->cf($vr, $str);
                $str = fread($hd, $this->STR_LEN);
            } while (!feof($hd));
        }

        $str   = $str . $bt;
        $count = strlen($str) * 8;
        $l     = $count / $this->LEN;
        for ($i = 0; $i < $l; $i++) {
            $vr = $this->cf($vr, substr($str, $i * $this->STR_LEN, $this->STR_LEN));
        }
        return bin2hex($vr);
    }


    private function t($i)
    {
        return $i < 16 ? 0x79cc4519 : 0x7a879d8a;
    }

    private function cf($ai, $bi)
    {
        $wr = array_values(unpack('N*', $bi));
        for ($i = 16; $i < 68; $i++) {
            $wr[$i] = $this->p1($wr[$i - 16]
                    ^
                    $wr[$i - 9]
                    ^
                    $this->lm($wr[$i - 3], 15))
                ^
                $this->lm($wr[$i - 13], 7)
                ^
                $wr[$i - 6];
        }
        $wr1 = [];
        for ($i = 0; $i < 64; $i++) {
            $wr1[] = $wr[$i] ^ $wr[$i + 4];
        }

        list($a, $b, $c, $d, $e, $f, $g, $h) = array_values(unpack('N*', $ai));

        for ($i = 0; $i < 64; $i++) {
            $ss1 = $this->lm(
                ($this->lm($a, 12) + $e + $this->lm($this->t($i), $i % 32) & 0xffffffff),
                7);
            $ss2 = $ss1 ^ $this->lm($a, 12);
            $tt1 = ($this->ff($i, $a, $b, $c) + $d + $ss2 + $wr1[$i]) & 0xffffffff;
            $tt2 = ($this->gg($i, $e, $f, $g) + $h + $ss1 + $wr[$i]) & 0xffffffff;
            $d   = $c;
            $c   = $this->lm($b, 9);
            $b   = $a;
            $a   = $tt1;
            $h   = $g;
            $g   = $this->lm($f, 19);
            $f   = $e;
            $e   = $this->p0($tt2);
        }

        return pack('N*', $a, $b, $c, $d, $e, $f, $g, $h) ^ $ai;
    }


    private function ff($j, $x, $y, $z)
    {
        return $j < 16 ? $x ^ $y ^ $z : ($x & $y) | ($x & $z) | ($y & $z);
    }

    private function gg($j, $x, $y, $z)
    {
        return $j < 16 ? $x ^ $y ^ $z : ($x & $y) | (~$x & $z);
    }


    private function lm($a, $n)
    {
        return ($a >> (32 - $n) | (($a << $n) & 0xffffffff));
    }

    private function p0($x)
    {
        return $x ^ $this->lm($x, 9) ^ $this->lm($x, 17);
    }

    private function p1($x)
    {
        return $x ^ $this->lm($x, 15) ^ $this->lm($x, 23);
    }

}

//------FOR TEST-------------------------------------
// 直接请求该PHP，运行测试代码
if (strcasecmp(basename($_SERVER['SCRIPT_NAME']), basename(__FILE__)) == 0)
{
	function msectime() {
		list($msec, $sec) = explode(' ', microtime());
		$msectime = (float)sprintf('%.0f', (floatval($msec) + floatval($sec)) * 1000);
		return $msectime;
	}

    $sm3 = new Sm3();
    $b = msectime();
    // echo $sm3->signFile("test.txt")."\n"; echo "time:".(msectime() - $b); die;

    $signData = '18A06C1EE8D5B1352D55421C14BDA9C136363636363636363636363636363636363636363636363636363636363636363636363636363636363636363636363661707049643D4646545A323231303039313135363238323430312662697A53657175656E636549643D39324246424538443842434434353738383236323644313037353644433037362662697A54696D653D323032323131333031303239323126656E637279707452616E646F6D3D424F50425866783768377933317A6D5A472B5977476F734A7764636A564D3149626E6278476B326F753747386F6C47583548753157656B517249533270366163484D6A51523532455634586669554E696C74502B6D793654717647786573733362627A7365357442415270566D697766426D3149733479386D64417862396F6F6F526A6D476872435A654B512F67506941376D46346F773D26656E6372797074547970653D3226656E63727970746564446174613D64562F656E4132416B42585153476A5968622F77626F6F756E7435456E4154426E657968332B72765549757865356252385873753478666771715261784342416A76674E457946694C75325045396E684546767A4F6A7974464E6C55347659794F2B316E7156684273595151574A4D4B7931352F74646746656E793278386C54705161697A2B68665A43486D764773796277375458766D68424E7A77356C52696B773969437270356B4C4A475431456E38334E372B732F766F2F52385534676253595131666945516D55594D5478535A616E5A42426B5035755966745A652F69776862384A4161796C4D522B354B7559507967664E6A53516D4A5A5552507551267365637572697479466163746F723D656E6372797074466163746F723D35393346363135304139354246313833267369676E466163746F723D45463943373137444546373634373233267369676E547970653D342676657273696F6E3D322E302E30';
    $signData = hex2bin($signData);
    // echo "src:".$signData."\n";

    // 签名结果: 1f11157281c1367d30819b9f5ca2344b8c46258151f7786ffb335255646f542b
	$b = msectime();
    echo $sm3->sign($signData)."\n";
	echo "time:".(msectime() - $b);
}

```
