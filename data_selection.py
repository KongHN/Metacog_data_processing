import pandas as pd
import os
import shutil
from tqdm import tqdm


def process_xlsx_and_copy_csv(xlsx_path, source_folder, destination_folder):
    try:
        # 读取 xlsx 文件
        df = pd.read_excel(xlsx_path)

        # 存储满足条件的 Name_in_database 列的值
        valid_names = []
        for index, row in df.iterrows():
            if row['Stimulus'] == 'yes' and row['Response'] == 'yes' and row['Num_Blocks'] != 'no':
                valid_names.append(row['Name_in_database'])

        # 获取源文件夹中的所有 CSV 文件
        csv_files = [f for f in os.listdir(source_folder) if f.endswith('.csv')]
        copied_count = 0

        # 使用 tqdm 显示进度条
        for filename in tqdm(csv_files, desc="Processing CSV files"):
            # 提取 csv 文件名中 data_ 后 .csv 前的部分
            name_part = filename.split('data_')[-1].split('.csv')[0]
            if name_part in valid_names:
                source_file_path = os.path.join(source_folder, filename)
                destination_file_path = os.path.join(destination_folder, filename)
                # 复制文件到目标文件夹
                shutil.copy2(source_file_path, destination_file_path)
                copied_count += 1

        print(f"成功筛选出 {copied_count} 个 CSV 数据。")

    except FileNotFoundError:
        print("错误: 文件或文件夹未找到!")
    except Exception as e:
        print(f"错误: 发生了一个未知错误: {e}")