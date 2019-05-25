"""
........................................................................................................................
........................................................................................................................
........................................................................................................................
...........##...............##..........................................................................................
...........###.............####.........................................................................................
..........#####...........####..........................................................................................
...........#####.........#####....................#...................................##................................
............#####.......#####..................#####................................####................................
...........#######....#########..............#######..............................######................................
....#################################........#######.............................#######................................
...###################################.......#######.................#####........######..................#####.........
..#####################################......#######.................#####........######..................#####.........
.#######################################......######..................####........######..................#####.........
.#######################################......######..................####........######..................#####.........
.#####............................######......######..................####........######..................#####.........
######.............................#####......######...............#..####.........#####................#..####.........
######.............................#####......######............#####.####..#####..#####.............#####.####..####...
######.............................#####......######............#####.#####.#####..#####.............#####.#####.#####..
######.......###.........###.......#####......######............###########.#####..#####.............#####.####..#####..
######..#########.......#########..#####......######............###########.#####..#####.............#####.#####.#####..
######.##########.......#########..#####.......#####............###########.#####..######............#####.#####.#####..
######..#########.......#########..#####.......#####.............####..####.#####..######.............####.#####.#####..
######..######.............######..#####.......#####..............####.####........######..............###.#####........
######..##.........................#####.......#####.............#####.####.#####...#####.............#####.####.#####..
######.............................#####.......#####.............#####.##########...#####.............#####.####.#####..
######.............................#####.......#####.............#####.##########...#####.............#####.####.#####..
######..............#..............#####........##########.......#####..#########...##########........#####.####.#####..
######.........##..###..#..........#####........##############....####..#########...##############....##########.#####..
######.........###########.........#####........################..#####.#########...#################.##########.#####..
######..........#########..........#####........#######################.#########....###########################.#####..
######...........##...#............#####........#######################.####.####....#################################..
######.............................#####........#######..##############.####.####....#######..##############.#########..
######.............................#####........#######...#############.#########....#######..##############.####.####..
.######...........................######........#######..#########.##############....#######..##############.####.####..
.#######################################........#################..#########.####....#################..####.####.####..
..#####################################.........################...#####.###.####....###############....####..###.####..
..#####################################.........##############......###......####....##############.....###.......####..
...###################################...........###########.........................###########........................
....################################.............########............................#########..........................
........#####...............#####.......................................................................................
.........###.................##.........................................................................................
........................................................................................................................
........................................................................................................................
........................................................................................................................
........................................................................................................................
"""

import asyncio
import json
import os
import re
import tkinter as tk
from tkinter.filedialog import askdirectory


async def fun_json_file_obj(json_file):
    return open(json_file, encoding='utf-8')


async def fun_txt_file_obj(txt_file_path, txt_file_str):
    with open(txt_file_path, mode='w') as txt_file_obj:
        txt_file_obj.write(txt_file_str)


async def fun_ffmpeg(txt_file_path, output_path, output_file_name):
    output_file_path = os.path.join(output_path, output_file_name).replace(' ', '_')
    for each_char in r'\/:*?"<>|':
        output_file_path.replace(each_char, '-')
    os.system("ffmpeg -f concat -safe 0 -i {} -c copy {} -y"
              .format(txt_file_path.replace('\\', '/'), output_file_path))


async def concat(each_dir, output_path, json_file='entry.json'):
    json_file_obj = await fun_json_file_obj(os.path.join(each_dir, json_file))

    output_file_name = json.load(json_file_obj)['page_data']['part'] + '.flv'
    for each_char in r'\/:*?"<>|':
        output_file_name.replace(each_char, '-')
    list_all = list(map(lambda x: os.path.join(each_dir, x), os.listdir(each_dir)))
    _dir = list(filter(lambda x: os.path.isdir(x), list_all))[0]
    # list_all_file = list(map(lambda x: os.path.join(_dir, x), os.listdir(_dir)))
    # blv_file_list = list(filter(lambda x: re.search(r'.+\.blv$', x), list_all_file))
    blv_file_list = list(filter(lambda x: re.search(r'.+\.blv$', x), os.listdir(_dir)))
    txt_file_str = ''
    for blv_file in blv_file_list:
        txt_file_str += "file '" + blv_file.replace('\\', '/') + "'\n"
    txt_file_path = os.path.join(_dir, 'concat.txt')

    await fun_txt_file_obj(txt_file_path, txt_file_str)

    await fun_ffmpeg(txt_file_path, output_path, output_file_name)


class Wind(tk.Frame):
    def __init__(self):
        global root
        root = tk.Tk()
        root.geometry('360x160+885+465')
        root.resizable(0, 0)
        super().__init__()
        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.pack()
        self.main_window()
        root.mainloop()

    def main_window(self):
        global root
        tk.Label(root, text='选择输入路径:').place(x=140, y=10)
        tk.Entry(root, textvariable=self.input_path, width=40).place(x=2, y=35)
        tk.Button(root, text='选择',
                  command=lambda: self.select_path(self.input_path)).place(x=305, y=30)

        tk.Label(root, text='选择输出路径:').place(x=140, y=68)
        tk.Entry(root, textvariable=self.output_path, width=40).place(x=2, y=93)
        tk.Button(root, text='选择',
                  command=lambda: self.select_path(self.output_path)).place(x=305, y=88)

        conformation_button = tk.Button(root, text='确定', command=self.concat, fg='white', bg='black',
                                        activeforeground='white', activebackground='navy', width=8, height=1)
        conformation_button.place(x=6, y=122)

        quit_button = tk.Button(root, text='取消', command=lambda: quit(), fg='white', bg='black',
                                activeforeground='white', activebackground='red', width=8, height=1)
        quit_button.place(x=288, y=122)

    def concat(self):
        ConcatBiliVideo(self.input_path.get(), self.output_path.get()).run()
        root.quit()

    @staticmethod
    def select_path(string_var):
        _path = askdirectory()
        string_var.set(_path)


class ConcatBiliVideo(object):
    def __init__(self, base_path, output_path):
        self.base_path = base_path
        self.list_dir = list(map(lambda x: os.path.join(self.base_path, x), os.listdir(self.base_path)))
        self.output_path = output_path

    def run(self):
        loop = asyncio.get_event_loop()
        tasks = [concat(each_dir, self.output_path) for each_dir in self.list_dir]
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()


if __name__ == '__main__':
    Wind()
