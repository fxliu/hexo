---
title: Binding
tags: 
    - Binding
categories: 
    - Android
description: Binding
date: 2022-07-20 21:54:29
updated: 2022-07-20 21:54:29
---

## 基础

```java
// build.gradle(:app)
android {
    // ..
    buildFeatures {
        viewBinding true
    }
}
// MainActivity
public class MainActivity extends AppCompatActivity {
    private ActivityMainBinding binding;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // setContentView(R.layout.activity_main);
        binding = ActivityMainBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());
    }
}
```