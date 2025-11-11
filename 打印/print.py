import socket
import time
import tkinter as tk
from tkinter import ttk, messagebox

# ---------------------- 打印机核心类（保留原有功能并优化） ----------------------
class BrotherPrinter:
    def __init__(self, ip, port=9100, encoding="gbk"):
        self.ip = ip
        self.port = port
        self.encoding = encoding
        self.socket = None
        self.is_connected = False  # 连接状态标识

    def connect(self):
        """建立TCP连接，返回连接状态"""
        try:
            if self.is_connected:
                return True  # 已连接则直接返回
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.ip, self.port))
            self.is_connected = True
            return True
        except Exception as e:
            self.is_connected = False
            raise Exception(f"连接失败：{str(e)}")

    def send_pcl_command(self, command):
        """发送PCL6指令，检查连接状态"""
        if not self.is_connected:
            raise Exception("未建立打印机连接，请先点击【连接打印机】")
        try:
            self.socket.send(command)
            return True
        except Exception as e:
            self.is_connected = False
            raise Exception(f"指令发送失败：{str(e)}")

    # 保留原有初始化、字体设置、文本打印、进纸、结束打印、关闭连接方法
    def initialize_printer(self):
        init_cmd = b"\x1B%-12345X@PJL JOB NAME=\"Python GUI Print\"\r\n"
        init_cmd += b"\x1B(E"  # 启用PCL文本模式
        return self.send_pcl_command(init_cmd)

    def set_font(self, size=12, bold=False):
        if not (10 <= size <= 72):
            raise Exception("字体大小需在10-72之间")
        font_cmd = b"\x1B(s" + f"{size}".encode() + b"H"  # 高度
        font_cmd += b"\x1B(s" + f"{size//2}".encode() + b"W"  # 宽度（1/2高度）
        font_cmd += b"\x1B&d1B" if bold else b"\x1B&d0B"
        return self.send_pcl_command(font_cmd)

    def print_text(self, text, new_line=True):
        try:
            text_bytes = text.encode(self.encoding, errors="replace")
            if new_line:
                text_bytes += b"\r\n"
            return self.send_pcl_command(text_bytes)
        except UnicodeEncodeError as e:
            raise Exception(f"编码错误（仅支持{self.encoding}）：{str(e)}")

    def feed_paper(self, lines=1):
        feed_cmd = b"\r\n" * lines
        return self.send_pcl_command(feed_cmd)

    def end_print(self):
        end_cmd = b"\x1B%-12345X"
        return self.send_pcl_command(end_cmd)

    def close(self):
        if self.socket and self.is_connected:
            self.socket.close()
            self.is_connected = False

    def get_printer_status(self):
        """获取打印机状态信息"""
        if not self.is_connected:
            raise Exception("未建立打印机连接")
        try:
            status_cmd = b"\x1B%-12345X@PJL INFO STATUS\r\n"
            self.socket.send(status_cmd)
            response = self.socket.recv(1024)
            return response.decode("ascii", errors="ignore")
        except Exception as e:
            raise Exception(f"获取状态失败: {str(e)}")


# ---------------------- 简化版GUI界面（仅IP打印） ----------------------
class PrinterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Brother打印机IP打印工具")
        self.root.geometry("600x400")  # 更小的窗口尺寸
        self.root.resizable(width=False, height=False)  # 固定大小
        
        # 全局样式
        self.style = ttk.Style()
        self.font_normal = ("Microsoft YaHei", 10)
        self.font_title = ("Microsoft YaHei", 11, "bold")
        
        # 主框架
        main_frame = ttk.Frame(root, padding=(20, 20))
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 1. 打印机连接设置
        ttk.Label(main_frame, text="打印机IP连接设置", style="Title.TLabel").pack(pady=10)
        
        ip_frame = ttk.Frame(main_frame)
        ip_frame.pack(pady=5)
        ttk.Label(ip_frame, text="IP地址:").grid(row=0, column=0, padx=5)
        self.ip_entry = ttk.Entry(ip_frame, width=20)
        self.ip_entry.grid(row=0, column=1, padx=5)
        self.ip_entry.insert(0, "192.168.1.103")
        
        port_frame = ttk.Frame(main_frame)
        port_frame.pack(pady=5)
        ttk.Label(port_frame, text="端口:").grid(row=0, column=0, padx=5)
        self.port_entry = ttk.Entry(port_frame, width=10)
        self.port_entry.grid(row=0, column=1, padx=5)
        self.port_entry.insert(0, "9100")
        
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=10)
        self.connect_btn = ttk.Button(btn_frame, text="连接打印机", command=self.connect_printer)
        self.connect_btn.pack(side=tk.LEFT, padx=5)
        self.close_btn = ttk.Button(btn_frame, text="断开连接", command=self.close_printer, state=tk.DISABLED)
        self.close_btn.pack(side=tk.LEFT, padx=5)
        self.status_btn = ttk.Button(btn_frame, text="查询状态", command=self.check_printer_status, state=tk.DISABLED)
        self.status_btn.pack(side=tk.LEFT, padx=5)
        
        self.status_label = ttk.Label(main_frame, text="状态: 未连接", style="Normal.TLabel")
        self.status_label.pack(pady=10)
        
        # 2. 文本打印区域
        ttk.Label(main_frame, text="打印内容:").pack(pady=5)
        self.text_input = tk.Text(main_frame, height=10, width=50, wrap=tk.WORD)
        self.text_input.pack(pady=5)
        self.text_input.insert(tk.END, "请输入要打印的文本内容...")
        
        # 3. 打印按钮
        self.print_btn = ttk.Button(main_frame, text="打印", command=self.print_text_gui, state=tk.DISABLED)
        self.print_btn.pack(pady=10)
        
        # 初始化打印机实例
        self.printer = None

    def check_printer_status(self):
        """查询打印机状态"""
        try:
            if not (self.printer and self.printer.is_connected):
                raise Exception("请先连接打印机")
                
            status = self.printer.get_printer_status()
            messagebox.showinfo("打印机状态", status)
        except Exception as e:
            messagebox.showerror("错误", f"获取状态失败:\n{str(e)}")

    # 连接打印机
    def connect_printer(self):
        try:
            ip = self.ip_entry.get().strip()
            port = int(self.port_entry.get().strip())

            if not ip:
                raise Exception("打印机IP不能为空")
            if not (1 <= port <= 65535):
                raise Exception("端口需在1-65535之间")

            self.printer = BrotherPrinter(ip=ip, port=port, encoding="gbk")
            if self.printer.connect():
                self.status_label.config(text=f"状态: 已连接到 {ip}:{port}")
                self.connect_btn.config(state=tk.DISABLED)
                self.close_btn.config(state=tk.NORMAL)
                self.status_btn.config(state=tk.NORMAL)
                self.print_btn.config(state=tk.NORMAL)
            else:
                raise Exception("连接返回失败")
        except Exception as e:
            self.status_label.config(text=f"错误: {str(e)}")
            messagebox.showerror("连接错误", f"连接打印机失败:\n{str(e)}")

    # 断开打印机连接
    def close_printer(self):
        if self.printer:
            self.printer.close()
            self.status_label.config(text="状态: 已断开连接")
            self.connect_btn.config(state=tk.NORMAL)
            self.close_btn.config(state=tk.DISABLED)
            self.status_btn.config(state=tk.DISABLED)
            self.print_btn.config(state=tk.DISABLED)
            self.printer = None


    # 文本打印
    def print_text_gui(self):
        try:
            if not (self.printer and self.printer.is_connected):
                raise Exception("请先连接打印机")

            text = self.text_input.get("1.0", tk.END).strip()
            if not text:
                raise Exception("打印内容不能为空")

            # 使用默认字体设置(12号字)
            self.printer.initialize_printer()
            self.printer.set_font(size=12)
            self.printer.print_text(text)
            self.printer.feed_paper(lines=2)
            self.printer.end_print()
            
            messagebox.showinfo("成功", "文本打印任务已发送")
        except Exception as e:
            messagebox.showerror("错误", f"打印失败:\n{str(e)}")



if __name__ == "__main__":
    root = tk.Tk()
    app = PrinterGUI(root)
    root.mainloop()
