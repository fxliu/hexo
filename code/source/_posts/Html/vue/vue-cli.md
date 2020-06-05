---
title: vue-cli
tags: 
  - vue-cli
categories: 
  - JS
  - vue
description: vue-cli
date: 2019-12-02 10:56:59
updated: 2019-12-02 10:56:59
---

## 基础

[vue-cli](https://cli.vuejs.org/zh/)
支持`vue ui`指令，使用Web页面方式管理工程

## 常规组件

+ less, less-loader
  + `npm install less less-loader --save-dev`
+ [postcss-px-to-viewport](https://www.npmjs.com/package/postcss-px-to-viewport)
  + [淘宝镜像-中文](https://npm.taobao.org/package/postcss-px-to-viewport)
  + postcss插件，自动转化px为vw,vh,vmin,vmax
+ postcss:
  + Vue CLI 项目默认支持 PostCSS 、CSS Modules 和包含 Sass 、Less 、Stylus 在内的预处理器
  + 默认开启了 autoprefixer
  + 如果要配置目标浏览器，可使用 package.json 的 browserslist 字段。
  + 安装：`npm install postcss-px-to-viewport --save-dev`
+ element
  + 插件安装
+ bootstrap4
  + `npm i bootstrap --save`
  + `import 'bootstrap/dist/css/bootstrap.min.css'`
+ bootstrapvue
  + 响应式移动框架，基于bootstrap4
  + 负载较大
+ jquery
  + `npm install jquery --save`
  + 配置到`vue.config.js`，见常规配置
  + 代码引用：
    + `import $ from 'jquery'`
+ axios
  + 插件安装
+ lodash
+ fastclick
  + `npm install --save fastclick`
  + `import FastClick from 'fastclick';`
  + `FastClick.attach(document.body);`
+ vue-router
  + vue add router
+ vuex: 前台数据缓存
+ font-awesome
  + `import 'font-awesome/css/font-awesome.min.css'`
  + `<i class="fa fa-car fa-lg"></i>`
  + 5.x版比较重载，谨慎使用
+ cropperjs：图片裁剪
  + `npm install --save vue-cropperjs`
+ better-scroll：滚轮监控
  + `npm i --save better-scroll`

## lint

```json
// package.json
    "rules": {
      "vue/no-unused-components": "off",
      "vue/no-unused-vars": "off",
      "no-unused-vars": "off"
    }
```

## 常规配置

```js
// 编译报告：js文件大小
npm install webpack-bundle-analyzer –save-dev
npm run build –report
```

```js
// vue.config.js
// vue.config.js
let path = require('path');
const webpack = require('webpack');

module.exports = {
    publicPath: process.env.NODE_ENV === 'production' ? '/wechat/mobile/' : '',
    assetsDir: process.env.NODE_ENV === 'production' ? './online_sales/' : '',
    productionSourceMap: false,
    pages: {
        index: {
            entry: 'src/main.js',
            filename: process.env.NODE_ENV === 'production' ? 'online_sales.html' : 'index.html',
            template: process.env.NODE_ENV === 'production' ? 'src/index_build.html' : 'src/index_dev.html'
        },
        // 多页
        // subpage: 'src/subpage.js',       // 默认对应 public/subpage.html
    },
    lintOnSave: process.env.NODE_ENV === 'development',
    devServer: {
        port: 9000,
        // open: true, // 编译后自动打开
        proxy: {
            '/online_sales/api': {
                // host替换
                // target:'http://localhost:80/online_sales/trunk/3_client/netizen/mall/src/test',
                target: 'http://localhost:80/',
                changeOrigin: true, // needed for virtual hosted sites
                // ws: true, // proxy websockets
                pathRewrite: {
                    // 路径替换
                    '/online_sales/api/': '/online_sales/trunk/3_client/netizen/mall/src/test/api/',
                }
            },
            '/mobile/api': {
                // host替换
                // target:'http://localhost:80/online_sales/trunk/3_client/netizen/mall/src/test',
                target: 'http://localhost:80/',
                changeOrigin: true, // needed for virtual hosted sites
                // ws: true, // proxy websockets
                pathRewrite: {
                    // 路径替换
                    '/mobile/api/': '/online_sales/trunk/3_client/netizen/mall/src/test/api/',
                }
            }
        }
    },
    configureWebpack: {
        plugins: [
            new webpack.ProvidePlugin({
                $:"jquery",
                jQuery:"jquery",
                "windows.jQuery":"jquery"
            })
        ],
    },
    css: {
        loaderOptions: {
            postcss: {
                plugins: [
                    require("postcss-px-to-viewport")({
                        unitToConvert: 'px',
                        viewportWidth: 375,
                        unitPrecision: 5,       // 指定`px`转换为视窗单位值的小数位数
                        propList: ['*'],
                        viewportUnit: 'vw',
                        fontViewportUnit: 'vw',
                        selectorBlackList: [],
                        minPixelValue: 1,       // 小于1px的不转换
                        mediaQuery: false,
                        replace: true,
                        landscape: false,
                        landscapeUnit: 'vw',
                        landscapeWidth: 667,
                        exclude: /(\/|\\)(node_modules)(\/|\\)/,
                    })
                ]
            }
        }
    }
};
```

### 懒加载

```js
// 按需加载路由
const percenter = () => import('views/percenter/main.vue');

const routes = [
    {
        path: '/',
        name: 'MainPage',
        component: () => import('../views/MainPage')
    }
];

// 移除移动端页面点击延迟: 异步加载
import('fastclick').then(FastClick => {
    FastClick.attach(document.body);
});
// 多个组件同时异步
Promise.all([
    import("./assets/js/eslibs"),
    import('bootstrap/dist/css/bootstrap.min.css'),
]).then(responses => {
    let eslibs = responses[0].default;
}

(() => {
    require.ensure([], function (require) {
        require('./router_view.js');
    });
})();
```
