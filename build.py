#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
构建脚本 - 用于构建DES加解密工具的可执行文件
"""

import os
import sys
import shutil
import subprocess
import platform
import argparse
from pathlib import Path

def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='DES加解密工具构建脚本')
    parser.add_argument('--clean', action='store_true', help='清理构建文件')
    parser.add_argument('--pyinstaller', action='store_true', help='使用PyInstaller构建')
    parser.add_argument('--cx_freeze', action='store_true', help='使用cx_Freeze构建')
    parser.add_argument('--all', action='store_true', help='构建所有格式')
    return parser.parse_args()

def clean():
    """清理构建文件夹"""
    print("正在清理构建文件...")
    dirs_to_remove = ['build', 'dist', '__pycache__']
    files_to_remove = ['*.spec']
    
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"已删除目录: {dir_name}")
    
    for pattern in files_to_remove:
        for file in Path('.').glob(pattern):
            file.unlink()
            print(f"已删除文件: {file}")
    
    # 清理所有__pycache__目录
    for root, dirs, files in os.walk('.'):
        for dir_name in dirs:
            if dir_name == '__pycache__':
                shutil.rmtree(os.path.join(root, dir_name))
                print(f"已删除目录: {os.path.join(root, dir_name)}")

def install_requirements():
    """安装依赖项"""
    print("正在安装依赖项...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("依赖项安装完成。")
    except subprocess.CalledProcessError:
        print("安装依赖项失败，请检查网络连接或手动安装。")
        return False
    return True

def build_with_pyinstaller():
    """使用PyInstaller构建可执行文件"""
    print("正在使用PyInstaller构建可执行文件...")
    try:
        # 基本命令
        cmd = [
            'pyinstaller',
            '--name=DES加解密工具',
            '--onefile',
            '--windowed',  # 如果是GUI应用
            '--icon=resources/icon.ico' if os.path.exists('resources/icon.ico') else '',
            '--add-data=README.md;.' if os.path.exists('README.md') else '',
            'app.py'
        ]
        
        # 过滤空字符串
        cmd = [item for item in cmd if item]
        
        print(f"执行命令: {' '.join(cmd)}")
        subprocess.check_call(cmd)
        print("PyInstaller构建完成！")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"构建失败: {e}")
        print("请确保已安装PyInstaller，或者手动运行: pip install pyinstaller")
        return False

def build_with_cx_freeze():
    """使用cx_Freeze构建可执行文件"""
    print("正在使用cx_Freeze构建可执行文件...")
    
    # 创建或更新cx_freeze的setup.py
    setup_py = """
from cx_Freeze import setup, Executable
import sys
import os

# 依赖项
build_exe_options = {
    "packages": ["os", "sys", "tkinter", "binascii", "threading", "argparse", "time", "random"],
    "excludes": ["unittest", "email", "html", "http", "xml", "pydoc"],
    "include_files": [],
}

# 基本信息
base = "Win32GUI" if sys.platform == "win32" else None

setup(
    name = "DES加解密工具",
    version = "1.0",
    description = "DES加密解密工具 - 支持所有类型的文件加密",
    options = {"build_exe": build_exe_options},
    executables = [Executable(
        "app.py",
        base=base,
        target_name="DES加解密工具",
        icon="resources/icon.ico" if os.path.exists("resources/icon.ico") else None
    )]
)
"""
    
    # 写入setup.py
    with open('setup_cx.py', 'w', encoding='utf-8') as f:
        f.write(setup_py)
    
    try:
        # 构建
        cmd = [sys.executable, 'setup_cx.py', 'build']
        print(f"执行命令: {' '.join(cmd)}")
        subprocess.check_call(cmd)
        print("cx_Freeze构建完成！")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"构建失败: {e}")
        print("请确保已安装cx_Freeze，或者手动运行: pip install cx_freeze")
        return False

def main():
    """主函数"""
    args = parse_arguments()
    
    # 清理构建文件
    if args.clean:
        clean()
        if not (args.pyinstaller or args.cx_freeze or args.all):
            return
    
    # 安装依赖项
    if not install_requirements():
        return
    
    # 根据参数选择构建方式
    success = True
    
    if args.all or args.pyinstaller:
        success = success and build_with_pyinstaller()
    
    if args.all or args.cx_freeze:
        success = success and build_with_cx_freeze()
    
    # 如果没有指定构建方式，默认使用PyInstaller
    if not (args.pyinstaller or args.cx_freeze or args.all):
        success = build_with_pyinstaller()
    
    if success:
        print("\n构建成功！可执行文件位于dist目录中。")
    else:
        print("\n构建过程中出现错误，请检查上方日志。")

if __name__ == "__main__":
    main()
