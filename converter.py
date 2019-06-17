# 获取blv文件所在目录
import json
import os
import re


async def get_blv_dir(path):
    list_all = list(map(lambda x: os.path.join(path, x), os.listdir(path)))
    return list(filter(lambda x: os.path.isdir(x), list_all))[0]


# 从entry.json获取输出文件名
async def get_output_file_name(path):
    json_file = os.path.join(path, 'entry.json')
    with open(json_file, encoding='utf-8') as json_file_obj:
        output_file_name = json.load(json_file_obj)['page_data']['part']
        for each_char in r'\/:*?"<>|':
            output_file_name.replace(each_char, '-')
    return ''.join((output_file_name, '.flv'))


# 获取需要写入concat.txt的文本
async def get_txt_file_str(blv_dir):
    blv_file_list = list(filter(lambda x: re.search(r'.+\.blv$', x), os.listdir(blv_dir)))
    txt_file_str = ''
    for blv_file in blv_file_list:
        txt_file_str_append = "'".join(("file ", blv_file.replace('\\', '/') + "\n"))
        txt_file_str = ''.join((txt_file_str, txt_file_str_append))
    return txt_file_str


# 写入concat.txt文件
async def write_txt_file(txt_file_path, txt_file_str):
    with open(txt_file_path, mode='w') as txt_file_obj:
        txt_file_obj.write(txt_file_str)


# 执行转换程序
async def cmd_ffmpeg(txt_file_path, output_path, output_file_name):
    command = 'ffmpeg -f concat -safe 0 -i {} -c copy "{}/{}" -y' \
        .format(txt_file_path, output_path, output_file_name)
    os.system(command)


async def concat(subdirectories, _output_path):
    path = subdirectories
    blv_dir = await get_blv_dir(path)
    txt_file_path = os.path.join(blv_dir, 'concat.txt').replace('\\', '/')

    output_file_name = await get_output_file_name(path)

    txt_file_str = await get_txt_file_str(blv_dir)

    await write_txt_file(txt_file_path, txt_file_str)

    await cmd_ffmpeg(txt_file_path, _output_path, output_file_name)
