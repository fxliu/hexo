---
title: onnx
tags: 
  - onnx
categories: 
  - Python
description: onnx
date: 2022-07-27 16:38:57
updated: 2022-07-27 16:38:57
---

## onnx

+ 在线查看：https://netron.app/

```sh
pip install onnx
pip install onnxruntime
```

## 

```py
import onnx

# 加载模型
model = onnx.load('centerface.onnx')
# 检查模型格式是否完整及正确
onnx.checker.check_model(model)
# 获取输入/输出层，包含层名称、维度信息
print(model.graph.input[0])
print(model.graph.output)
```
