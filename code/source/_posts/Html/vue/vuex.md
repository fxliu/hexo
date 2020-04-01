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
// 简单的store，自己直接定义一个外变量，然后挂载到所有vue即可
var store = {
    debug: true,
    state: {
        message: 'Hello!'
    },
    setMessageAction (newValue) {
        this.state.message = newValue
    },
    clearMessageAction () {
        this.state.message = ''
    }
}
```

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
        // 可以封装成 Promise 对象, 调用者可以知道action结束事件
        // store.dispatch('actionA').then(() => {})
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
    },
    // 在严格模式下，无论何时发生了状态变更且不是由 mutation 函数引起的，将会抛出错误。
    // 这能保证所有的状态变更都能被调试工具跟踪到。
    // 严格模式会深度监测状态树来检测不合规的状态变更——请确保在发布环境下关闭严格模式，以避免性能损失
    strict: process.env.NODE_ENV !== 'production'
})

const moduleA = {
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

const moduleB = {
    state: { ... },
    mutations: { ... },
    actions: { ... }
}

const store = new Vuex.Store({
    modules: {
        a: moduleA,
        b: moduleB
    }
})
```

```js
// store 映射
export default {
    computed: mapState([
    // 映射 this.count 为 store.state.count
    'count'
    ]),
    computed: {
        // 使用对象展开运算符将此对象混入到外部对象中
        ...mapState({
            // ...
        }),
        // 使用对象展开运算符将 getter 混入 computed 对象中
        ...mapGetters([
            'doneTodosCount',
            'anotherGetter',
            // ...
        ])
    },
    methods: {
        // mutations 混入
        ...mapMutations([
                'increment', // 将 `this.increment()` 映射为 `this.$store.commit('increment')`

                // `mapMutations` 也支持载荷：
                'incrementBy' // 将 `this.incrementBy(amount)` 映射为 `this.$store.commit('incrementBy', amount)`
            ]),
        ...mapMutations({
            add: 'increment' // 将 `this.add()` 映射为 `this.$store.commit('increment')`
        }),
        // actions 混入
        ...mapActions([
            'increment', // 将 `this.increment()` 映射为 `this.$store.dispatch('increment')`
            // `mapActions` 也支持载荷：
            'incrementBy' // 将 `this.incrementBy(amount)` 映射为 `this.$store.dispatch('incrementBy', amount)`
        ]),
        ...mapActions({
            add: 'increment' // 将 `this.add()` 映射为 `this.$store.dispatch('increment')`
        })
    },
}
```
