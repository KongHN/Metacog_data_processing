import os
import shutil
from tqdm import tqdm


def copy_txt_files(data_separation_folder, source_folder, output_folder):
    # 存储 data_separation_folder 中 csv 文件的关键信息
    csv_mapping = {}
    for root, _, files in os.walk(data_separation_folder):
        for file in files:
            if file.endswith('.csv') and file.startswith('data_'):
                # 提取 data_ 后面、_part 前面的部分
                start_index = file.find('data_') + 5
                end_index = file.find('_part')
                if end_index != -1:
                    key = file[start_index:end_index]
                    csv_mapping[key] = True

    # 遍历源文件夹，查找以 readme_ 开头的 .txt 文件
    txt_files = []
    for root, _, files in os.walk(source_folder):
        for file in files:
            if file.endswith('.txt') and file.startswith('readme_'):
                txt_files.append(file)

    copied_count = 0
    with tqdm(total=len(txt_files), desc="复制文件进度") as pbar:
        for file in txt_files:
            # 提取 readme_ 后面、.txt 前面的部分
            start_index = file.find('readme_') + 7
            end_index = file.find('.txt')
            match_key = file[start_index:end_index]
            if match_key in csv_mapping:
                source_file_path = os.path.join(source_folder, file)
                destination_file_path = os.path.join(output_folder, file)
                try:
                    shutil.copy2(source_file_path, destination_file_path)
                    copied_count += 1
                    pbar.set_postfix({"成功复制文件数": copied_count})
                except Exception as e:
                    print(f"复制 {file} 时出现错误: {e}")
            pbar.update(1)

    print(f"总共成功复制了 {copied_count} 个文件")
