---
title: MediaPlayer
tags: 
    - MediaPlayer
categories: 
    - MediaPlayer
description: MediaPlayer
date: 2023-02-09 12:03:21
updated: 2023-02-09 12:03:21
---

## MediaPlayer + SurfaceView

```xml
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"
        tools:ignore="ScopedStorage" />
```

```java
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        // ...
        mSurfaceView = findViewById(R.id.surfaceView);
        //请求权限全部结果
        RxPermissions rxPermission = new RxPermissions(MainActivity.this);
        rxPermission.request(
                Manifest.permission.READ_EXTERNAL_STORAGE,
                Manifest.permission.WRITE_EXTERNAL_STORAGE
        ).subscribe(granted -> {
            if (granted) {
                startMediaPlayer();
            }
        });
    }

    void startMediaPlayer() {
        Log.e(TAG, "-------- start --------");
        mSurfaceView.getHolder().addCallback(new SurfaceHolder.Callback() {
            @Override
            public void surfaceCreated(@NonNull SurfaceHolder holder) {
                mPlayer = new MediaPlayer();
                mPlayer.setAudioStreamType(AudioManager.STREAM_MUSIC);
                mPlayer.setDisplay(holder);  // 设置视频显示区域
                try {
                    String fn = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DCIM) + "/Camera/test.mp4";
                    Log.d(TAG, "file: " + fn);
                    mPlayer.setDataSource(fn);
                    mPlayer.prepare();
                    mPlayer.setLooping(true);
                    mPlayer.start();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }

            @Override
            public void surfaceChanged(@NonNull SurfaceHolder holder, int format, int width, int height) {
                Log.e(TAG, String.format("surfaceChanged: w=%d, h=%d", width, height));
            }

            @Override
            public void surfaceDestroyed(@NonNull SurfaceHolder holder) {

            }
        });
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        if(mPlayer != null) {
            if(mPlayer.isPlaying())
                mPlayer.stop();
            mPlayer.release();
        }
    }
```

## VideoView

```java
    @Override
    protected void onCreate(Bundle savedInstanceState) {
		// ...
        mVideoView = findViewById(R.id.videoView);
        //请求权限全部结果
        RxPermissions rxPermission = new RxPermissions(MainActivity.this);
        rxPermission.request(
                Manifest.permission.READ_EXTERNAL_STORAGE,
                Manifest.permission.WRITE_EXTERNAL_STORAGE
        ).subscribe(granted -> {
            if (granted) {
                startVideoView();
            }
        });
    }
    void startVideoView() {
        String fn = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DCIM) + "/Camera/test.mp4";
        mVideoView.setVideoPath(fn);
        mVideoView.setOnPreparedListener(new MediaPlayer.OnPreparedListener() {
            @Override
            public void onPrepared(MediaPlayer mp) {
                mp.setLooping(true);
                mVideoView.start();
            }
        });
    }
    @Override
    protected void onDestroy() {
        super.onDestroy();
        if(mVideoView != null) {
            if(mVideoView.isPlaying())
                mVideoView.stopPlayback();
            mVideoView.suspend();
        }
    }
```
