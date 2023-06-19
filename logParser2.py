import tkinter as tk
from tkinter import filedialog, messagebox


class LogParserGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Log Parser")

        self.recognizer_var = tk.StringVar()
        self.expand_button_var = tk.StringVar(value="+")
        self.log_content_var = tk.StringVar()
        self.extracted_fields = {}
        self.var_check_enable = tk.StringVar(value="0")
        self.regex_patterns = []


        self.frame_recog = tk.Frame(self.root)
        self.var_frame_all = tk.Frame(self.root)
        self.frame_var = tk.Frame(self.var_frame_all)
        self.add_var = tk.Button(self.var_frame_all, text="+", command=self.add_regex_pattern)
        self.create_widgets()

    def create_widgets(self):
        # 第一行：Recognizer   
        self.frame_recog.pack(side="top", pady=2, fill=tk.X)
        recognizer_label = tk.Label(self.frame_recog, text="Recognizer")
        recognizer_label.pack(side="left", padx=10, pady=10)

        recognizer_entry = tk.Entry(self.frame_recog, textvariable=self.recognizer_var, width=50)
        recognizer_entry.pack(side="left", padx=10, pady=10)

        escape_label = tk.Label(self.frame_recog, text="特殊字符需转义")
        escape_label.pack(side="left", padx=10, pady=10)

        # 添加Recognizer确认按钮
        confirm_button = tk.Button(self.frame_recog, text="确认", command=self.confirm_recognizer)
        confirm_button.pack(side="right", padx=10, pady=10)
        
        # 定义正则变量   
        var_input_enable = tk.Checkbutton(self.root, text="define regex pattern", variable=self.var_check_enable, command=self.var_input_enable_check)
        var_input_enable.pack(side="top",pady=2,anchor="w")
        self.var_frame_all.pack(side="top",pady=2,anchor="w")
        
        # 日志内容
        log_frame_first = tk.Frame(self.root)
        log_frame_first.pack(side="top",pady=2,anchor="w")

        log_lable = tk.Label(log_frame_first, text="log content")
        log_lable.pack(side="left", padx=10, pady=10,anchor="w")
        add_log_button = tk.Button(log_frame_first, text="+", command=self.add_log_window)
        add_log_button.pack(side="left",pady=2)

        log_frame_content = tk.Frame(self.root)
        log_frame_content.pack(side="top",pady=2,anchor="w")
        log_content_text = tk.Text(log_frame_content, height=2)
        log_content_text.pack(side="left",pady=2)
        self.log_content_text = log_content_text
        log_content_parse = tk.Button(log_frame_content,text="parse",command=self.parse_log)
        log_content_parse.pack(side="left",pady=2)
        
        # 属性赋值
        attribution_frame_first = tk.Frame(self.root)
        attribution_frame_first.pack(side="top",pady=2,fill=tk.X)
        attribut_label = tk.Label(attribution_frame_first, text="event attribute")
        attribut_label.pack(side="left", padx=1, pady=1)
        attr_value = tk.StringVar()
        attr_values = ["eventType","vendor","srcIp"]
        attr_value.set(attr_values[0])
        atrribut_combox = tk.OptionMenu(attribution_frame_first, attr_value, *attr_values
                                       )
        atrribut_combox.pack(side="left", padx=1, pady=1)
        attribut_value_label = tk.Label(attribution_frame_first, text="attribute value type")
        attribut_value_label.pack(side="left", padx=1, pady=1)
        attr_type_value = tk.StringVar()
        attr_type_values = ["static value", "variable value", "function value"]
        attr_type_value.set(attr_type_values[0])       
        atrribut_combox = tk.OptionMenu(attribution_frame_first, attr_type_value,*attr_type_values)
        atrribut_combox.pack(side="left", padx=1, pady=1)
        attribut_value_label = tk.Label(attribution_frame_first, text="value")
        attribut_value_label.pack(side="left", padx=1, pady=1)
        attribut_value = tk.Text(attribution_frame_first, height=1, width=10)
        attribut_value.pack(side="left", padx=2)
        attr_add_button = tk.Button(attribution_frame_first,text="+",command=self.add_attribute)
        attr_add_button.pack(side="left", padx=1, pady=1)
    
    def confirm_recognizer(self):
        # Recognizer确认
        recognizer_value = self.recognizer_var.get()
        messagebox.showinfo("确认", f"已确认 Recognizer 值为: {recognizer_value}")
        print("Recognizer: " + recognizer_value)
    
    def var_input_enable_check(self):
        if self.var_check_enable.get() == "1":
            self.add_var.pack(side="top", padx=10, pady=10,anchor="w")
            self.frame_var.pack(side="top", pady=2, fill=tk.X)          
        else:
            self.frame_var.pack_forget()
            self.add_var.pack_forget()

    def add_regex_pattern(self):
        frame_var_first = tk.Frame(self.frame_var)
        frame_var_first.confirmed = False  # 添加confirmed属性并初始化为False
        frame_var_first.pack(side="top", pady=2, fill=tk.X)

        var_label_name = tk.Label(frame_var_first, text="variable name")
        var_label_name.pack(side="left", padx=1, pady=1)
        var_name_text = tk.Text(frame_var_first, height=1, width=10)
        var_name_text.pack(side="left", padx=2)

        var_label_pattern = tk.Label(frame_var_first, text="pattern")
        var_label_pattern.pack(side="left", padx=1, pady=1)
        var_pattern_text = tk.Text(frame_var_first, height=1, width=20)
        var_pattern_text.pack(side="left", padx=2)

        var_confirm_button = tk.Button(frame_var_first, text="确认", command=lambda frame=frame_var_first, name=var_name_text, pattern=var_pattern_text: self.confirm_regex_pattern(frame, name, pattern))
        var_confirm_button.pack(side="left", padx=2)

        var_pattern_del = tk.Button(frame_var_first, text="-", command=lambda frame=frame_var_first: self.del_regex_pattern(frame))
        var_pattern_del.pack(side="left", padx=2)

    def del_regex_pattern(self, frame):
        var_name_text = frame.winfo_children()[1]
        var_pattern_text = frame.winfo_children()[3]
        var_name = var_name_text.get("1.0", tk.END).strip()
        var_pattern = var_pattern_text.get("1.0", tk.END).strip()
        self.regex_patterns.remove((var_name, var_pattern))
        frame.destroy()
        print("Regex Patterns:", self.regex_patterns)

    def confirm_regex_pattern(self, frame, name_text, pattern_text):
        if frame.confirmed:
            return

        var_name = name_text.get("1.0", tk.END).strip()
        var_pattern = pattern_text.get("1.0", tk.END).strip()
        self.regex_patterns.append((var_name, var_pattern))
        frame.confirmed = True  # 将confirmed属性设置为True

        # 设置文本框、确认按钮为不可编辑
        name_text.configure(state="disabled", bg="gray")
        pattern_text.configure(state="disabled", bg="gray")
        # frame.winfo_children()[3].configure(state="disabled", bg="gray")
        
        print("Regex Patterns:", self.regex_patterns)
    
    def parse_log(self):
        return
    
    def add_attribute(self):
        return
    
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
        log_content = self.log_content_text.get("1.0", tk.END).strip() #1.0: 第一行第一个字符
        fields = log_content.split(";")
        self.extracted_fields = {}

        for field in fields:
            if ":" in field:
                key, value = field.split(":", 1)
                key = key.strip()
                value = value.strip()
                self.extracted_fields[key] = value

        self.display_extracted_fields()

        extracted_log = self.extracted_fields
        print(extracted_log)

    def display_extracted_fields(self):
        # 清除旧的字段显示
        for widget in self.frame.winfo_children():
            widget.destroy()

        padx_value = 1
        row_index = 0

        for key, value in self.extracted_fields.items():
            key_button = tk.Button(self.frame, text=key, bg="lightblue", command=lambda k=key: self.on_key_click(k))
            key_button.grid(row=row_index, column=0, padx=padx_value, pady=20)

            value_button = tk.Button(self.frame, text=value, bg="lightgray", command=lambda v=value: self.on_value_click(v))
            value_button.grid(row=row_index, column=1, padx=padx_value, pady=20)

            row_index += 1

    def on_key_click(self, key):
        new_key = tk.simpledialog.askstring("Modify Key", "Enter a new value for the key:", initialvalue=key)
        if new_key is not None:
            if new_key != key:
                value = self.extracted_fields[key]
                del self.extracted_fields[key]
                self.extracted_fields[new_key] = value
                self.display_extracted_fields()

    def on_value_click(self, value):
        new_value = tk.simpledialog.askstring("Modify Value", "Enter a new value for the value:", initialvalue=value)
        if new_value is not None:
            if new_value != value:
                for key, val in self.extracted_fields.items():
                    if val == value:
                        self.extracted_fields[key] = new_value
                self.display_extracted_fields()


root = tk.Tk()
app = LogParserGUI(root)
root.mainloop()
