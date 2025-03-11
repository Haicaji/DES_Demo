import tkinter as tk
from tkinter import ttk, filedialog
import os
import time
import threading
# 修改导入路径，使用绝对导入
from gui.des_gui_common import validate_key, generate_hex_key, show_warning, show_error, show_info

class FileEncryptionTab:
    def __init__(self, parent, des):
        """初始化文件加解密选项卡"""
        self.parent = parent
        self.des = des
        self.tab = ttk.Frame(parent)
        self.processing_file = False
        
        self.create_widgets()
    
    def create_widgets(self):
        """创建文件选项卡的界面元素"""
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
        
        # 文件选择区域
        file_frame = ttk.LabelFrame(self.tab, text="文件选择")
        file_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(file_frame, text="输入文件:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.input_file_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.input_file_var, width=50).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(file_frame, text="浏览", command=self.browse_input_file).grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Label(file_frame, text="输出文件:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.output_file_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.output_file_var, width=50).grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(file_frame, text="浏览", command=self.browse_output_file).grid(row=1, column=2, padx=5, pady=5)
        
        # 操作按钮
        button_frame = ttk.Frame(self.tab)
        button_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(button_frame, text="加密文件", command=self.encrypt_file).pack(side="left", padx=5)
        ttk.Button(button_frame, text="解密文件", command=self.decrypt_file).pack(side="left", padx=5)
        
        # 进度条
        progress_frame = ttk.LabelFrame(self.tab, text="处理进度")
        progress_frame.pack(fill="x", padx=10, pady=5)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill="x", padx=5, pady=5)
        
        # 结果区域
        result_frame = ttk.LabelFrame(self.tab, text="处理结果")
        result_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.result_text = tk.Text(result_frame, height=8)
        self.result_text.pack(fill="both", expand=True, padx=5, pady=5)
        
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
    
    def browse_input_file(self):
        """浏览输入文件"""
        filename = filedialog.askopenfilename(title="选择输入文件")
        if filename:
            self.input_file_var.set(filename)
            # 默认设置输出文件名
            base_dir = os.path.dirname(filename)
            base_name = os.path.basename(filename)
            output_filename = os.path.join(base_dir, "encrypted_" + base_name)
            self.output_file_var.set(output_filename)
    
    def browse_output_file(self):
        """浏览输出文件"""
        filename = filedialog.asksaveasfilename(title="选择输出文件位置")
        if filename:
            self.output_file_var.set(filename)
    
    def update_progress_periodically(self, file_size):
        """定期更新进度条"""
        if not self.processing_file:
            return
        
        if os.path.exists(self.output_file_var.get()):
            try:
                output_size = os.path.getsize(self.output_file_var.get())
                progress = min(100, (output_size / file_size) * 100)
                self.progress_var.set(progress)
            except:
                pass
            
            self.tab.after(200, lambda: self.update_progress_periodically(file_size))
    
    def encrypt_file(self):
        """加密文件"""
        input_file = self.input_file_var.get()
        output_file = self.output_file_var.get()
        key = self.key_var.get()
        mode = self.mode_var.get()
        iv = None
        counter = None
        
        if not input_file:
            show_warning("警告", "请选择输入文件")
            return
            
        if not output_file:
            show_warning("警告", "请指定输出文件")
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
        
        try:
            if not os.path.exists(input_file):
                show_error("错误", f"文件 '{input_file}' 不存在")
                return
                
            # 获取文件大小
            file_size = os.path.getsize(input_file)
            
            self.status_var.set("正在加密文件...")
            self.progress_var.set(0)
            self.tab.update()
            
            # 启动处理标志
            self.processing_file = True
            
            # 开始周期性更新进度
            self.tab.after(200, lambda: self.update_progress_periodically(file_size))
            
            # 使用线程执行加密，避免界面卡死
            def encrypt_thread():
                try:
                    start_time = time.time()
                    
                    # 读取文件内容
                    with open(input_file, 'rb') as f:
                        data = f.read()
                    
                    # 加密数据，传递模式、IV和计数器
                    encrypted = self.des.encrypt(data, key, rounds=rounds, mode=mode, iv=iv, counter=counter)
                    
                    # 写入输出文件
                    with open(output_file, 'wb') as f:
                        f.write(encrypted)
                    
                    end_time = time.time()
                    
                    # 更新界面
                    self.tab.after(0, self.update_result_ui, 
                                  "加密完成", file_size, len(encrypted), 
                                  end_time - start_time, rounds, key, mode, iv, counter)
                except Exception as e:
                    self.tab.after(0, self.show_error, str(e))
                finally:
                    self.processing_file = False
            
            # 启动线程
            thread = threading.Thread(target=encrypt_thread)
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            self.processing_file = False
            self.status_var.set(f"加密出错: {str(e)}")
            show_error("错误", f"加密过程中出现错误: {str(e)}")
    
    def decrypt_file(self):
        """解密文件"""
        input_file = self.input_file_var.get()
        output_file = self.output_file_var.get()
        key = self.key_var.get()
        mode = self.mode_var.get()
        iv = None
        counter = None
        
        if not input_file:
            show_warning("警告", "请选择输入文件")
            return
            
        if not output_file:
            show_warning("警告", "请指定输出文件")
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
        
        try:
            if not os.path.exists(input_file):
                show_error("错误", f"文件 '{input_file}' 不存在")
                return
                
            # 获取文件大小
            file_size = os.path.getsize(input_file)
            
            self.status_var.set("正在解密文件...")
            self.progress_var.set(0)
            self.tab.update()
            
            # 启动处理标志
            self.processing_file = True
            
            # 开始周期性更新进度
            self.tab.after(200, lambda: self.update_progress_periodically(file_size))
            
            # 使用线程执行解密，避免界面卡死
            def decrypt_thread():
                try:
                    start_time = time.time()
                    
                    # 读取文件内容
                    with open(input_file, 'rb') as f:
                        data = f.read()
                    
                    # 解密数据，传递模式、IV和计数器
                    decrypted = self.des.decrypt(data, key, rounds=rounds, mode=mode, iv=iv, counter=counter)
                    
                    # 写入输出文件
                    with open(output_file, 'wb') as f:
                        f.write(decrypted)
                    
                    end_time = time.time()
                    
                    # 更新界面
                    self.tab.after(0, self.update_result_ui, 
                                   "解密完成", len(data), len(decrypted), 
                                   end_time - start_time, rounds, key, mode, iv, counter)
                except Exception as e:
                    self.tab.after(0, self.show_error, str(e))
                finally:
                    self.processing_file = False
            
            # 启动线程
            thread = threading.Thread(target=decrypt_thread)
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            self.processing_file = False
            self.status_var.set(f"解密出错: {str(e)}")
            show_error("错误", f"解密过程中出现错误: {str(e)}")
    
    def update_result_ui(self, status, input_size, output_size, process_time, rounds, key, mode=None, iv=None, counter=None):
        """更新文件处理结果界面"""
        self.status_var.set(status)
        self.progress_var.set(100)
        
        result = f"{status}!\n"
        result += f"输入文件大小: {input_size} 字节\n"
        result += f"输出文件大小: {output_size} 字节\n"
        result += f"处理时间: {process_time:.4f} 秒\n"
        result += f"处理速度: {(input_size / process_time / 1024):.2f} KB/s\n"
        result += f"使用轮数: {rounds}\n"
        result += f"密钥: {key}"
        
        if mode:
            result += f"\n分组模式: {mode}"
            if mode in ["CBC", "CFB", "OFB"] and iv:
                result += f"\n初始向量: {self.iv_var.get()}"
            elif mode == "CTR" and counter is not None:
                result += f"\n计数器初始值: {counter}"
        
        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", result)
    
    def show_error(self, error_msg):
        """显示文件处理错误"""
        self.status_var.set(f"处理出错: {error_msg}")
        self.progress_var.set(0)
        show_error("错误", f"处理过程中出现错误: {error_msg}")