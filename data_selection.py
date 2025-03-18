import os
import pandas as pd
import pyreadstat
from tqdm import tqdm

def filter_and_save_files(input_folder, output_folder):
    # 定义需要筛选的关键词
    required_columns = ['Block', 'Response', 'Confidence', 'Stimulus', 'Subj_idx']
    # 检查输出文件夹是否存在，如果不存在则创建
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    # 用于存储符合条件的输出文件名
    valid_files = []
    # 统计筛选成功和失败的文件个数
    success_count = 0
    fail_count = 0

    # 收集所有要处理的文件
    all_files = []
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith(('.xlsx', '.csv', '.sav')):
                all_files.append(os.path.join(root, file))

    # 用 tqdm 创建进度条
    for file_path in tqdm(all_files, desc="文件筛选进度", unit="文件"):
        file = os.path.basename(file_path)
        # 检查文件名是否包含 'unpub'，如果包含则跳过该文件
        if 'unpub' in file.lower():
            fail_count += 1
            continue
        try:
            if file.endswith('.xlsx'):
                df = pd.read_excel(file_path)
            elif file.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file.endswith('.sav'):
                df, _ = pyreadstat.read_sav(file_path)
            # 获取列名
            columns = df.columns.tolist()
            # 检查列名是否包含所有所需的关键词
            has_required_columns = all(
                any(keyword in col for col in columns) for keyword in required_columns
            )
            if has_required_columns:
                # 检查是否包含Accuracy列
                has_accuracy = 'Accuracy' in columns
                # 检查数据中是否含有NaN
                has_nan = df.isna().any().any()
                # 构建输出文件名
                file_name, file_ext = os.path.splitext(file)
                if not has_accuracy:
                    file_name = f"{file_name}(no Acc)"
                if has_nan:
                    file_name = f"{file_name}(NAN)"
                output_file_name = f"{file_name}{file_ext}"
                output_file = os.path.join(output_folder, output_file_name)

                if file.endswith('.xlsx'):
                    df.to_excel(output_file, index=False, na_rep='NAN')
                elif file.endswith('.csv'):
                    df.to_csv(output_file, index=False, na_rep='NAN')
                elif file.endswith('.sav'):
                    pyreadstat.write_sav(df, output_file)
                valid_files.append(output_file_name)
                success_count += 1
            else:
                fail_count += 1
        except Exception as e:
            # 打印处理文件时出现的错误信息
            print(f"处理文件 {file_path} 时出错: {e}")
            fail_count += 1
    # 打印符合条件的所有输出文件的名字
    if valid_files:
        print(f"已保存筛选后的数据到 {output_folder}")
        print("符合条件的输出文件有：")
        for valid_file in valid_files:
            print(valid_file)
    else:
        print("没有符合条件的文件。")
    # 打印筛选成功和失败的个数
    print(f"筛选成功的文件个数: {success_count}")
    print(f"筛选失败的文件个数: {fail_count}")