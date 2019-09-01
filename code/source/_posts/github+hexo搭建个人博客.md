---
title: github+hexo搭建个人博客
tags: 
  - hexo
  - github 
categories: 
  - 博客
---

+ [Hexo官网](https://hexo.io/)
+ [Hexo中文网](https://hexo.io/zh-cn/docs/)

- - -

## nodejs

+ 官网[下载](http://nodejs.cn/download/ "中文网")安装最新版即可
+ [淘宝cnpm镜像](https://npm.taobao.org/)
  + `npm install -g cnpm --registry=https://registry.npm.taobao.org`
  + 备注：先装的nodejs 64位，cnpm安装失败，各种百度 - 各种尝试 - 各种不好使；卸载重装32位搞定，心都碎了。

## GitHub

+ [GitHub Desktop](https://desktop.github.com/): 桌面版，Git UI工具
+ [Git For Windows](https://gitforwindows.org/): Git命令行工具，hexo需要
+ 仓库1：[博客仓库](https://github.com/fxliu/fxliu.github.io "静态文件")静态文件部署位置
+ GitHub免费提供，申请方法问度娘，每个账号可以免费申请一个
+ 仓库2：[源码仓库](https://github.com/fxliu/hexo)hexo源码保存位置

## VSCode：编译器

+ 微软官网[下载](https://code.visualstudio.com/)安装
+ 推荐插件
  + `Ctrl+Shift+P`->`configure Display Language`安装简体中文
  + `Ctrl+Shift+P`->`Markdown All in One`
  + `Ctrl+Shift+P`->`Markdown Preview Github Styling`
    + [规则翻译](https://www.jianshu.com/p/51523a1c6fe1)

## [hexo](https://hexo.io/zh-cn/docs/)

+ 安装：`cnpm install -g hexo-cli`
+ 初始化：`hexo init 保存博客源码目录`
+ 配置：[官网中文文档](https://hexo.io/zh-cn/docs/configuration)说的很详细了
  + 然而，只需要把title什么的改成自己的就行了，其他都不用动
+ `hexo server`启动本地服务，看看效果如何

## RSS插件

+ 安装插件：`cnpm install hexo-generator-feed`
+ 启用插件：修改根目录下`_config.yml`配置文件

```yml
# Extensions
plugins:
  hexo-generator-feed

#Feed Atom
feed:
  type: atom
  path: atom.xml
  limit: 20
```

## 主题更换：推荐一个个人比较喜欢的fexo

+ [fexo](https://github.com/forsigner/fexo)，中文文档，配置方法说明也很详细
+ 我是fork到我仓库使用的
  + 打开大佬的github，点击右上角的fork按钮
  + 然后回到自己的github->Repositories，同名的仓库已经存在了，就是这么简单
+ 打开根目录的`_config.yml`，设为`theme: fexo`
+ 主题配置全部在`theme/fexo`里面完成，所以下面所有配置指的是配置`theme/fexo/_config.yml`
+ 名称`blog_name`，标语`slogan`，头像`avatar`什么的一笔带过
+ 导航，根据自己需要配置
  + 除了`archives`是和hexo的配置文件对应的，其他都是fexo自己的
  + *关键是，关键是所有fexo自己的，都需要自己敲命令启动才好使~~~*
  + 启用就好，根据提示补充头，`_config.xml`中有默认Demo

## fexo：启用分类页面

+ 根目录执行`hexo new page category`
+ 修改`my-blog/source/category/index.md`内容

```md
---
title: category
layout: category
comments: false
---
```

## fexo：启用标签页面

+ 根目录执行`hexo new page tag`
+ 修改`my-blog/source/tag/index.md`内容

```md
---
title: tag
layout: tag
comments: false
---
```

## fexo：启用友链页面

+ 根目录执行`hexo new page link`
+ 修改`my-blog/source/link/index.md`内容

```md
---
title: link
layout: link
comments: false
---
```

## fexo: 启用关于页面

+ 根目录执行`hexo new page about`
+ 修改`my-blog/source/about/index.md`内容

```md
---
title: about
layout: about
comments: false
---
```

## 启用项目页面

+ 根目录执行`hexo new page project`
+ 修改`my-blog/source/project/index.md`内容

```md
---
title: project
layout: project
comments: false
---
```

## 启用搜索页面

+ 目录执行`hexo new page search`
+ 修改`my-blog/source/search/index.md`内容

```md
---
title: search
layout: search
comments: false
---
```

+ *然后安装 Hexo 插件`hexo-search`*
  + `cd my-blog(hexo根目录)`
  + `npm install hexo-search --save`

## 安装完成，享受成果把

+ `hexo server`启动本地服务，看看效果如何
+ `hexo g`执行编译，编译结果静态文件保存到`Public`文件夹

## 部署到GitHub

+ 把`Public`下所有内容发布到博客仓库即可
  + 原理就是这么简单，如果想要自动化复制+上传，自己动手吧
  + git命令行自动提交需要配置秘钥什么的，就别问我这种准备使用GitHub Desktop工具的农民了
+ [我的成果](https://fxliu.github.io/)
+ [源码仓库](https://github.com/fxliu/hexo)
+ [博客仓库](https://github.com/fxliu/fxliu.github.io)
