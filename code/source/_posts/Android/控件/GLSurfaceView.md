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

## 坐标系

+ 世界坐标系是以屏幕中心为原点(0, 0, 0)，且是始终不变的。
  + x轴正方向为屏幕从左向右，y轴正方向为屏幕从下向上，z轴正方向为屏幕从里向外。
  + 长度单位这样来定：窗口范围按此单位恰好是(-1,-1)到(1,1)，即屏幕左下角坐标为（-1，-1），右上角 坐标为（1,1）
+ 顶点坐标 是世界坐标系
+ 纹理坐标 是本地坐标系, 左下角是(0, 0, 0), 右上角是(1, 1, 0)

## Demo

[OpenCamera](https://github.com/moo611/opencamera-for-android)
+ 基于opengles+glsurfaceview,能实现实时滤镜，拍照，录制短视频，美颜磨皮等功能
[AndroidOpenGLDemo](https://github.com/doggycoder/AndroidOpenGLDemo)
+ 基础应用的各种效果集合
[lib_essurface](svn\esface\trunk\Android\libs\lib_essurface)
