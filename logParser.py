import tkinter as tk
from tkinter import filedialog, messagebox


class LogParserGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Log Parser")

        # 设置网格布局权重，使得组件可以自适应窗口大小
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.recognizer_var = tk.StringVar()
        self.expand_button_var = tk.StringVar(value="▼")
        self.log_content_var = tk.StringVar()
        self.extracted_fields = {}

        self.create_widgets()

    def create_widgets(self):
        # 第一行：Recognizer
        recognizer_label = tk.Label(self.root, text="Recognizer")
        recognizer_label.grid(row=0, column=0, padx=10, pady=10)

        recognizer_entry = tk.Entry(self.root, textvariable=self.recognizer_var, width=50)
        recognizer_entry.grid(row=0, column=1, padx=10, pady=10)

        escape_label = tk.Label(self.root, text="特殊字符需转义")
        escape_label.grid(row=0, column=2, padx=10, pady=10)

        # 第二行：展开/合上按钮、日志内容
        expand_button = tk.Button(self.root, textvariable=self.expand_button_var, command=self.toggle_log_content)
        expand_button.grid(row=1, column=0, padx=10, pady=10)

        log_content_text = tk.Text(self.root, height=2)
        log_content_text.grid(row=1, column=1, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.log_content_text = log_content_text

        add_log_button = tk.Button(self.root, text="增加日志", command=self.add_log_window)
        add_log_button.grid(row=1, column=3, padx=10, pady=10)

        # 第四行：提取日志字段按钮
        extract_button = tk.Button(self.root, text="提取日志字段", command=self.extract_log_fields)
        extract_button.grid(row=2, column=1,  padx=10, pady=10)

        # 设置网格布局权重，使得日志内容文本框可以自动扩展
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(1, weight=1)


    def toggle_log_content(self):
        if self.log_content_text.cget("height") == 1:
            self.log_content_text.config(height=6)
            self.expand_button_var.set("▼")
        else:
            self.log_content_text.config(height=1)
            self.expand_button_var.set("▲")

    def add_log_window(self):
        add_log_window = tk.Toplevel(self.root)
        add_log_window.title("Add Log")

        log_entry_label = tk.Label(add_log_window, text="复制一行日志或上传日志文件：")
        log_entry_label.pack(padx=10, pady=10)

        log_entry = tk.Entry(add_log_window, textvariable=self.log_content_var, width=50)
        log_entry.pack(padx=10, pady=10)

        upload_button = tk.Button(add_log_window, text="上传日志文件", command=self.upload_log_file)
        upload_button.pack(padx=10, pady=10)

        confirm_button = tk.Button(add_log_window, text="确认", command=lambda: self.confirm_log(add_log_window))
        confirm_button.pack(padx=10, pady=10)

        cancel_button = tk.Button(add_log_window, text="取消", command=add_log_window.destroy)
        cancel_button.pack(padx=10, pady=10)

    def upload_log_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                log_content = file.read()
                self.log_content_var.set(log_content)

    def confirm_log(self, add_log_window):
        log_content = self.log_content_var.get()
        self.log_content_text.insert(tk.END, log_content + "\n")
        add_log_window.destroy()

    def extract_log_fields(self):
        log_content = self.log_content_text.get("1.0", tk.END).strip()
        fields = log_content.split(";")
        self.extracted_fields = {}

        for field in fields:
            if ":" in field:
                key, value = field.split(":", 1)
                key = key.strip()
                value = value.strip()
                self.extracted_fields[key] = value

        self.display_extracted_fields()

    def display_extracted_fields(self):

        row_index = 4
        col_index = 0
        padx_value = 1

        frame = tk.Frame(self.root)
        frame.grid(row=4, column=0, columnspan=5, padx=10, pady=20)


        for key, value in self.extracted_fields.items():
            # key_button = tk.Button(self.root, text=key, bg="lightblue", command=lambda k=key: self.on_key_click(k))
            # key_button.grid(row=row_index, column=col_index, padx=padx_value, pady=5, sticky="w")
            key_button = tk.Button(frame, text=key, bg="lightblue", command=lambda k=key: self.on_key_click(k))
            key_button.pack(side=tk.LEFT,  padx=padx_value, pady=20)

            # value_button = tk.Button(self.root, text=value, bg="lightgray", command=lambda v=value: self.on_value_click(v))
            # value_button.grid(row=row_index, column=col_index+1, padx=padx_value+1, pady=5, sticky="w")
            value_button = tk.Button(frame, text=value, bg="lightgray", command=lambda v=value: self.on_value_click(v))
            value_button.pack(side=tk.LEFT, padx=padx_value, pady=20)

            # row_index += 1
            # col_index += 2

    def on_key_click(self, key):
        messagebox.showinfo("Key", key)

    def on_value_click(self, value):
        messagebox.showinfo("Value", value)


if __name__ == "__main__":
    root = tk.Tk()
    app = LogParserGUI(root)
    root.mainloop()
