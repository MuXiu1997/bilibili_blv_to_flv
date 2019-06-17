import asyncio
import os
import tkinter as tk
from tkinter.filedialog import askdirectory

import converter


class Wind(tk.Frame):
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('360x160+885+465')
        self.root.resizable(0, 0)
        super().__init__()
        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.pack()
        self.main_window()
        self.root.mainloop()

    # 主窗口
    def main_window(self):
        tk.Label(self.root, text='选择输入路径:').place(x=140, y=10)
        tk.Entry(self.root, textvariable=self.input_path, width=40).place(x=2, y=35)
        tk.Button(self.root, text='选择',
                  command=lambda: self.select_path(self.input_path)).place(x=305, y=30)

        tk.Label(self.root, text='选择输出路径:').place(x=140, y=68)
        tk.Entry(self.root, textvariable=self.output_path, width=40).place(x=2, y=93)
        tk.Button(self.root, text='选择',
                  command=lambda: self.select_path(self.output_path)).place(x=305, y=88)

        confirmation_button = tk.Button(self.root, text='确定', command=self.confirmation, fg='white', bg='black',
                                        activeforeground='white', activebackground='navy', width=8, height=1)
        confirmation_button.place(x=6, y=122)

        quit_button = tk.Button(self.root, text='取消', command=lambda: quit(), fg='white', bg='black',
                                activeforeground='white', activebackground='red', width=8, height=1)
        quit_button.place(x=288, y=122)

    # 设置地址的回调函数
    @staticmethod
    def select_path(string_var):
        _path = askdirectory()
        string_var.set(_path)

    # 确认按钮的回调函数
    def confirmation(self):
        self.root.quit()

    # 实例被作为函数调用时的魔法方法
    def __call__(self):
        # 返回两个地址框中的文本
        return self.input_path.get(), self.output_path.get()


if __name__ == '__main__':

    input_path, output_path = Wind()()

    list_dir = list(map(lambda file_name: os.path.join(input_path, file_name), os.listdir(input_path)))
    loop = asyncio.get_event_loop()
    tasks = [converter.concat(each_dir, output_path) for each_dir in list_dir]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
