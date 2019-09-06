---
title: HOOK键盘钩子
tags: 
  - HOOK
categories: 
  - VC
---

## 键盘钩子

```C++
// winuser.h (include Windows.h)
m_hHook = SetWindowsHookEx(WH_KEYBOARD_LL, LowLevelKeyboardProc, 0, 0);
```

## 备注


## Demo

[FFmpeg+SDL播放器](https://github.com/fxliu/VCDemo/tree/master/TOOLS/ffmpeg+SDL)
`https://github.com/fxliu/VCDemo/tree/master/TOOLS/ffmpeg+SDL`
