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
            # 去掉 Category 为 Perception 的筛选条件
            if row['Stimulus'] == 'yes' and row['Response'] == 'yes' and row['Min_Num_Blocks'] != 'no':
                valid_names.append(row['Name_in_database'])

        # 获取源文件夹中的所有 CSV 文件
        csv_files = [f for f in os.listdir(source_folder) if f.endswith('.csv')]
        copied_count = 0

        block_keywords = ['block', 'blocks', 'Block', 'Blocks', 'BlockNumber', 'Block_count',
                          'Int.Block', 'block_type', 'BlockID', 'Block_Type', 'NumBlock', 'blocki']

        # 使用 tqdm 显示进度条
        for filename in tqdm(csv_files, desc="Processing CSV files"):
            # 修改匹配逻辑，只要 Name_in_database 的内容完全包含在 CSV 文件名中就认为匹配成功
            for valid_name in valid_names:
                if valid_name in filename:
                    file_path = os.path.join(source_folder, filename)
                    try:
                        # 读取 CSV 文件
                        data = pd.read_csv(file_path)
                        columns = data.columns

                        # 检查是否包含 Stimulus 列、Response 列以及 block 相关列
                        has_stimulus = 'Stimulus' in columns
                        has_response = 'Response' in columns
                        has_block = any(keyword in columns for keyword in block_keywords)

                        if has_stimulus and has_response and has_block:
                            source_file_path = os.path.join(source_folder, filename)
                            destination_file_path = os.path.join(destination_folder, filename)
                            # 复制文件到目标文件夹
                            shutil.copy2(source_file_path, destination_file_path)
                            copied_count += 1
                            break
                    except Exception as e:
                        print(f"读取 {filename} 时出现错误: {e}")

        print(f"成功筛选出 {copied_count} 个 CSV 数据。")

    except FileNotFoundError:
        print("错误: 文件或文件夹未找到!")
    except Exception as e:
        print(f"错误: 发生了一个未知错误: {e}")