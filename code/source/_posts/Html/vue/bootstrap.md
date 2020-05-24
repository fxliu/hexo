---
title: element-ui
tags: 
  - element-ui
categories: 
  - JS
  - vue
description: element-ui
date: 2020-04-04 20:59:46
updated: 2020-04-04 20:59:46
---

## 组件默认属性

```css
textarea:focus {
    outline:none;   /*去掉自带外边框，点击变色问题*/
}
```

## 对齐

```css
/* 工具类：文本 */
text-justify: 组件对齐
text-left | text-center | text-right: 左右定位
text-wrap | text-nowrap: 多行定位
/* 垂直对齐 */
align-baseline | align-top | align-middle | align-bottom | align-text-top | align-text-bottom
```

## flex

```html
<!-- 工具类：flex布局 -->
<div class="d-flex" bc="x99">宽度：100%</div>
<div class="d-inline-flex" bc="xff">宽度：auto</div>

<div class="d-flex flex-column" bc="x99">
    <div>单行：左右</div>
    <div>justify-content-start：居左</div>
    <div>justify-content-end：居右</div>
    <div>justify-content-between：两端</div>
    <div>justify-content-around：两端留空</div>
</div>

<div class="d-flex flex-column" bc="xff">
    <div>单行：上下</div>
    <div>align-items-start：居上</div>
    <div>align-items-end：居下</div>
    <div>align-items-centern：居中</div>
    <div>align-items-baseline：基线对齐</div>
    <div>align-items-stretch：拉伸：高度占满</div>
</div>

<div class="d-flex flex-column" bc="x99">
    <div>子元素自身：上下</div>
    <div>align-self-start：居上</div>
    <div>align-self-end：居下</div>
    <div>align-self-centern：居中</div>
    <div>align-self-baseline：基线对齐</div>
    <div>align-self-stretch：拉伸：高度占满</div>
    <div>子元素自身：左右</div>
    <div>flex-fill：根据子内容计算子元素宽度比例</div>
    <div>flex-grow-1：占满剩余空间</div>
    <div>flex-shrink-1: 子元素占两行</div>
    <div>子元素：上下弹簧</div>
    <div>mb-auto：底部弹簧</div>
    <div>mt-auto：顶端弹簧</div>
</div>

<div class="d-flex flex-column" bc="xff">
    <div>flex-nowrap: 强制单行</div>
    <div>flex-wrap: 多行</div>
    <div>多行：上下</div>
    <div>align-content-start: 多行居上</div>
    <div>align-content-end: 多行居下</div>
    <div>align-content-center: 多行居中</div>
    <div>align-content-between: 多行两端</div>
    <div>align-content-around: 多行均分-两端留白</div>
    <div>align-content-stretch: 多行拉伸</div>
</div>
```
