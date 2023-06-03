---
title: sm2
tags: 
  - sm2
categories: 
  - PHP
description: sm2
date: 2023-06-03 18:45:56
updated: 2023-06-03 18:45:56
---

## sm2

```php
// Util.php
trait Util
{
    public function hexToBytes($hex)
    {
        if (strlen($hex) % 2 != 0) { // 奇数位补0
            $hex = "0" . $hex;
        }
        $bytes = [];
        $len = strlen($hex);
        for ($i = 0; $i < $len; $i++) {
            $bytes[] = (int)base_convert($hex[$i] . $hex[++$i], 16, 10);
        }

        return $bytes;
    }

    public function bytesToHex($data)
    {
        $hex = '';
        foreach ($data as $value) {
            $hex .= $this->decHex($value, 8);
        }

        return $hex;
    }

    public function leftRotate($x, $i)
    {
        $i %= 32;

        return (($x << $i) & 0xFFFFFFFF) | ($x >> (32 - $i));
    }

    public function strToBytes($string)
    {
        return unpack("C*", $string);
    }

    public function bytesToStr($bytes)
    {
        array_unshift($bytes,'C'.count($bytes));

        return call_user_func_array('pack', $bytes);
    }

    public function add(...$a)
    {
        $sum = array_sum($a);
        $sum > 0xFFFFFFFF && $sum &= 0xFFFFFFFF;

        return $sum;
    }

    public function getHex($number, $count = 8)
    {
        return str_pad($number, $count, "0", STR_PAD_LEFT);
    }

    public function generate($numBits = 256)
    {
        $value = gmp_random_bits($numBits);
        $mask = gmp_sub(gmp_pow(2, $numBits), 1);
        $integer = gmp_and($value, $mask);

        return $integer;
    }

    public function decHex($dec, $len = 0): string
    {
        if (!$dec instanceof \GMP) {
            $dec = gmp_init($dec, 10);
        }
        if (gmp_cmp($dec, 0) < 0) {
            throw new \Exception('Unable to convert negative integer to string');
        }

        $hex = gmp_strval($dec, 16);

        if (strlen($hex) % 2 != 0) {
            $hex = '0'.$hex;
        }
        if ($len && strlen($hex) < $len) {  // point x y 要补齐 64 位
            $hex = str_pad($hex, $len, "0", STR_PAD_LEFT);
        }

        return $hex;
    }

    public function strToInt($string)
    {
        $hex = unpack('H*', $string);

        return gmp_init($hex[1], 16);
    }
}
```

```php
// Point.php
class Point
{
    const P = "0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF";
    const A = "0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC";
    const B = "0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93";
    const N = "0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123";
    const GX = "0x32c4ae2c1f1981195f9904466a39c9948fe30bbff2660be1715a4589334c74c7";
    const GY = "0xbc3736a2f4f6779c59bdcee36b692153d0a9877cc62a474002df32e52139f0a0";

    protected $x;
    protected $y;

    protected $P;
    protected $A;
    protected $B;
    protected $N;
    protected $GX;
    protected $GY;
    protected $size;

    public function __construct(\GMP $x, \GMP $y)
    {
        $this->x = $x;
        $this->y = $y;
        $this->init();
    }

    protected function init()
    {
        $this->P = gmp_init(self::P,16);
        $this->A = gmp_init(self::A,16);
        $this->B = gmp_init(self::B,16);
        $this->N = gmp_init(self::N,16);
        $this->GX = gmp_init(self::GX,16);
        $this->GY = gmp_init(self::GY,16);
        $this->size = 256;
    }

    public function mul(\GMP $n, $isBase = true)
    {
        $zero = gmp_init(0, 10);
        $n = gmp_mod($n, $this->P);
        if (gmp_cmp($n, $zero) === 0) {
            return $this->getInfinity();
        }
        $p = $isBase ? new self($this->GX, $this->GY) : clone $this;
        /** @var Point[] $r */
        $r = [
            $this->getInfinity(), // Q
            $p// P
        ];
        $base = gmp_strval(gmp_init(gmp_strval($n), 10), 2);
        $n = strrev(str_pad($base, $this->size, '0', STR_PAD_LEFT));
        for ($i = 0; $i < $this->size; $i++) {
            $j = $n[$i];
            if($j == 1){
                $r[0] = $r[0]->add($r[1]); // r0 + r1 => p + 0 = p
            }
            $r[1] = $r[1]->getDouble();
        }
        $r[0]->checkOnLine();

        return $r[0];
    }

    public function add(Point $addend)
    {
        if ($addend->isInfinity()) {
            return clone $this;
        }

        if ($this->isInfinity()) { // 是否是无穷远点
            return clone $addend;
        }

        // x 相等
        if (gmp_cmp($addend->getX(), $this->x) === 0) {
            // y 也相等 = 倍点
            if (gmp_cmp($addend->getY(), $this->y) === 0) {
                return $this->getDouble();
            } else { // y 不相等 无穷远点
                return $this->getInfinity();
            }
        }

        $slope = $this->divMod(// λ = (y2 - y1) / (x2 - x1) (mod p)
            gmp_sub($addend->getY(), $this->y),  // y2 - y1
            gmp_sub($addend->getX(), $this->x)  // x2 - x1
        );
        // λ² - x1 - x2
        $xR =  $this->subMod(gmp_sub(gmp_pow($slope, 2), $this->x), $addend->getX());
        // (λ(x1 - x3)-y1)
        $yR = $this->subMod(gmp_mul($slope, gmp_sub($this->x, $xR)), $this->y);

        return new self($xR, $yR);
    }

    public function getDouble()
    {
        if ($this->isInfinity()) {
            return $this->getInfinity();
        }
        $threeX2 = gmp_mul(gmp_init(3, 10), gmp_pow($this->x, 2)); // 3x²
        $tangent = $this->divMod( // λ = (3x² + a) / 2y (mod p)
            gmp_add($threeX2, $this->A),  // 3x² + a
            gmp_mul(gmp_init(2, 10), $this->y)  // 2y
        );
        $x3 = $this->subMod(  // λ² - 2x (mod p)
            gmp_pow($tangent, 2), // λ²
            gmp_mul(gmp_init(2, 10), $this->x) // 2x
        );
        $y3 = $this->subMod( // λ(x - x3)-y  (mod p)
            gmp_mul($tangent, gmp_sub($this->x, $x3)), // λ(x - x3)
            $this->y
        );

        return new self($x3, $y3);
    }

    public function getInfinity()
    {
        return new self(gmp_init(0,10), gmp_init(0,10));
    }

    /**
     * @return \GMP
     */
    public function getX()
    {
        return $this->x;
    }

    /**
     * @return \GMP
     */
    public function getY()
    {
        return $this->y;
    }

    public function isInfinity()
    {
        return gmp_cmp($this->x, gmp_init(0,10)) === 0
            && gmp_cmp($this->y, gmp_init(0,10)) === 0;
    }

    /**
     * // k ≡ (x/y) (mod n) => ky ≡ x (mod n) => k y/x ≡ 1 (mod n)
     * @param $x
     * @param $y
     * @param null $n
     * @return \GMP|resource
     */
    protected function divMod($x, $y, $n = null)
    {
        $n = $n?:$this->P;
        // y k ≡ 1 (mod n) => k ≡ 1/y (mod n)
        $k = gmp_invert($y, $n);
        // kx ≡ x/y (mod n)
        $kx = gmp_mul($x, $k);

        return gmp_mod($kx, $n);
    }

    protected function subMod($x, $y, $n = null)
    {
       return gmp_mod(gmp_sub($x, $y), $n?:$this->P);
    }

    public function contains(\GMP $x, \GMP $y)
    {
        $eq_zero = gmp_cmp(
            $this->subMod(
                gmp_pow($y, 2),
                gmp_add(
                    gmp_add(
                        gmp_pow($x, 3),
                        gmp_mul($this->A, $x)
                    ),
                    $this->B
                )
            ),
            gmp_init(0, 10)
        );

        return $eq_zero;
    }

    public function checkOnLine()
    {
        if($this->contains($this->x, $this->y) !== 0){
            throw new \Exception('Invalid point');
        }

        return true;
    }
}
```

```php
// PrivateKey.php
use FG\ASN1\ASNObject;
use FG\ASN1\Identifier;

class PrivateKey
{
    const X509_ECDSA_OID = "1.2.840.10045.2.1"; // x509 证书 oid
    const SECP_256SM2_OID = '1.2.156.10197.1.301'; // sm2 oid
    protected $key;
    protected $pubKey;

    /**
     * @param string $binaryData
     * @return Point
     * @throws \FG\ASN1\Exception\ParserException
     */
    public function parse($binaryData)
    {
        $asnObject = ASNObject::fromBinary($binaryData);
        $children = $asnObject->getChildren();
        if ($asnObject->getType() !== Identifier::SEQUENCE) {
            throw new \RuntimeException('Invalid data.');
        }
        /** @var Sequence $asnObject */
        if ($asnObject->getNumberofChildren() != 3) {
            throw new \RuntimeException('Invalid data.');
        }
        $oid = $children[1]->getContent()[1];
        $bin = hex2bin($children[2]->getContent());
        $otherAsn = ASNObject::fromBinary($bin);
        $otherChildren = $otherAsn->getChildren();
        $version = $otherChildren[0]; // 版本
        $this->setKey($otherChildren[1]->getContent());// 私钥
    }

    public function setKey($key)
    {
        $this->key = gmp_init($key, 16);  // 私钥;
    }

    public function getKey()
    {
        return $this->key;
    }

    protected function parseUncompressedPoint($data)
    {
        if (substr($data, 0, 2) != '04') {
            throw new \InvalidArgumentException('Invalid data: only uncompressed keys are supported.');
        }
        $data = substr($data, 2);
        $dataLength = strlen($data);

        $x = gmp_init(substr($data, 0, $dataLength / 2), 16);
        $y = gmp_init(substr($data, $dataLength / 2), 16);

        return [$x, $y];
    }

    public function getPublickKey()
    {
        if($this->pubKey){
            return $this->pubKey;
        }
        $point = new Point(gmp_init(0), gmp_init(0));
        $pubPoint = $point->mul($this->key, true);
        $pubKey = new PublicKey();
        $pubKey->setPoint($pubPoint);
        $this->pubKey = $pubKey;

        return $pubKey;
    }
}
```

```php
// PublicKey
use FG\ASN1\ASNObject;
use FG\ASN1\Identifier;

class PublicKey
{
    const X509_ECDSA_OID = "1.2.840.10045.2.1"; // x509 证书 oid
    const SECP_256SM2_OID = '1.2.156.10197.1.301'; // sm2 oid

    /** @var Point */
    protected $point;

    /**
     * @return mixed
     */
    public function getPoint()
    {
        return $this->point;
    }

    /**
     * @param mixed $point
     */
    public function setPoint(Point $point)
    {
        $this->point = $point;
    }


    /**
     * 公钥格式
    SEQUENCE {
        SEQUENCE {
            OBJECT IDENTIFIER (1.2.840.10045.2.1)
            OBJECT IDENTIFIER (1.2.156.10197.1.301)
        }
        BIT STRING (坐标点)
    }
     * @param string $binaryData
     * @return Point
     * @throws \FG\ASN1\Exception\ParserException
     */
    public function parse($binaryData)
    {
        $asnObject = ASNObject::fromBinary($binaryData);
        if ($asnObject->getType() !== Identifier::SEQUENCE) {
            throw new \RuntimeException('Invalid data.');
        }

        $children = $asnObject->getChildren();
        if (count($children) != 2) {
            throw new \RuntimeException('Invalid data.');
        }

        if (count($children[0]->getChildren()) != 2) {
            throw new \RuntimeException('Invalid data.');
        }

        if ($children[0]->getChildren()[0]->getType() !== Identifier::OBJECT_IDENTIFIER) {
            throw new \RuntimeException('Invalid data.');
        }

        if ($children[0]->getChildren()[1]->getType() !== Identifier::OBJECT_IDENTIFIER) {
            throw new \RuntimeException('Invalid data.');
        }

        if ($children[1]->getType() !== Identifier::BITSTRING) {
            throw new \RuntimeException('Invalid data.');
        }

        $oid = $children[0]->getChildren()[0];
        $curveOid = $children[0]->getChildren()[1];
        $encodedKey = $children[1];
        if ($oid->getContent() !== self::X509_ECDSA_OID) {
            throw new \RuntimeException('Invalid data: non X509 data.');
        }

        if ($curveOid->getContent() !== self::SECP_256SM2_OID) {
            throw new \RuntimeException('Invalid data: non sm2 data.');
        }
        list($x, $y) = $this->parseUncompressedPoint($encodedKey->getContent());
        $this->setPoint(new Point($x, $y));
    }

    public function parseUncompressedPoint($data)
    {
        if (substr($data, 0, 2) != '04') {
            throw new \InvalidArgumentException('Invalid data: only uncompressed keys are supported.');
        }
        $data = substr($data, 2);
        $dataLength = strlen($data);
        if ($dataLength != 128) {
            throw new \InvalidArgumentException('Invalid Public Key length');
        }
        $x = gmp_init(substr($data, 0, $dataLength / 2), 16);
        $y = gmp_init(substr($data, $dataLength / 2), 16);
        $this->setPoint(new Point($x, $y)); //test
        
        return [$x, $y];
    }
}
```

```php
// sm2.php
require_once 'Util.php';
require_once 'Point.php';
require_once 'PublicKey.php';
require_once 'PrivateKey.php';
require_once 'Sm3.php';

class Sm2
{
    use Util;
    protected $sm3;

    public function __construct()
    {
        $this->sm3 = new Sm3();
    }

    public function pubEncrypt(PublicKey $publicKey, $data)
    {
        $point = $publicKey->getPoint();
        $t = '';
        while (!$t){
            $k = $this->generate(); // 随机数
            // $k = gmp_init('74689821225634928628057736695642952596354672349967165733607647475567920739952',10);
            $kG = $point->mul($k);
            $x1 = $this->decHex($kG->getX(), 64);
            $y1 = $this->decHex($kG->getY(), 64);
            $c1 = $x1.$y1;
            $kPb = $point->mul($k, false);
            $x2 = $this->decHex($kPb->getX(), 64);
            $y2 = $this->decHex($kPb->getY(), 64);
            $t = $this->kdf($x2.$y2, strlen($data));
        }
        $strHex = bin2hex($data);
        // $c2 = gmp_xor(gmp_init($t, 16),  gmp_init($strHex, 16));
        $c2 = gmp_xor(gmp_init($t, 16),  gmp_init($strHex, 16));
        $c2 = $this->decHex($c2);
        $c3 = $this->sm3->sign(hex2bin($x2.$strHex.$y2));
        //  $encryptData = "04".$c1.$c3.$c2;
        $encryptData = "04".$c1.$c2.$c3;

        return $encryptData;
    }
    protected function kdf($z, $klen)
    {
        $res = '';
        $ct = 1;
        $j = ceil($klen / 32);
        for ($i = 0; $i < $j; $i++) {
            $hex = $this->sm3->sign(hex2bin($z . $this->decHex($ct, 8)));
            if ($i + 1 == $j && $klen % 32 != 0) {  // 最后一个 且 $klen/$v 不是整数
                $res .= substr($hex, 0, ($klen % 32) * 2); // 16进制比byte长度少一半 要乘2
            } else {
                $res .= $hex;
            }
            $ct++;
        }

        return $res;
    }
    // c1 c2 c3
    public function decrypt(PrivateKey $privateKey,$data)
    {
        $decodeData = substr($data, 2);
        // 取出 c1
        $c1 = substr($decodeData, 0,128); // 转成16进制后 点数据长度要乘以2
        $x1 = substr($c1, 0,64);
        $y1 = substr($c1, 64);
        $dbC1 = (new Point(gmp_init($x1, 16), gmp_init($y1,16)))->mul($privateKey->getKey(), false);
        $x2 = $this->decHex($dbC1->getX(), 64);
        $y2 = $this->decHex($dbC1->getY(), 64);
        $len = strlen($decodeData) - 128 - 64;
        $t = $this->kdf($x2 . $y2, $len / 2);  // 转成16进制后 字符长度要除以2

        $c2 = substr($decodeData,128, $len);
        $m1 = $this->decHex(gmp_xor(gmp_init($t, 16), gmp_init($c2, 16)));
        $u = $this->sm3->sign(hex2bin($x2.$m1.$y2));
        $c3 = substr($decodeData, -64); // 验证hash数据
        if(strtoupper($u) != strtoupper($c3)){
            throw new \Exception("error decrypt data");
        }
        // $m1 如果是16进制数 hex2bin,否则直接返回
        //  return $m1;
        //  return pack("H*",$m1);
        return hex2bin($m1);
    }

    // c1 c3 c2
    public function decrypt2(PrivateKey $privateKey,$data)
    {
        $decodeData = substr($data, 2);
        // 取出 c1
        $c1 = substr($decodeData, 0,128); // 转成16进制后 点数据长度要乘以2
        $x1 = substr($c1, 0,64);
        $y1 = substr($c1, 64);
        $dbC1 = (new Point(gmp_init($x1, 16), gmp_init($y1,16)))->mul($privateKey->getKey(), false);
        $x2 = $this->decHex($dbC1->getX(), 64);
        $y2 = $this->decHex($dbC1->getY(), 64);
        $len = strlen($decodeData) - 128 - 64;
        $t = $this->kdf($x2 . $y2, $len / 2);  // 转成16进制后 字符长度要除以2
        $c2 = substr($decodeData, -$len);
        $m1 = $this->decHex(gmp_xor(gmp_init($t, 16), gmp_init($c2, 16)));
        $u = $this->sm3->sign(hex2bin($x2.$m1.$y2));
        $c3 = substr($decodeData, 128,64); // 验证hash数据
        if(strtoupper($u) != strtoupper($c3)){
            throw new \Exception("error decrypt data");
        }
        // $m1 如果是16进制数 hex2bin,否则直接返回
        //  return $m1;
        //  return pack("H*",$m1);
        return hex2bin($m1);
    }
}

//------FOR TEST-------------------------------------
// 直接请求该PHP，运行测试代码
// SM2 测试密钥
// pri: aec335da1f2bb072f5d224395c6d4d4d2b4ad8dd58d673333b0b1489b73ef7af
// pub: 97f13aa1f35bb24a675cacdd7ed3da1b54ce9ca056a3d84f555c0219187bc6d8bd8e47f8a20750a91e7ef8b77381bc865db61733ddc447a386cc0d8454d0ec8f
if (strcasecmp(basename($_SERVER['SCRIPT_NAME']), basename(__FILE__)) == 0)
{
    function msectime() {
        list($msec, $sec) = explode(' ', microtime());
        $msectime = (float)sprintf('%.0f', (floatval($msec) + floatval($sec)) * 1000);
        return $msectime;
    }
    $pubKey = new PublicKey();
    $pubKey->parseUncompressedPoint('04'.'97f13aa1f35bb24a675cacdd7ed3da1b54ce9ca056a3d84f555c0219187bc6d8bd8e47f8a20750a91e7ef8b77381bc865db61733ddc447a386cc0d8454d0ec8f');

    $data = '1234567812345678';
    $sm2 = new Sm2();
    $begin = msectime();
    $re = $sm2->pubEncrypt($pubKey, $data);
    echo "time:".(msectime() - $begin)."\n";
    echo "sm2Enc:".$re."\n";

    $begin = msectime();
    $priKey = new PrivateKey();
    $priKey->setKey('aec335da1f2bb072f5d224395c6d4d4d2b4ad8dd58d673333b0b1489b73ef7af');
    $re = $sm2->decrypt($priKey, $re);
    echo "time:".(msectime() - $begin)."\n";
    echo "sm2Dec:".$re."\n";

    // win命令行工具校对
    // sm2_dec rsM12h8rsHL10iQ5XG1NTStK2N1Y1nMzOwsUibc+968= BCv7g8MNwSRZckz4CwOaKEE/MIqInnxlniIWdFdF+ZDvG/Pnht+Vfo+oL8Hm+VHjH1gU9coRE/KN0U4c4mcef6lhmaBYjDb+tasrg7fg0AkW3bFsOE4CKWvA8VWbFSMZFh6h77F8Pew49qJCmVEl7FQ=
    // echo "sm2_dec ".base64_encode(hex2bin('aec335da1f2bb072f5d224395c6d4d4d2b4ad8dd58d673333b0b1489b73ef7af')).' '.base64_encode(hex2bin($re));
}
```
