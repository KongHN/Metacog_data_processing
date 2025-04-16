import os
import pandas as pd


def check_columns(data):
    """
    检查数据框是否包含所有必需列，返回缺失列列表，无缺失则返回空列表
    :param data: 要检查的pandas数据框
    :return: 缺失列列表
    """
    block_keywords = ['block', 'blocks', 'Block', 'Blocks', 'BlockNumber', 'Block_count',
                      'Int.Block', 'block_type', 'BlockID', 'Block_Type', 'NumBlock', 'blocki']
    required_keywords = ['Response', 'Confidence', 'Stimulus', 'Subj_idx']
    missing_columns = []
    block_found = False
    for keyword in block_keywords:
        if keyword in data.columns:
            block_found = True
            break
    if not block_found:
        missing_columns.append("one of block keywords")
    for keyword in required_keywords:
        keyword_found = False
        for col in data.columns:
            if keyword in col:
                keyword_found = True
                break
        if not keyword_found:
            missing_columns.append(keyword)
    return missing_columns


def split_data(data):
    """
    根据'Block'相关列将数据框均分为两部分
    :param data: 要分割的pandas数据框，需含'Block'相关列
    :return: 包含前后两部分数据框的元组
    """
    block_keywords = ['block', 'blocks', 'Block', 'Blocks', 'BlockNumber', 'Block_count',
                      'Int.Block', 'block_type', 'BlockID', 'Block_Type', 'NumBlock', 'blocki']
    block_column = None
    for keyword in block_keywords:
        if keyword in data.columns:
            block_column = keyword
            break
    if block_column is None:
        raise ValueError("No block-related column found in the DataFrame.")
    unique_blocks = sorted(data[block_column].unique())
    num_blocks = len(unique_blocks)
    if num_blocks % 2 == 1:
        del unique_blocks[num_blocks // 2]
    half_index = len(unique_blocks) // 2
    first_half = data[data[block_column].isin(unique_blocks[:half_index])]
    second_half = data[data[block_column].isin(unique_blocks[half_index:])]
    return first_half, second_half


def process_file(input_file_path, output_folder):
    """
    处理单个文件，读取、检查列、分割并保存数据
    :param input_file_path: 输入文件完整路径
    :param output_folder: 输出文件目标文件夹路径
    :return: 文件处理成功返回True，否则返回False
    """
    file_extension = os.path.splitext(input_file_path)[1].lower()
    supported_extensions = ['.xlsx', '.sav', '.csv']
    if file_extension not in supported_extensions:
        print(f"不支持的文件类型: {file_extension}，文件名: {os.path.basename(input_file_path)}")
        return False
    try:
        if file_extension == '.xlsx':
            data = pd.read_excel(input_file_path)
        elif file_extension == '.sav':
            data = pd.read_spss(input_file_path)
        elif file_extension == '.csv':
            data = pd.read_csv(input_file_path)
        missing_columns = check_columns(data)
        if missing_columns:
            missing_columns_str = ', '.join(missing_columns)
            print(f"{os.path.basename(input_file_path)}因缺少列{missing_columns_str}无法被分离。")
            return False
        first_half, second_half = split_data(data)
        file_name = os.path.basename(input_file_path)
        base_name, ext = os.path.splitext(file_name)
        # 创建以原文件名命名的文件夹
        file_output_folder = os.path.join(output_folder, base_name)
        os.makedirs(file_output_folder, exist_ok=True)
        output_file_1 = os.path.join(file_output_folder, f"{base_name}_part1{ext}")
        output_file_2 = os.path.join(file_output_folder, f"{base_name}_part2{ext}")
        if file_extension == '.xlsx':
            first_half.to_excel(output_file_1, index=False)
            second_half.to_excel(output_file_2, index=False)
        elif file_extension == '.sav':
            first_half.to_spss(output_file_1)
            second_half.to_spss(output_file_2)
        elif file_extension == '.csv':
            first_half.to_csv(output_file_1, index=False)
            second_half.to_csv(output_file_2, index=False)
        return True
    except Exception as e:
        print(f"处理文件{os.path.basename(input_file_path)}时出现错误: {e}")
        return False


def process_folder(input_folder, output_folder):
    """
    处理指定文件夹中的所有文件
    :param input_folder: 输入文件夹路径
    :param output_folder: 输出文件夹路径
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    success_count = 0
    fail_count = 0
    success_files = []
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            file_path = os.path.join(root, file)
            if process_file(file_path, output_folder):
                success_count += 1
                success_files.append(file)
            else:
                fail_count += 1
    print("\n成功分离的文件名:")
    for file in success_files:
        print(file)
    print(f"\n成功分离的数据文件数量: {success_count}")
    print(f"分离失败的数据文件数量: {fail_count}")
    print(f"分离后的数据地址: {output_folder}")