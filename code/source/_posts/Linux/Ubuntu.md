---
title: Ubuntu
tags: 
  - Ubuntu
categories: 
  - linux
description: Ubuntu
date: 2022-06-22 16:45:50
updated: 2022-06-22 16:45:50
---

## 虚拟机工具

```bash
sudo apt-get autoremove open-vm-tools
sudo apt-get install open-vm-tools
sudo apt-get install open-vm-tools-desktop
sudo reboot
```

## ssh

```sh
sudo apt-get install openssh-server
sudo systemctl status ssh   # q退出

sudo systemctl enable ssh
sudo systemctl disable ssh
```
