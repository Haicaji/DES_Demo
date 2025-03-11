import random
import tkinter as tk
from tkinter import messagebox
import binascii

def generate_hex_key(length=16):
    """生成指定长度的十六进制随机密钥"""
    key = ''.join(random.choice('0123456789ABCDEF') for _ in range(length))
    return key

def validate_key(key):
    """验证密钥是否为有效的十六进制字符串"""
    if not key or len(key) != 16 or not all(c in "0123456789ABCDEFabcdef" for c in key):
        return False
    return True

def show_error(title, message):
    """显示错误消息框"""
    messagebox.showerror(title, message)

def show_warning(title, message):
    """显示警告消息框"""
    messagebox.showwarning(title, message)

def show_info(title, message):
    """显示信息消息框"""
    messagebox.showinfo(title, message)

def format_time(seconds):
    """格式化时间为易读字符串"""
    return f"{seconds:.4f} 秒"

def format_speed(bytes_count, seconds):
    """计算并格式化处理速度"""
    if seconds <= 0:
        return "N/A"
    return f"{(bytes_count / seconds / 1024):.2f} KB/s"

def try_decode_bytes(data):
    """尝试将字节解码为文本，如果失败返回None"""
    try:
        return data.decode('utf-8')
    except UnicodeDecodeError:
        return None

def try_parse_encrypted(text):
    """尝试解析加密的文本（十六进制或Base64格式）"""
    try:
        # 先尝试以十六进制解析
        try:
            return binascii.unhexlify(text.strip())
        except:
            # 如果失败，尝试以Base64解析
            return binascii.a2b_base64(text.strip())
    except:
        return None
