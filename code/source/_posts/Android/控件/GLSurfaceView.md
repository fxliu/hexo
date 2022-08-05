---
title: GLSurfaceView
tags: 
    - GLSurfaceView
categories: 
    - Android
description: GLSurfaceView
date: 2022-08-04 17:41:24
updated: 2022-08-04 17:41:24
---

## 说明

[LearnOpenGL-中文](https://learnopengl-cn.github.io/)
[LearnOpenGL-GitHub](https://github.com/LearnOpenGL-CN/LearnOpenGL-CN)
[开发者文档: opengl](https://developer.android.google.cn/guide/topics/graphics/opengl)

+ 构建OpenGL ES环境：关键元素
  + [GLSurfaceView](https://developer.android.google.cn/reference/android/opengl/GLSurfaceView)
    + 继承SurfaceView，专用于OpenGL渲染
  + [GLSurfaceView.Renderer](https://developer.android.google.cn/reference/android/opengl/GLSurfaceView.Renderer)
    + 渲染器接口
    + 渲染器在单独的线程中运行，渲染与UI完全解耦
    + 数据直接跨线程发送给渲染器即可
