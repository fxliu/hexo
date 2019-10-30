---
title: HOOK键盘钩子
tags: 
  - HOOK
categories: 
  - VC
description: HOOK, 钩子
date: 2019-10-27 ‏‎15:35:33
updated: 2019-10-27 ‏‎15:35:33
---

## 键盘钩子

+ `WH_KEYBOARD_LL`：全局键盘钩子
  + 不需要封装DLL，EXE中直接钩挂即可
  + `WH_KEYBOARD`：需要DLL封装模式使用
+ `WH_MOUSE_LL`：鼠标钩子，使用方式同键盘钩子
  + `WH_KEYBOARD`: DLL模式
  + DLL导出`HOOKPROC`函数
  + EXE加载DLL后，SetWindowsHookEx安装即可

```C++
// EXE模式
// 挂在钩子
m_hHook = SetWindowsHookEx(WH_KEYBOARD_LL, LowLevelKeyboardProc, 0, 0);
// 卸载钩子
UnhookWindowsHookEx(m_hHook);
// 键盘事件处理
LRESULT CALLBACK LowLevelKeyboardProc(int nCode, WPARAM wParam, LPARAM lParam)
{
  if (nCode == HC_ACTION)
  {
    switch (wParam)
    {
    case WM_KEYDOWN:
    case WM_SYSKEYDOWN:
    case WM_KEYUP:
    case WM_SYSKEYUP:
      PKBDLLHOOKSTRUCT p = (PKBDLLHOOKSTRUCT)lParam;
      if (p->vkCode == VK_ESCAPE && GetAsyncKeyState(VK_CONTROL) & 0x8000 && GetAsyncKeyState(VK_SHIFT) & 0x8000) {
        std::cout << "Ctrl+Shift+Esc" << std::endl;
        // 返回1代表终止
        return 1;
      }
      else if (p->vkCode == VK_ESCAPE && GetAsyncKeyState(VK_CONTROL) & 0x8000) {
        std::cout << "Ctrl+Esc" << std::endl;
        return 1;
      }
      break;
    }
  }
  // 其他常规事件一定要继续传递下去
  return CallNextHookEx(NULL, nCode, wParam, lParam);
}
// 注意钩子线程不能阻塞，可以内置消息循环，确保钩子有效
MSG msg;
while (!GetMessage(&msg, NULL, NULL, NULL) && pThis->m_hHook)
{
  //TranslateMessage(&msg);
  //DispatchMessage(&msg);
  break;
}
```

```C++
// DLL模块方式
// ------------------------------------------------------------------
// DLL导出函数
// 全局共享段，用户DLL公共数据处理，可以根据自己需要增删
#pragma data_seg("SHARED")
static HHOOK g_hHook = NULL;  // 钩子句柄, 便于卸载
static HWND g_hookWnd = NULL;  // 调用DLL的主窗口句柄, 这样就可以SendMessage给主窗口鼠标消息及其参数
#pragma data_seg()
#pragma comment(linker,"/section:SHARED,rws")
// 钩子回调函数
LRESULT CALLBACK MouseProc(int nCode, WPARAM wParam, LPARAM lParam)
{
  // 有鼠标消息时，将其发给主程序
  if (g_hookWnd != NULL && nCode == HC_ACTION)
  {
    // 自定义消息
    ::SendMessage(g_hookWnd, WM_HOOKMSG, wParam, lParam);
  }
  // 常规事件继续传递: g_hook 可以给NULL
  return CallNextHookEx(g_hHook, nCode, wParam, lParam);
}
// 其他辅助导出函数
BOOL SetHwnd(HWND hwnd, HHOOK hHook)
{
  g_hookWnd = hwnd;
  g_hHook = hHook;
  return TRUE;
}
// .def 内容
LIBRARY
EXPORTS
  MouseProc
  SetHwnd
// ------------------------------------------------------------------
// EXE 加载部分
// 加载DLL
HMODULE hModule = LoadLibrary(GetRunPath() + TEXT("\\HookDll.dll"));
PSetHwnd pSetHwnd = (PSetHwnd)GetProcAddress(hModule, "SetHwnd");
HOOKPROC mouseProc = (HOOKPROC)GetProcAddress(hModule, "MouseProc");
if (!pSetHwnd || !mouseProc)
{
  return FALSE;
}
// 安装
HHOOK hHook = NULL;
// 0代表全局
hHook = SetWindowsHookEx(WH_MOUSE, mouseProc, hModule, 0);
if (hHook)
{
  SetWindowText(g_static, TEXT("SetWindowsHookEx Success"));
  // 把句柄设置进去是为了方便回传数据
  pSetHwnd(g_hwnd, hHook);
}
else
  SetWindowText(g_static, TEXT("SetWindowsHookEx Fail"));
// 卸载
FreeLibrary(hModule);
if (hHook)
  UnhookWindowsHookEx(hHook);

```

## 备注

+ EXE模式仍然依赖于消息机制，调用`SetWindowsHookEx`的线程不可被阻塞，否则会导致钩子无效，系统所有按键事件被延迟处理
+ Exe需要管理员权限

## Demo

[HOOK](https://github.com/fxliu/VCDemo/tree/master/HOOK/KeyboardHook)包含一个EXE方式键盘钩子和一个DLL模块方式鼠标钩子
`https://github.com/fxliu/VCDemo/tree/master/HOOK/KeyboardHook`
EXE方式比DLL方式便捷的多，但貌似DLL模块方式速度比较快
