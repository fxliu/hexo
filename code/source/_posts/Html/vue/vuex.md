---
title: vuex
tags: 
  - vuex
categories: 
  - JS
  - vue
description: vuex
date: 2019-12-02 10:56:59
updated: 2019-12-02 10:56:59
---

## 基础

```js
import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        // 存放状态，用于查询，不建议直接修改
        hello: "hello world",
        user: {
            name: "",
            cert: ""
        },
        // 直接修改
        // Vue.set(state,"age",15)  设置，不存在则创建
        // Vue.delete(state,'age')  删除
    },
    mutations: {
        // 成员操作
    },
    actions: {
        // 异步操作：直接在modules中使用setTimeout等异步，会引起数据失效
        hello(context,payload){
            // context => store
            // 组件调用: this.$store.dispatch('hello',"world")
            setTimeout(()=>{
                // 调用modules
                context.commit('hello',payload)
            },2000)
        },
        // 可以封装成 Promise 对象
        helloPromise(context,payload){
            return new Promise((resolve,reject)=>{
                setTimeout(()=>{
                    // 调用modules
                    context.commit('hello',payload);
                    resolve();
                },2000)
            })
        },
    },
    getters:{
        // 数据查询：通常用于数据联合查询
        userName(state, getters){
            // 默认参数：state => store.state, getters => store.getters
            // 组件调用：this.$store.getters.userName
            return "姓名:" + state.user.name;
        }
    },
    modules: {
        // state数据增删改入口
        hello(name) {
            // 组件调用：this.$store.commit('hello',"world")
            this.state.hello = "hello " + name;
        },
        // 用户信息入口
        user(userInfo) {
            // 组件调用：this.$store.commit('user',{"name":"","cert":"",icafe:[]})
            this.state.user.name = userInfo.name;
            this.state.user.cert = userInfo.cert;
            this.memberIcafes = userInfo.icafe;
        }
    },
    models:{
        // 可以内封装模块，执行动作是，会自动查找拥有该动作的所有模块并执行
        // 模块支持多层嵌套
        m1:{
            state:{},
            getters:{
                userName(state,getters, rootState){
                    // 默认参数：state => m1.state, getters => m1.getters, rootState => 根state
                    // 组件调用：this.$store.getters.userName
                    return "姓名:" + state.user.name;
                }
            },
            actions: {
                hello(context, payload) {
                    // context: context.state => m1.state, context.rootState => 根state
                    // 组件调用: this.$store.dispatch('hello',"world")
                    setTimeout(() => {
                        // 调用modules
                        context.commit('hello', payload)
                    }, 2000)
                },
            }
        }
    },
})
```
