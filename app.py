import sys
import argparse
import os

# 确保能够从当前目录导入模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 使用绝对导入
from gui.des_gui import main as gui_main

def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='DES加密解密工具 - 支持所有类型的文件加密')
    parser.add_argument('--cli', action='store_true', help='使用命令行界面而非图形界面')
    return parser.parse_args()

def main():
    """
    程序主入口函数
    该程序可以加密解密任何类型文件，包括文本文件、图像、视频、音频等二进制文件，
    唯一的限制是文件大小，因为需要将文件加载到内存中进行处理。
    """
    args = parse_arguments()
    
    if args.cli:
        # 如果指定了使用CLI界面
        try:
            from cli.des_cli import main as cli_main
            cli_main()
        except ImportError as e:
            print(f"错误：命令行界面模块无法导入: {e}")
            print("请使用GUI界面或检查安装。")
            sys.exit(1)
    else:
        # 默认使用图形界面
        gui_main()

if __name__ == "__main__":
    main()
