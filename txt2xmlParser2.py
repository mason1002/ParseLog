import tkinter as tk
from tkinter import filedialog

def split_fields(log_line):
    pairs = log_line.strip().split(';')
    fields = {}
    for pair in pairs:
        key, value = pair.split(':', 1)
        fields[key.strip()] = value.strip()
    return fields

def concatenate_fields():
    selected_fields = [field_listbox.get(idx).split(':')[0].strip() for idx in field_listbox.curselection()]
    concatenated_text = ' '.join(selected_fields)
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, concatenated_text)

def show_selected_product(selected_product):
    result_text.insert(tk.END, f"Selected Product: {selected_product}\n")

def display_fields(log_lines):
    field_listbox.delete(0, tk.END)
    if len(log_lines) > 0:
        log_line = log_lines[0]
        fields = split_fields(log_line)
        for key, value in fields.items():
            # key_label = tk.Label(field_listbox, text=f"{key}: ", bg="lightblue", relief=tk.RAISED)
            key_label = tk.Label(field_listbox, text=f"{key.replace(':', '')} ", bg="lightblue", relief=tk.RAISED)
            key_label.bind("<Button-1>", lambda event, key=key: concatenate_field(key))
            value_label = tk.Label(field_listbox, text=value, bg="lightgray", relief=tk.SUNKEN)
            key_label.pack(side=tk.LEFT)
            value_label.pack(side=tk.LEFT)
        log_lines.pop(0)



def concatenate_field(key):
    current_text = result_text.get("1.0", tk.END).strip()
    if current_text:
        current_text += " "
    current_text += key
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, current_text)

def next_log():
    concatenate_fields()
    display_fields(log_lines)  # 读取并显示新的一行日志
    next_button.config(state=tk.DISABLED)
    end_button.config(state=tk.NORMAL)

def end_concatenation():
    end_button.config(state=tk.DISABLED)
    result_text.insert(tk.END, "\nEnd of File (EOF)")

root = tk.Tk()
root.title("Field Concatenation")

# 添加产品类型下拉框
product_label = tk.Label(root, text="Product Type:")
product_label.pack()

product_var = tk.StringVar()
product_var.set("请选择产品类型")
product_dropdown = tk.OptionMenu(root, product_var, "深信服", "绿盟", command=lambda value: show_selected_product(value))
product_dropdown.pack()

# 添加上传按钮
def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as file:
            global log_lines
            log_lines = file.readlines()
        display_fields(log_lines)

upload_button = tk.Button(root, text="上传", command=upload_file)
upload_button.pack()

# 添加字段列表框
field_listbox_frame = tk.Frame(root, bd=1, relief=tk.SUNKEN)
field_listbox_frame.pack(fill=tk.BOTH, expand=True)

field_listbox = tk.Listbox(field_listbox_frame)
field_listbox.pack(fill=tk.BOTH, expand=True)

# 添加拼接按钮
concatenate_button = tk.Button(root, text="拼接字段", command=concatenate_fields)
concatenate_button.pack()

# 添加文本框
result_text = tk.Text(root, height=10, width=50)
result_text.pack(fill=tk.BOTH, expand=True)

# 添加下一行和结束拼接按钮
button_frame = tk.Frame(root)
button_frame.pack(fill=tk.BOTH, expand=True)

next_button = tk.Button(button_frame, text="下一行", command=next_log)
next_button.pack(side=tk.LEFT)

end_button = tk.Button(button_frame, text="结束拼接", command=end_concatenation, state=tk.DISABLED)
end_button.pack(side=tk.LEFT)

root.mainloop()
