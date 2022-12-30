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
    <tech-list>
        <tech>android.nfc.tech.IsoDep</tech>
        <tech>android.nfc.tech.NfcA</tech>
        <tech>android.nfc.tech.NfcB</tech>
        <tech>android.nfc.tech.NfcF</tech>
        <tech>android.nfc.tech.NfcV</tech>
        <tech>android.nfc.tech.Ndef</tech>
        <tech>android.nfc.tech.NdefFormatable</tech>
        <tech>android.nfc.tech.MifareClassic</tech>
        <tech>android.nfc.tech.MifareUltralight</tech>
    </tech-list>
</resources>
```

### 事件

```java
public class EsNfcUtil {
    // 硬件是否支持
    static public boolean isSupport(Context context) {
        return NfcAdapter.getDefaultAdapter(context) != null;
    }

    // NFC功能是否启用
    static public boolean isEnable(Context context) {
        NfcAdapter nfcAdapter = NfcAdapter.getDefaultAdapter(context);
        if (nfcAdapter == null)
            return false;
        return nfcAdapter.isEnabled();
    }

    // ---------------------------------------------------------------------------------------------
    // 绑定 A/B 卡监听
    static public NfcAdapter enableReaderMode(Activity activity, NfcAdapter.ReaderCallback readerCallback) {
        try {
            NfcAdapter nfcAdapter = NfcAdapter.getDefaultAdapter(activity);
            if (nfcAdapter == null)
                return null;
            if (!nfcAdapter.isEnabled())
                return null;
            Bundle options = new Bundle();
            //对卡片的检测延迟300ms
            options.putInt(NfcAdapter.EXTRA_READER_PRESENCE_CHECK_DELAY, 300);
            int READER_FLAGS = NfcAdapter.FLAG_READER_NFC_B | NfcAdapter.FLAG_READER_NFC_A;
            nfcAdapter.enableReaderMode(activity, readerCallback, READER_FLAGS, options);
            return nfcAdapter;
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }

    static public void disableReaderMode(Activity activity) {
        NfcAdapter nfcAdapter = NfcAdapter.getDefaultAdapter(activity);
        if (nfcAdapter == null)
            return;
        if (!nfcAdapter.isEnabled())
            return;
        nfcAdapter.disableReaderMode(activity);
    }

    // ---------------------------------------------------------------------------------------------
    // 绑定NFC刷证事件, 当此窗口启动时, 刷证不会弹出APP选择
    // 集成到: onResume
    @SuppressLint("UnspecifiedImmutableFlag")
    static public boolean enableDispatch(Activity activity) {
        if (!isEnable(activity))
            return false;
        Intent intent = new Intent(activity, activity.getClass()).addFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP);
        PendingIntent pi;
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
            pi = PendingIntent.getActivity(activity, 0, intent, PendingIntent.FLAG_MUTABLE);
        } else {
            pi = PendingIntent.getActivity(activity, 0, intent, PendingIntent.FLAG_UPDATE_CURRENT);
        }
        IntentFilter[] ifs = new IntentFilter[]{new IntentFilter(NfcAdapter.ACTION_TECH_DISCOVERED)};
        String[][] techLists = new String[][]{
                new String[]{NfcB.class.getName()},
                new String[]{NfcA.class.getName()}
        };
        NfcAdapter.getDefaultAdapter(activity).enableForegroundDispatch(activity, pi, ifs, techLists);
        return true;
    }

    // 集成到: onPause
    static public boolean disableDispatch(Activity activity) {
        if (!isEnable(activity))
            return false;
        NfcAdapter.getDefaultAdapter(activity).disableForegroundDispatch(activity);
        return true;
    }

    // ---------------------------------------------------------------------------------------------
    // 事件判定
    static public boolean isTech(Intent intent) {
        if (intent == null || intent.getAction() == null)
            return false;
        return intent.getAction().equals("android.nfc.action.TECH_DISCOVERED");
    }

    static public Tag getTechTag(Intent intent) {
        if (!isTech(intent))
            return null;
        return intent.getParcelableExtra(NfcAdapter.EXTRA_TAG);
    }
}

```

```java
// enableReaderMode 设置NFC读事件回调
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

## M1

```java
    void testM1(Intent intent) {
        Tag tag = intent.getParcelableExtra(NfcAdapter.EXTRA_TAG);
        MifareClassic mifareClassic = MifareClassic.get(tag);
        try {
            int block = 2;
            int sector = 2 / 4;
            mifareClassic.connect();
            mifareClassic.authenticateSectorWithKeyA(sector, MifareClassic.KEY_DEFAULT);
            byte[] d = mifareClassic.readBlock(block);
            Log.e(TAG, "testM1: " + HexUtil.Hex2String(d));
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
```

## 读卡

[nfcard](https://github.com/sinpolib/nfcard)
    + Support PBOC/EMV,北京市政一卡通,武汉通,长安通,Felica,ISO14443
[nfcard-android](https://github.com/PlatformaSoft/nfcard-android)
[身份证](es:svn\cloud_visitor\trunk\4_android\guard\idcardsdk)
