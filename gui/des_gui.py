import tkinter as tk
from tkinter import ttk
# 修改导入路径，使用绝对导入
from core.des import DES
from gui.des_gui_text import TextEncryptionTab
from gui.des_gui_file import FileEncryptionTab

class DESApplication:
    def __init__(self, root):
        """初始化DES GUI应用程序"""
        self.root = root
        self.root.title("DES加解密工具")
        self.root.geometry("700x600")
        self.root.minsize(600, 500)
        
        # 创建DES实例
        self.des = DES()
        
        # 创建选项卡控件
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 创建并添加文本加解密选项卡
        self.text_tab = TextEncryptionTab(self.notebook, self.des)
        self.notebook.add(self.text_tab.tab, text="文本加解密")
        
        # 创建并添加文件加解密选项卡
        self.file_tab = FileEncryptionTab(self.notebook, self.des)
        self.notebook.add(self.file_tab.tab, text="文件加解密")
        
        # 底部状态栏
        status_frame = ttk.Frame(root)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=5, pady=2)
        
        ttk.Label(status_frame, text="DES加解密工具 - 支持自定义轮数").pack(side=tk.LEFT)
        ttk.Label(status_frame, text="版本: 1.0").pack(side=tk.RIGHT)

def main():
    """主函数"""
    root = tk.Tk()
    app = DESApplication(root)
    root.mainloop()

if __name__ == "__main__":
    main()