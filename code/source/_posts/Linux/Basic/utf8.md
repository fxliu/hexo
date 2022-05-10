---
title: UNICODE
tags: 
  - UNICODE
categories: 
  - linux
description: UNICODE
date: 2020-10-25 16:19:46
updated: 2020-10-25 16:19:46
---

## UNICODE UTF8 互转

```cpp
int enc_unicode_to_utf8_one(unsigned long unic, unsigned char* pOutput, int outSize)
{
    if (outSize < 6)
        return 0;
    if (unic <= 0x0000007F)
    {
        // * U-00000000 - U-0000007F:  0xxxxxxx
        *pOutput = (unsigned char)(unic & 0x7F);
        return 1;
    }
    else if (unic >= 0x00000080 && unic <= 0x000007FF)
    {
        // * U-00000080 - U-000007FF:  110xxxxx 10xxxxxx
        *(pOutput + 1) = (unsigned char)(unic & 0x3F) | 0x80;
        *pOutput = (unsigned char)((unic >> 6) & 0x1F) | 0xC0;
        return 2;
    }
    else if (unic >= 0x00000800 && unic <= 0x0000FFFF)
    {
        // * U-00000800 - U-0000FFFF:  1110xxxx 10xxxxxx 10xxxxxx
        *(pOutput + 2) = (unsigned char)(unic & 0x3F) | 0x80;
        *(pOutput + 1) = (unsigned char)((unic >> 6) & 0x3F) | 0x80;
        *pOutput = (unsigned char)((unic >> 12) & 0x0F) | 0xE0;
        return 3;
    }
#ifdef UC4
    else if (unic >= 0x00010000 && unic <= 0x001FFFFF)
    {
        // * U-00010000 - U-001FFFFF:  11110xxx 10xxxxxx 10xxxxxx 10xxxxxx
        *(pOutput + 3) = (unsigned char)(unic & 0x3F) | 0x80;
        *(pOutput + 2) = (unsigned char)((unic >> 6) & 0x3F) | 0x80;
        *(pOutput + 1) = (unsigned char)((unic >> 12) & 0x3F) | 0x80;
        *pOutput = (unsigned char)((unic >> 18) & 0x07) | 0xF0;
        return 4;
    }
    else if (unic >= 0x00200000 && unic <= 0x03FFFFFF)
    {
        // * U-00200000 - U-03FFFFFF:  111110xx 10xxxxxx 10xxxxxx 10xxxxxx 10xxxxxx
        *(pOutput + 4) = (unsigned char)(unic & 0x3F) | 0x80;
        *(pOutput + 3) = (unsigned char)((unic >> 6) & 0x3F) | 0x80;
        *(pOutput + 2) = (unsigned char)((unic >> 12) & 0x3F) | 0x80;
        *(pOutput + 1) = (unsigned char)((unic >> 18) & 0x3F) | 0x80;
        *pOutput = (unsigned char)((unic >> 24) & 0x03) | 0xF8;
        return 5;
    }
    else if (unic >= 0x04000000 && unic <= 0x7FFFFFFF)
    {
        // * U-04000000 - U-7FFFFFFF:  1111110x 10xxxxxx 10xxxxxx 10xxxxxx 10xxxxxx 10xxxxxx
        *(pOutput + 5) = (unsigned char)(unic & 0x3F) | 0x80;
        *(pOutput + 4) = (unsigned char)((unic >> 6) & 0x3F) | 0x80;
        *(pOutput + 3) = (unsigned char)((unic >> 12) & 0x3F) | 0x80;
        *(pOutput + 2) = (unsigned char)((unic >> 18) & 0x3F) | 0x80;
        *(pOutput + 1) = (unsigned char)((unic >> 24) & 0x3F) | 0x80;
        *pOutput = (unsigned char)((unic >> 30) & 0x01) | 0xFC;
        return 6;
    }
#endif

    return 0;
}
std::string enc_unicode_to_utf8(std::wstring in)
{
    std::string out;
    for (size_t i = 0; i < in.size(); i++) {
        unsigned char szTmp[8] = { 0 };
        if (enc_unicode_to_utf8_one(in.at(i), szTmp, 8) == 0)
            szTmp[0] = (char)in.at(i);
        out.append((char*)szTmp);
    }
    return out;
}
int enc_get_utf8_size(const unsigned char ch)
{
    if (ch <= 0x7F)     return 1;    // 0xxxxxxx
    else if (ch < 0xC0) return 1;    //
    else if (ch < 0xE0) return 2;    // 110xxxxx
#ifdef UC4
    else if (ch < 0xF0)    return 3;  // 1110xxxxx
    else if (ch < 0xF8)    return 4;  // 11110xxx
    else if (ch < 0xFC)    return 5;  // 111110xx
    else if (ch >= 0xFC) return 6;    // 1111110x
#else
    else if (ch >= 0xE0)    return 3; // 1110xxxxx
    #endif
    return 0;
}
int enc_utf8_to_unicode_one(const unsigned char* pInput, unsigned long* Unic)
{
    // b1 表示UTF-8编码的pInput中的高字节, b2 表示次高字节, ...
    char b1, b2, b3, b4, b5, b6;
    int utfbytes = enc_get_utf8_size(*pInput);
    unsigned char* pOutput = (unsigned char*)Unic;

    switch (utfbytes)
    {
    case 0:
        *pOutput = *pInput;
        utfbytes += 1;
        break;
    case 2:
        b1 = *pInput;
        b2 = *(pInput + 1);
        if ((b2 & 0xC0) != 0x80)
            return 0;
        *pOutput = (unsigned char)((b1 << 6) + (b2 & 0x3F));
        *(pOutput + 1) = (unsigned char)((b1 >> 2) & 0x07);
        break;
    case 3:
        b1 = *pInput;
        b2 = *(pInput + 1);
        b3 = *(pInput + 2);
        if (((b2 & 0xC0) != 0x80) || ((b3 & 0xC0) != 0x80))
            return 0;
        *pOutput = (unsigned char)((b2 << 6) + (b3 & 0x3F));
        *(pOutput + 1) = (unsigned char)((b1 << 4) + ((b2 >> 2) & 0x0F));
        break;
#ifdef UC4
    case 4:
        b1 = *pInput;
        b2 = *(pInput + 1);
        b3 = *(pInput + 2);
        b4 = *(pInput + 3);
        if (((b2 & 0xC0) != 0x80) || ((b3 & 0xC0) != 0x80)
            || ((b4 & 0xC0) != 0x80))
            return 0;
        *pOutput = (unsigned char)((b3 << 6) + (b4 & 0x3F));
        *(pOutput + 1) = (unsigned char)((b2 << 4) + ((b3 >> 2) & 0x0F));
        *(pOutput + 2) = (unsigned char)(((b1 << 2) & 0x1C) + ((b2 >> 4) & 0x03));
        break;
    case 5:
        b1 = *pInput;
        b2 = *(pInput + 1);
        b3 = *(pInput + 2);
        b4 = *(pInput + 3);
        b5 = *(pInput + 4);
        if (((b2 & 0xC0) != 0x80) || ((b3 & 0xC0) != 0x80)
            || ((b4 & 0xC0) != 0x80) || ((b5 & 0xC0) != 0x80))
            return 0;
        *pOutput = (unsigned char)((b4 << 6) + (b5 & 0x3F));
        *(pOutput + 1) = (unsigned char)((b3 << 4) + ((b4 >> 2) & 0x0F));
        *(pOutput + 2) = (unsigned char)((b2 << 2) + ((b3 >> 4) & 0x03));
        *(pOutput + 3) = (unsigned char)(b1 << 6);
        break;
    case 6:
        b1 = *pInput;
        b2 = *(pInput + 1);
        b3 = *(pInput + 2);
        b4 = *(pInput + 3);
        b5 = *(pInput + 4);
        b6 = *(pInput + 5);
        if (((b2 & 0xC0) != 0x80) || ((b3 & 0xC0) != 0x80)
            || ((b4 & 0xC0) != 0x80) || ((b5 & 0xC0) != 0x80)
            || ((b6 & 0xC0) != 0x80))
            return 0;
        *pOutput = (unsigned char)((b5 << 6) + (b6 & 0x3F));
        *(pOutput + 1) = (unsigned char)((b5 << 4) + ((b6 >> 2) & 0x0F));
        *(pOutput + 2) = (unsigned char)((b3 << 2) + ((b4 >> 4) & 0x03));
        *(pOutput + 3) = (unsigned char)(((b1 << 6) & 0x40) + (b2 & 0x3F));
        break;
#endif
    default:
        return 0;
        break;
    }

    return utfbytes;
}
std::wstring enc_utf8_to_unicode(std::string in)
{
    std::wstring out;
    const unsigned char* tmp = (const unsigned char*)in.data();
    for (size_t i = 0; i < in.size();) {
        unsigned long w[3] = { 0 };
        int len = enc_utf8_to_unicode_one(tmp, w);
        if (len == 0) {
            w[0] = *tmp;
            len = 1;
        }
        out.append((wchar_t*)w);
        tmp += len;
        i += len;
    }
    return out;
}

int main()
{
    setlocale(LC_ALL, "zh_CN.UTF-8");

    std::wstring str = L"UNICODE UTF8 互转";

    std::string out = enc_unicode_to_utf8(str);
    // printf("%s\n", out.data());

    std::wstring w1 = enc_utf8_to_unicode(out);
    out = enc_unicode_to_utf8(w1);
    printf("%s\n", out.data());

    return 0;
}
```
