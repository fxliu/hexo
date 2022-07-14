---
title: rknn
tags: 
    - rknn
categories: 
    - Android
description: rknn
date: 2022-07-14 17:46:43
updated: 2022-07-14 17:46:43
---

## 环境搭建

+ [InsightFace-REST](https://github.com/SthPhoenix/InsightFace-REST)
  + 获取人证模板库 - w600k_r50
+ 瑞芯微-RKNN
  + [rknn-toolkit](https://github.com/rockchip-linux/rknn-toolkit)
  + [rknn-toolkit2](https://github.com/rockchip-linux/rknn-toolkit2)
    + doc\Rockchip_Quick_Start_RKNN_Toolkit2_CN-1.3.0
  + [rknpu2](https://github.com/rockchip-linux/rknpu2)
    + doc\Rockchip_Quick_Start_RKNN_SDK_V1.3.0_CN.pdf
  + [瑞芯微3568J](https://wiki.t-firefly.com/Core-3568J/usage_npu.html)
  + [rknn使用](https://wiki.t-firefly.com/zh_CN/CORE-1126-JD4/rknn.html)
+ 资料
  + [瑞芯微转化人脸识别模型](https://blog.csdn.net/ZuoSeDiao/article/details/124245510)
  + [YOLOv5-RK3399Pro](https://github.com/littledeep/YOLOv5-RK3399Pro)

```shell
# rknpu 提供的python环境是linux版本，需要在linux下执行
# ubuntu 20.04_x64 - 必须是python 3.8
# 实际部署换使用 rknn-toolkit2-1.3.0_no_docker + python环境
```

## YOLOv5

* 
* 基于COCO数据集预训练的物体检测架构和模型
* 物体检测预训练方法 - 可用于训练物体检测，例如人脸
* 官方提供的基于COCO训练结果，包含80种物体分类识别

* 口罩检测训练: 
  * https://blog.csdn.net/Blueeyedboy521/article/details/125658327
  * https://blog.csdn.net/didiaopao/article/details/119954291

```sh
```



## ONNX

* 推理模型

## 转换

* [netron](https://netron.app/)
  * 查看模型的输入及输出
  * inputs
    * type: float32[None, 3, 112, 112]
    * 应该是指3通道，112*112 图片
  * outputs
    * name: 683
    * type: float32[1, 512]
* config 参数说明
  * mean_values: 输入的均值
    * [[128, 128, 128]] 表示一个输入的3通道的值减去128
  * std_values: 输入的归一化值
    * [[128, 128, 128]] 表示设置一个输入的三个通道的值减去均值后在除以128。
