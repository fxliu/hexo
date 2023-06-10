---
title: JNA
tags: 
  - JNA
categories: 
  - JAVA
description: JAVA, JNA
date: 2023-06-10 17:49:00
updated: 2023-06-10 17:49:00
---

## JNA

+ [github](https://github.com/java-native-access/jna)
  + [jna-5.13.0.jar](https://repo1.maven.org/maven2/net/java/dev/jna/jna/5.13.0/jna-5.13.0.jar)
  + [Doc](http://java-native-access.github.io/jna/5.13.0/javadoc/)

## Demo

```c++
// 回调
enum ES_LOG_LEVEL {
	ES_LOG_LEVEL_NULL = 0,
	ES_LOG_LEVEL_DEBUG = 1,
	ES_LOG_LEVEL_INFO = 2,
	ES_LOG_LEVEL_WARN = 3,
	ES_LOG_LEVEL_ERROR = 4,
};

typedef void(*PES_LogCB)(ES_LOG_LEVEL level, const char* szMsg, void* lpVoid);
typedef void(*PEsIdcardCB)(int notify, const char* data, int dataLen, LPVOID lpVoid);
typedef void(*PEsIdcardStatusCB)(EsIdcardStatus status, LPVOID lpVoid);
// 功能函数
BOOL ES_EIDSDK_SetUart(const char* szDevPath, int bps);
BOOL ES_EIDSDK_SetCfg(int idx, int v, char* data, int len);
BOOL ES_EIDSDK_SetAutoSdt(BOOL bAutoSdt);

BOOL ES_EIDSDK_Init(const char* ioType, const char* flag);
void ES_EIDSDK_Release();

BOOL ES_EIDSDK_Start();
BOOL ES_EIDSDK_Stop();

void ES_EIDSDK_SetLogCB(PES_LogCB cb, LPVOID lpVoid);
void ES_EIDSDK_SetIdcardCB(PEsIdcardCB cb, LPVOID lpVoid);
void ES_EIDSDK_SetIdcardStatusCB(PEsIdcardStatusCB cb, LPVOID lpVoid);

BOOL ES_EIDSDK_GetSamID(char* id);
BOOL ES_EIDSDK_GetProVersion(char* ver);
BOOL ES_EIDSDK_GetHardVersion(char* ver);
BOOL ES_EIDSDK_GetExpTime(char* outData, int outDataLen);

BOOL ES_EIDSDK_Update(const char *szBinFile);

BOOL ES_EIDSDK_WltUnpack(const char* wltData, int wltLen, char* bmp, int bmpLen);
```

```java
import com.sun.jna.Callback;
import com.sun.jna.Library;
import com.sun.jna.Native;
import com.sun.jna.Pointer;

public interface EsEidSdk extends Library {
    EsEidSdk sdk = (EsEidSdk) Native.load("EsEidSdk.dll", EsEidSdk.class);

    static final String ES_EID_SDK_IOTYPE_UART = "UART";
    static final String ES_EID_SDK_IOTYPE_USBHID = "USBHID";

    // --------------------------------------------------------------------
    // 前置参数配置，必须再Init之前配置
    // --------------------------------------------------------------------
    Boolean ES_EIDSDK_SetUart(String szDevPath, int bps);   // 传入字符串 -> 可以直接用String
    Boolean ES_EIDSDK_SetCfg(int idx, int v, byte[] data, int len);
    Boolean ES_EIDSDK_SetAutoSdt(Boolean bAutoSdt);

    // ----------------------------------------------------------------------------
    // 服务管理
    // ----------------------------------------------------------------------------
    Boolean ES_EIDSDK_Init(String ioType, String flag);
    void ES_EIDSDK_Release();
    Boolean ES_EIDSDK_Start();
    Boolean ES_EIDSDK_Stop();

    // ---------------------------------------------------------------------------------
    // 回调应尽快返回，不要影响程序正常执行
    // ---------------------------------------------------------------------------------
    interface PES_LogCB extends Callback {
        static final int ES_LOG_LEVEL_NULL = 0;
        static final int ES_LOG_LEVEL_DEBUG = 1;
        static final int ES_LOG_LEVEL_INFO = 2;
        static final int ES_LOG_LEVEL_WARN = 3;
        static final int ES_LOG_LEVEL_ERROR = 4;
        // 传出的字符串 - 无中文 - 可以支持使用String
        void callback(int level, String msg, Pointer lpVoid);
    }

    void ES_EIDSDK_SetLogCB(PES_LogCB cb, Pointer lpVoid);

    interface PEsIdcardCB extends Callback {
        // 不定长数据, 使用Pointer接收
        void callback(int notify, Pointer data, int dataLen, Pointer lpVoid);
    }

    void ES_EIDSDK_SetIdcardCB(PEsIdcardCB cb, Pointer lpVoid);

    interface PEsIdcardStatusCB extends Callback {
        static final int ES_IDCARD_ERROR_IO = -2;                // 读写失败 - 自动重新尝试
        static final int ES_IDCARD_ERROR_CONNECT = -1;            // 连接失败(专用) - 通常设备掉线所致 - 自动重新尝试
        static final int ES_IDCARD_ERROR = -1;                    // 连接失败(专用) - 通常设备掉线所致 - 自动重新尝试
        static final int ES_IDCARD_STOP = 0;                    // 未启动
        static final int ES_IDCARD_STOPPING = 1;                // 停止中
        static final int ES_IDCARD_STARTING = 2;                // 启动中
        static final int ES_IDCARD_RUNNING = 3;                    // 运行中 - 恢复连接
        static final int ES_IDCARD_CONNECT = ES_IDCARD_RUNNING;    // 运行中 - 恢复连接
        static final int ES_IDCARD_PAUSE = 4;                    // 暂停

        void callback(int status, Pointer lpVoid);
    }

    void ES_EIDSDK_SetIdcardStatusCB(PEsIdcardStatusCB cb, Pointer lpVoid);

    // ---------------------------------------------------------------------------------
    // 信息获取
    // ---------------------------------------------------------------------------------
    Boolean ES_EIDSDK_GetSamID(byte[] id);      // 数据接收, 传入有效内存块接收
    Boolean ES_EIDSDK_GetProVersion(byte[] ver);
    Boolean ES_EIDSDK_GetHardVersion(byte[] ver);
    Boolean ES_EIDSDK_GetExpTime(byte[] outData, int outDataLen);

//    // ---------------------------------------------------------------------------------
//    // 升级
//    // ---------------------------------------------------------------------------------
//    BOOL ES_EIDSDK_Update(String szBinFile);

    // ---------------------------------------------------------------------------------
    // Wlt文件解码: wltLen=1024, bmpLen=38862
    // ---------------------------------------------------------------------------------
    Boolean ES_EIDSDK_WltUnpack(byte[] wltData, int wltLen, byte[] bmp, int bmpLen);
}

```

```java
// 结构体解析
public class EsIdcardInfo {
    static final int ESIDCARD_NOTIFY_FIND = 1;    // 发现证件
    static final int ESIDCARD_NOTIFY_SUCCESS = 2;    // 证件信息提取成功

    // ------------------------------------------------------------------------
    // 注意这里的字段长度定义, 必须和C头文件保持一致
    byte classify;                // 射频分类：1 真实证件，2 电子证照
    byte idType;                // 证件类型: ESIDCARD_IDTYPE_N | ESIDCARD_IDTYPE_J | ESIDCARD_IDTYPE_I
    byte[] szName = new byte[64];            // 姓名：15 * 3	| 中文姓名(I证)
    byte[] szSex = new byte[4];                // 性别 未知 0，男 1，女 2
    byte[] szNationCode = new byte[4];        // 民族编码(N证) | 无效(J证) | 国籍编码(I证)
    byte[] szNation = new byte[128];            // 民族(N证) | 无效(J证) | 国籍(I证)
    byte[] szBirthDate = new byte[16];        // 生日
    byte[] szAddr = new byte[256];            // 住址：70 * 3	| 无效(I证)
    byte[] szCert = new byte[32];            // 证件号
    byte[] szDep = new byte[64];                // 签发机关：15 * 3		| 无效(I证)
    byte[] szBegin = new byte[16];            // 有效期-起始时间
    byte[] szEnd = new byte[16];                // 有效期-结束时间
    byte[] wlt = new byte[1024];                // WLT原数据
    // J证扩展
    byte[] szOtherIdNum = new byte[32];        // 港澳台有效，通行证号码
    byte[] szSigningTimes = new byte[4];        // 港澳台有效，签发次数
    // I证扩展
    byte[] szEnName = new byte[64];            // 英文姓名
    byte[] szVersion = new byte[4];            // 证件版本号
    byte[] szDepCode = new byte[8];            // 受理机关代码 1500 -> 公安部/Ministry of Public Security
    // ------------------------------------------------------------------------

    EsIdcardInfo(byte[] data) {
        int idx = 0;
        classify = data[idx++];
        idType = data[idx++];
        idx = arraycopy(data, idx, szName);
        idx = arraycopy(data, idx, szSex);
        idx = arraycopy(data, idx, szNationCode);
        idx = arraycopy(data, idx, szNation);
        idx = arraycopy(data, idx, szBirthDate);
        idx = arraycopy(data, idx, szAddr);
        idx = arraycopy(data, idx, szCert);
        idx = arraycopy(data, idx, szDep);
        idx = arraycopy(data, idx, szBegin);
        idx = arraycopy(data, idx, szEnd);
        idx = arraycopy(data, idx, wlt);
        idx = arraycopy(data, idx, szOtherIdNum);
        idx = arraycopy(data, idx, szSigningTimes);
        idx = arraycopy(data, idx, szEnName);
        idx = arraycopy(data, idx, szVersion);
        arraycopy(data, idx, szDepCode);
    }

    int arraycopy(byte[] src, int idx, byte[] dest) {
        System.arraycopy(src, idx, dest, 0, dest.length);
        return idx + dest.length;
    }

    String byte2String(byte[] data) {
        try {
            int idx = 0;
            while ((idx < data.length) && (data[idx] != 0x00)) idx++;
            String str = new String(data, 0, idx, "GBK");
            return str.replace(" ", "");
        } catch (UnsupportedEncodingException e) {
            throw new RuntimeException(e);
        }
    }

    String getName() {
        return byte2String(szName);
    }

    String getSex() {
        return byte2String(szSex);
    }

    String getNation() {
        return byte2String(szNation);
    }

    String getCert() {
        return byte2String(szCert);
    }

    String getAddr() {
        return byte2String(szAddr);
    }
}
```

```java
public class Main {
    private static final Boolean UART = false;
    private static final String UART_PATH = "\\\\.\\COM15";

    public static <BufferedReader> void main(String[] args) {
        // ----------------------------------------------------
        // 配置回调
        EsEidSdk.sdk.ES_EIDSDK_SetLogCB(logCB, null);
        EsEidSdk.sdk.ES_EIDSDK_SetIdcardCB(idcardCB, null);
        EsEidSdk.sdk.ES_EIDSDK_SetIdcardStatusCB(idcardStatusCB, null);
        // ----------------------------------------------------
        // flag: 厂商标记，eid_demo 是测试标记，发布前请联系服务商获取正式版标记
        if (UART) {
            EsEidSdk.sdk.ES_EIDSDK_SetUart(UART_PATH, 115200);
            EsEidSdk.sdk.ES_EIDSDK_Init(EsEidSdk.ES_EID_SDK_IOTYPE_UART, "eid_demo");
        } else {
            EsEidSdk.sdk.ES_EIDSDK_Init(EsEidSdk.ES_EID_SDK_IOTYPE_USBHID, "eid_demo");
        }
        // ----------------------------------------------------
        // TODO: 禁用SDT功能, 设备无SDT输出, 或用户业务无需使用SDT功能时, 建议关闭, 提高读卡速度
        //  支持SDT功能的读卡器, 接线位置有SDT私印, 如果SDT引脚未接线引出到主板, 即可关闭此功能
        EsEidSdk.sdk.ES_EIDSDK_SetAutoSdt(Boolean.FALSE);
        // 关闭优化机制 - 仅适用于 Demo 测试, 正常产品发布建议打开优化机制
        //ES_EIDSDK_SetCfg(100, 0, NULL, 0);
        // 打开优化机制
        EsEidSdk.sdk.ES_EIDSDK_SetCfg(100, 1, null, 0);
        // ----------------------------------------------------
        if (!EsEidSdk.sdk.ES_EIDSDK_Start()) {
            ESLOGD("ES_EIDSDK_Start error");
            return;
        }
        ESLOGD("ES_EIDSDK_Start");
        try {
            System.in.readNBytes(1);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        ESLOGD("-------------- stop --------------\n");
        EsEidSdk.sdk.ES_EIDSDK_Stop();
        EsEidSdk.sdk.ES_EIDSDK_Release();
    }

    static void ESLOGD(String msg) {
        System.out.println(msg);
    }

    static final EsEidSdk.PES_LogCB logCB = (level, msg, lpVoid) -> {
        String strLevel = "";
        switch (level) {
            case EsEidSdk.PES_LogCB.ES_LOG_LEVEL_NULL:
                strLevel = "[N]";
                break;
            case EsEidSdk.PES_LogCB.ES_LOG_LEVEL_DEBUG:
                strLevel = "[D]";
                break;
            case EsEidSdk.PES_LogCB.ES_LOG_LEVEL_INFO:
                strLevel = "[I]";
                break;
            case EsEidSdk.PES_LogCB.ES_LOG_LEVEL_WARN:
                strLevel = "[W]";
                break;
            case EsEidSdk.PES_LogCB.ES_LOG_LEVEL_ERROR:
                strLevel = "[E]";
                break;
        }
        SimpleDateFormat formatter = new SimpleDateFormat("[yyyy-MM-dd HH:mm:ss.SSS]");
        String strDate = formatter.format(new Date());
        ESLOGD(strDate + strLevel + msg);
    };

    static final EsEidSdk.PEsIdcardCB idcardCB = (notify, data, dataLen, lpVoid) -> {
        if (notify == EsIdcardInfo.ESIDCARD_NOTIFY_FIND) {
            ESLOGD("ESIDCARD_NOTIFY_FIND");
        }
        if (dataLen > 0 && notify == EsIdcardInfo.ESIDCARD_NOTIFY_SUCCESS) {
            EsIdcardInfo info = new EsIdcardInfo(data.getByteArray(0, dataLen));
            ESLOGD(String.format("EsIdcardCB: name  : %s", info.getName()));
            ESLOGD(String.format("EsIdcardCB: sex   : %s", Objects.equals(info.getSex(), "1") ? "男" : "女"));
            ESLOGD(String.format("EsIdcardCB: nation: %s", info.getNation()));
            ESLOGD(String.format("EsIdcardCB: cert  : %s", info.getCert()));
            ESLOGD(String.format("EsIdcardCB: addr  : %s", info.getAddr()));
        }
    };

    static String ver2String(byte[] data) {
        StringBuilder str = new StringBuilder();
        for (byte b : data) {
            if (b == 0x00)
                break;
            str.append((char) b);
        }
        return str.toString();
    }

    static final EsEidSdk.PEsIdcardStatusCB idcardStatusCB = (status, lpVoid) -> {
        // ----------------------------------------------------
        // 回调函数中不要做复杂业务逻辑, 尽快反馈, 必要时请开启多线程处理
        switch (status) {
            case EsEidSdk.PEsIdcardStatusCB.ES_IDCARD_ERROR_IO:
                ESLOGD("ES_IDCARD_ERROR_IO");
                break;
            case EsEidSdk.PEsIdcardStatusCB.ES_IDCARD_ERROR_CONNECT:
                // 设备连接失败
                // 1. 硬件接线 不正确触发
                // 2. 主动发送 设备重启指令触发
                ESLOGD("ES_IDCARD_ERROR_CONNECT");
                break;
            case EsEidSdk.PEsIdcardStatusCB.ES_IDCARD_STOP:
                ESLOGD("ES_IDCARD_STOP");
                break;
            case EsEidSdk.PEsIdcardStatusCB.ES_IDCARD_STOPPING:
                ESLOGD("ES_IDCARD_STOPPING");
                break;
            case EsEidSdk.PEsIdcardStatusCB.ES_IDCARD_STARTING:
                ESLOGD("ES_IDCARD_STARTING");
                break;
            case EsEidSdk.PEsIdcardStatusCB.ES_IDCARD_RUNNING: {
                ESLOGD("ES_IDCARD_RUNNING");
                // 只有进入 ES_IDCARD_RUNNING 状态之后，才可以成功获取设备编号
                // TODO: 设备序号, 建议显示到界面或通过其他方式管理, 以便于后续对读卡器设备进行授权管控
                byte[] szSamID = new byte[64];
                EsEidSdk.sdk.ES_EIDSDK_GetSamID(szSamID);
                ESLOGD(String.format("SamID: %s", ver2String(szSamID)));
                // 固件版本号
                byte[] proVersion = new byte[64];
                EsEidSdk.sdk.ES_EIDSDK_GetProVersion(proVersion);
                ESLOGD(String.format("Soft Version: %s", ver2String(proVersion)));
                // 硬件版本号 - 用于区分读卡器型号
                byte[] hardVersion = new byte[64];
                EsEidSdk.sdk.ES_EIDSDK_GetHardVersion(hardVersion);
                ESLOGD(String.format("Hard Version: %s", ver2String(hardVersion)));
                break;
            }
            case EsEidSdk.PEsIdcardStatusCB.ES_IDCARD_PAUSE:
                ESLOGD("ES_IDCARD_PAUSE");
                break;
            default:
                break;
        }
    };
}
```
