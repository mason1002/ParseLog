import tkinter as tk
from tkinter import filedialog
import xml.etree.ElementTree as ET

class GUI:
    def __init__(self, master):
        self.master = master
        master.title("log parser")

        # 创建产品下拉框
        product_types = ["深信服", "绿盟", "QIZHI"]
        selected_product = tk.StringVar()
        selected_product.set(product_types[2])
        product_menu = tk.OptionMenu(master, selected_product, *product_types)
        product_menu.pack()

        # 创建Label显示“选择要解析的log文件”
        # self.label = tk.Label(master, text="选择要解析的log文件")
        # self.label.pack()

        # 创建Button让用户选择txt文件
        self.button = tk.Button(master, text="选择要解析的log文件", command=self.open_file)
        self.button.pack()

        # 创建一个Text框，用于显示txt文件内容和XML格式
        self.text = tk.Text(master)
        self.text.pack()
        # 如果要自适应窗口
        # scrollbar = tk.Scrollbar(master)
        # scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # self.text = tk.Text(master, yscrollcommand=scrollbar.set)
        # self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # scrollbar.config(command=self.text.yview)
        # self.text.insert(tk.END, "hi")

        # 创建几个关键字key value框
        # self.text = tk.Text(master)
        # self.text.pack()
        key_ziduan = ["id", "time", "source"]
        ziduan_value = ["123", "2023-4-18", "0.0.0.0"]

        for i in range(len(key_ziduan)):
        #     label_key = tk.Label(master, text = key_ziduan[i])
        #     label_value = tk.Label(master, text = ziduan_value[i])
        #     input_box = tk.Entry(master)

        #     label_key.grid(row=i, column=0)
        #     label_value.grid(row=i, column=1)
        #     input_box.grid(row=i, column=2)
            # 创建一个Frame作为容器
            frame = tk.Frame(master)
            frame.pack(side=tk.TOP)

            # 创建label显示关键词
            label_key = tk.Label(frame, text=key_ziduan[i], width=10, padx=5)
            label_key.pack(side=tk.LEFT)

            label_value = tk.Label(frame, text=ziduan_value[i], width=20, padx=10)
            label_value.pack(side=tk.RIGHT)

            # 创建entry接收用户输入的值
            entry_value = tk.Entry(frame, width=20)
            entry_value.insert(tk.END, "可手动修改关键词")
            entry_value.pack(side=tk.LEFT)



        # pairs = self.parse_data
        # for idx, (key, value) in (pairs):
        #     label_key = tk.Label(root, text=key)
        #     label_value = tk.Label(root, text=value)
        #     manual_input_box = tk.Entry(master)

        #     label_key.grid(row=idx, column=0)
        #     label_value.grid(row=idx, column=1)
        #     manual_input_box.grid(row=idx, column=2)



        # 创建提交Button
        self.button = tk.Button(master, text = "Submit", command=self.submit)
        self.button.pack()



    def parse_data(self):
    # TODO 解析提取字段
        with open("keywords.txt", "r") as f:
            lines = f.readlines()
        # 循环遍历每一行，将每个关键词和其对应的值存储为一个元组，并附加到pairs列表中
        pairs = []
        for line in lines:
            key, value = line.strip().split(",")
            pairs.append((key, value))
        return pairs

    def convert_to_xml(self):
    # TODO 转换数据为XML格式的代码
        pass

    
    def open_file(self):
    # TODO 创建上传方法
        # 打开文件对话框，让用户选择要上传的txt文件
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])

        # 如果用户选择了文件，将其内容显示在Text框中，解析数据并将其转换为XML格式
        if file_path:
            with open(file_path, "r", encoding='utf-8') as file:
                content = file.read()
                self.text.insert(tk.END, content)

                # 将txt内容转换为XML格式
                # root = ET.Element("root")
                # element = ET.SubElement(root, "content")
                # element.text = content
                # xml_content = ET.tostring(root)
                # self.text.insert(tk.END, "\n\nXML格式:\n\n")
                # self.text.insert(tk.END, xml_content)

                # parse_data(content)
                # convert_to_xml(content)

    
    def submit(self):
    # TODO 创建提交方法
        pass


# 创建GUI实例
root = tk.Tk()
gui = GUI(root)
root.mainloop()