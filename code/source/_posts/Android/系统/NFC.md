---
title: NFC
tags: 
  - NFC
categories: 
  - Android
description: NFC
date: 2020-02-03 08:44:37
updated: 2020-02-03 08:44:37
---

## 权限

```xml
<--AndroidManifest.xml-->
<application>
  <activity android:name=".MainActivity">
    <intent-filter>
      <action android:name="android.intent.action.MAIN" />
      <category android:name="android.intent.category.LAUNCHER" />
    </intent-filter>
    <!--绑定事件-->
    <intent-filter>
      <action android:name="android.nfc.action.TECH_DISCOVERED" />
    </intent-filter>
    <!--NFC数据过滤，仅捕获指定数据类型事件-->
    <meta-data
      android:name="android.nfc.action.TECH_DISCOVERED"
      android:resource="@xml/nfc_tech_filter" />
  </activity>
</application>
<!--NFC权限-->
<uses-permission android:name="android.permission.NFC"/>
<!-- 声明所依赖的外部的硬件，并指定为必须 -->
<uses-feature android:name="android.hardware.nfc" android:required="true" />
```

```xml
<!--nfc_tech_filter.xml-->
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <tech-list>
        <tech>android.nfc.tech.NfcB</tech>
    </tech-list>
    <tech-list>
        <tech>android.nfc.tech.IsoDep</tech>
    </tech-list>
</resources>
```

### 事件

```java
    NfcAdapter m_nfcAdapter;
    PendingIntent m_nfcPi;
    IntentFilter[] m_nfcIfs;
    String[][] m_techLists;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        // ...
        m_nfcAdapter = NfcAdapter.getDefaultAdapter(this);
        if (null == m_nfcAdapter) {
            m_textDes.setText("设备不支持NFC功能");
        } else if (!m_nfcAdapter.isEnabled()) {
            m_textDes.setText("请先开启设备NFC功能");
        } else {
            m_textDes.setText("请放置身份证到设备背面");
        }
        // 用于页面绑定：仅软件启动时绑定NFC事件
        m_nfcPi = PendingIntent.getActivity(this, 0, new Intent(this, getClass()).addFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP), PendingIntent.FLAG_UPDATE_CURRENT);
        m_nfcIfs = new IntentFilter[]{new IntentFilter(NfcAdapter.ACTION_TECH_DISCOVERED)};
        m_techLists = new String[][]{new String[]{NfcB.class.getName()}, new String[]{IsoDep.class.getName()}};
        // ...
    }
    @Override
    protected void onResume() {
        super.onResume();
        if (m_nfcAdapter != null) // 绑定NFC事件
            m_nfcAdapter.enableForegroundDispatch(this, m_nfcPi, m_nfcIfs, m_techLists);
    }
    @Override
    protected void onPause() {
        super.onPause();
        Log.e("test", "onPause");
        if (m_nfcAdapter != null) // 解绑NFC
            m_nfcAdapter.disableForegroundDispatch(this);
    }
    @Override
    protected void onNewIntent(Intent intent) {
        super.onNewIntent(intent);
        //获取到Tag标签对象
        Tag mTag = intent.getParcelableExtra(NfcAdapter.EXTRA_TAG);
        try {
            String[] techList = mTag.getTechList();
            Log.w("test", "标签支持的tachnology类型：");
            for (String tech : techList) {
                Log.w("test", tech);
            }
        } catch (NullPointerException e) {
            e.printStackTrace();
        }
    }
    public void onSetting(View view) {
        // 根据包名打开对应的设置界面：开关NFC位置
        Intent intent = new Intent(Settings.ACTION_NFC_SETTINGS);
        startActivity(intent);
    }
```

```java
// enableReaderMode 设置事件回调
NfcAdapter m_nfcAdapter;
private static final int READER_FLAGS = NfcAdapter.FLAG_READER_NFC_A | NfcAdapter.FLAG_READER_NFC_B;
@Override
protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    setContentView(R.layout.activity_main);
    m_nfcAdapter = NfcAdapter.getDefaultAdapter(this);
}
private NfcAdapter.ReaderCallback mReaderCallback = new NfcAdapter.ReaderCallback() {
    @Override
    public void onTagDiscovered(Tag tag) {
        Log.d("test", "onTagDiscovered: " + Arrays.toString(tag.getTechList()));
    }
};
@Override
protected void onResume() {
    super.onResume();
    Log.e("test", "onResume");
    if (m_nfcAdapter != null) // 绑定NFC事件
        m_nfcAdapter.enableReaderMode(this, mReaderCallback, READER_FLAGS, null);
}
@Override
protected void onPause() {
    super.onPause();
    Log.e("test", "onPause");
    if (m_nfcAdapter != null) // 解绑NFC
        m_nfcAdapter.disableReaderMode(this);
}
```
