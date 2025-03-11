# DES加解密工具

## 项目概述

《现代密码学》实验课作业产物, 功能如下

## 功能

- **多种加密模式**：支持ECB、CBC、CFB、OFB、CTR五种分组密码工作模式
- **灵活的轮数设置**：支持自定义DES算法轮数(1-32轮)
- **文本加解密**：直接在界面中输入文本进行加解密
- **文件加解密**：支持任意类型文件加密
- **密钥管理**：支持生成随机密钥和初始化向量(IV)
- **数据格式**：支持十六进制和Base64编码显示加密结果
- **命令行支持**：提供命令行界面

## 安装与运行

1. 克隆或下载本仓库
   ```
   git clone https://github.com/yourusername/DES_Demo.git
   cd DES_Demo
   ```

2. 运行程序
   ```
   python app.py        # 启动GUI界面
   python app.py --cli  # 启动命令行界面
   ```

## 项目结构

```
DES_Demo/
├── app.py               # 主入口文件
├── build.py             # 构建脚本
├── requirements.txt     # 依赖项列表
├── core/                # 核心算法实现
│   ├── __init__.py
│   └── des.py           # DES算法实现
├── gui/                 # 图形界面
│   ├── __init__.py
│   ├── des_gui.py       # 主GUI界面
│   ├── des_gui_text.py  # 文本处理选项卡
│   ├── des_gui_file.py  # 文件处理选项卡
│   └── des_gui_common.py # 通用GUI组件
└── cli/                 # 命令行界面
    ├── __init__.py
    └── des_cli.py       # CLI实现
```
