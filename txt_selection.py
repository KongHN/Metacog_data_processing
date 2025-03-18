import os
import shutil
from tqdm import tqdm

def copy_txt_files(source_folder, output_folder):
    # 存储输出文件夹中以 data_ 开头的文件夹的关键信息
    output_folder_mapping = {}
    for item in os.listdir(output_folder):
        item_path = os.path.join(output_folder, item)
        if os.path.isdir(item_path) and item.startswith('data_'):
            # 提取 data_ 后面、( 前面的部分
            index = item.find('(')
            if index != -1:
                key = item[5:index]
            else:
                key = item[5:]
            output_folder_mapping[key] = item_path

    # 遍历源文件夹，查找以 readme_ 开头的 .txt 文件
    txt_files = []
    for root, _, files in os.walk(source_folder):
        for file in files:
            if file.endswith('.txt') and file.startswith('readme_'):
                txt_files.append(file)

    copied_count = 0
    with tqdm(total=len(txt_files), desc="复制文件进度") as pbar:
        for file in txt_files:
            match_key = file[7:file.find('.txt')]
            if match_key in output_folder_mapping:
                source_file_path = os.path.join(source_folder, file)
                destination_folder = output_folder_mapping[match_key]
                destination_file_path = os.path.join(destination_folder, file)
                try:
                    shutil.copy2(source_file_path, destination_file_path)
                    copied_count += 1
                    pbar.set_postfix({"成功复制文件数": copied_count})
                except Exception as e:
                    print(f"复制 {file} 时出现错误: {e}")
            pbar.update(1)

    print(f"总共成功复制了 {copied_count} 个文件")