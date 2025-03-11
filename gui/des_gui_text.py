import tkinter as tk
from tkinter import ttk
import binascii
import time
# 修改导入路径，使用绝对导入
from gui.des_gui_common import validate_key, generate_hex_key, show_warning, show_error, try_parse_encrypted

class TextEncryptionTab:
    def __init__(self, parent, des):
        """初始化文本加解密选项卡"""
        self.parent = parent
        self.des = des
        self.tab = ttk.Frame(parent)
        
        self.create_widgets()
    
    def create_widgets(self):
        """创建文本选项卡的界面元素"""
        # 密钥输入区域
        key_frame = ttk.LabelFrame(self.tab, text="密钥设置")
        key_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(key_frame, text="密钥 (16个十六进制字符):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.key_var = tk.StringVar(value="0123456789ABCDEF")
        self.key_entry = ttk.Entry(key_frame, textvariable=self.key_var, width=40)
        self.key_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        ttk.Button(key_frame, text="生成随机密钥", command=self.generate_key).grid(row=0, column=2, padx=5, pady=5)
        
        # 轮数设置
        ttk.Label(key_frame, text="DES轮数:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.rounds_var = tk.StringVar(value="16")
        rounds_values = ["1", "2", "4", "8", "12", "16", "24", "32"]
        self.rounds_combobox = ttk.Combobox(key_frame, textvariable=self.rounds_var, values=rounds_values, width=10)
        self.rounds_combobox.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        # 添加分组密码模式选择
        ttk.Label(key_frame, text="分组密码模式:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.mode_var = tk.StringVar(value="ECB")
        mode_values = ["ECB", "CBC", "CFB", "OFB", "CTR"]
        self.mode_combobox = ttk.Combobox(key_frame, textvariable=self.mode_var, values=mode_values, width=10)
        self.mode_combobox.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.mode_combobox.bind("<<ComboboxSelected>>", self.on_mode_changed)
        
        # 添加初始化向量(IV)输入
        self.iv_frame = ttk.Frame(key_frame)
        self.iv_frame.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky="ew")
        ttk.Label(self.iv_frame, text="初始向量 (IV):").pack(side="left", padx=5)
        self.iv_var = tk.StringVar(value="0000000000000000")
        self.iv_entry = ttk.Entry(self.iv_frame, textvariable=self.iv_var, width=30)
        self.iv_entry.pack(side="left", padx=5, expand=True, fill="x")
        ttk.Button(self.iv_frame, text="随机IV", command=self.generate_iv).pack(side="left", padx=5)
        
        # 添加计数器初始值输入(用于CTR模式)
        self.counter_frame = ttk.Frame(key_frame)
        self.counter_frame.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky="ew")
        ttk.Label(self.counter_frame, text="计数器初始值:").pack(side="left", padx=5)
        self.counter_var = tk.StringVar(value="0")
        self.counter_entry = ttk.Entry(self.counter_frame, textvariable=self.counter_var, width=20)
        self.counter_entry.pack(side="left", padx=5)
        self.counter_frame.grid_remove()  # 默认隐藏计数器选项
        
        # 文本输入/输出区域
        input_frame = ttk.LabelFrame(self.tab, text="输入文本")
        input_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.input_text = tk.Text(input_frame, height=8)
        self.input_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # 操作按钮
        button_frame = ttk.Frame(self.tab)
        button_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(button_frame, text="加密", command=self.encrypt_text).pack(side="left", padx=5)
        ttk.Button(button_frame, text="解密", command=self.decrypt_text).pack(side="left", padx=5)
        ttk.Button(button_frame, text="清除", command=self.clear_text).pack(side="right", padx=5)
        
        # 输出区域
        output_frame = ttk.LabelFrame(self.tab, text="输出结果")
        output_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.output_text = tk.Text(output_frame, height=8)
        self.output_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # 状态区域
        self.status_var = tk.StringVar(value="就绪")
        ttk.Label(self.tab, textvariable=self.status_var).pack(side="left", padx=10, pady=5)
        
        # 初始化UI状态
        self.on_mode_changed(None)
    
    def on_mode_changed(self, event):
        """当分组密码模式改变时调整UI"""
        mode = self.mode_var.get()
        if mode == "ECB":
            self.iv_frame.grid_remove()
            self.counter_frame.grid_remove()
        elif mode == "CTR":
            self.iv_frame.grid_remove()
            self.counter_frame.grid()
        else:  # CBC, CFB, OFB
            self.iv_frame.grid()
            self.counter_frame.grid_remove()
    
    def generate_key(self):
        """生成随机密钥"""
        self.key_var.set(generate_hex_key())
    
    def generate_iv(self):
        """生成随机初始化向量"""
        self.iv_var.set(generate_hex_key())
    
    def encrypt_text(self):
        """加密文本"""
        try:
            plaintext = self.input_text.get("1.0", "end-1c")
            key = self.key_var.get()
            mode = self.mode_var.get()
            iv = None
            counter = None
            
            if not plaintext:
                show_warning("警告", "请输入要加密的文本")
                return
                
            if not validate_key(key):
                show_warning("警告", "密钥必须是16个十六进制字符")
                return
                
            try:
                rounds = int(self.rounds_var.get())
                if rounds <= 0:
                    rounds = 16
                    self.rounds_var.set("16")
            except ValueError:
                rounds = 16
                self.rounds_var.set("16")
            
            # 处理IV和计数器
            if mode in ["CBC", "CFB", "OFB"]:
                iv_hex = self.iv_var.get()
                if not validate_key(iv_hex):
                    show_warning("警告", "初始向量必须是16个十六进制字符")
                    return
                iv = bytes.fromhex(iv_hex)
            elif mode == "CTR":
                try:
                    counter = int(self.counter_var.get())
                    if counter < 0:
                        counter = 0
                        self.counter_var.set("0")
                except ValueError:
                    counter = 0
                    self.counter_var.set("0")
                
            self.status_var.set("正在加密...")
            self.tab.update()
            
            start_time = time.time()
            encrypted = self.des.encrypt(plaintext, key, rounds=rounds, mode=mode, iv=iv, counter=counter)
            end_time = time.time()
            
            # 以多种格式显示加密结果
            hex_result = binascii.hexlify(encrypted).decode()
            base64_result = binascii.b2a_base64(encrypted).decode().strip()
            
            result = f"十六进制: {hex_result}\n\nBase64: {base64_result}\n\n"
            result += f"处理时间: {(end_time - start_time):.4f} 秒\n"
            result += f"使用轮数: {rounds}\n"
            result += f"密钥: {key}\n"
            result += f"分组模式: {mode}"
            if mode in ["CBC", "CFB", "OFB"]:
                result += f"\n初始向量: {self.iv_var.get()}"
            elif mode == "CTR":
                result += f"\n计数器初始值: {self.counter_var.get()}"
            
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", result)
            
            self.status_var.set("加密完成")
            
        except Exception as e:
            self.status_var.set(f"加密出错: {str(e)}")
            show_error("错误", f"加密过程中出现错误: {str(e)}")
    
    def decrypt_text(self):
        """解密文本"""
        try:
            encrypted_text = self.input_text.get("1.0", "end-1c").strip()
            key = self.key_var.get()
            mode = self.mode_var.get()
            iv = None
            counter = None
            
            if not encrypted_text:
                show_warning("警告", "请输入要解密的文本")
                return
                
            if not validate_key(key):
                show_warning("警告", "密钥必须是16个十六进制字符")
                return
            
            encrypted = try_parse_encrypted(encrypted_text)
            if encrypted is None:
                show_error("错误", "输入的文本不是有效的十六进制或Base64格式")
                return
                
            try:
                rounds = int(self.rounds_var.get())
                if rounds <= 0:
                    rounds = 16
                    self.rounds_var.set("16")
            except ValueError:
                rounds = 16
                self.rounds_var.set("16")
            
            # 处理IV和计数器
            if mode in ["CBC", "CFB", "OFB"]:
                iv_hex = self.iv_var.get()
                if not validate_key(iv_hex):
                    show_warning("警告", "初始向量必须是16个十六进制字符")
                    return
                iv = bytes.fromhex(iv_hex)
            elif mode == "CTR":
                try:
                    counter = int(self.counter_var.get())
                    if counter < 0:
                        counter = 0
                        self.counter_var.set("0")
                except ValueError:
                    counter = 0
                    self.counter_var.set("0")
                
            self.status_var.set("正在解密...")
            self.tab.update()
            
            start_time = time.time()
            decrypted = self.des.decrypt(encrypted, key, rounds=rounds, mode=mode, iv=iv, counter=counter)
            end_time = time.time()
            
            try:
                decoded_text = decrypted.decode('utf-8')
                result = f"解密文本: {decoded_text}\n\n"
            except UnicodeDecodeError:
                hex_result = binascii.hexlify(decrypted).decode()
                result = f"解密结果 (二进制，无法显示为文本):\n十六进制: {hex_result}\n\n"
            
            result += f"处理时间: {(end_time - start_time):.4f} 秒\n"
            result += f"使用轮数: {rounds}\n"
            result += f"密钥: {key}\n"
            result += f"分组模式: {mode}"
            if mode in ["CBC", "CFB", "OFB"]:
                result += f"\n初始向量: {self.iv_var.get()}"
            elif mode == "CTR":
                result += f"\n计数器初始值: {self.counter_var.get()}"
            
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", result)
            
            self.status_var.set("解密完成")
            
        except Exception as e:
            self.status_var.set(f"解密出错: {str(e)}")
            show_error("错误", f"解密过程中出现错误: {str(e)}")
    
    def clear_text(self):
        """清除输入和输出文本框"""
        self.input_text.delete("1.0", "end")
        self.output_text.delete("1.0", "end")
        self.status_var.set("就绪")