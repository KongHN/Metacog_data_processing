from data_selection import process_xlsx_and_copy_csv
from data_separation import process_folder
from txt_selection import copy_txt_files
import os

def main():
    # 通过 input 获取 all_data_folder 和 xlsx_path
    all_data_folder = input("请输入所有数据文件夹的路径 (all_data_folder): ")
    xlsx_path = input("请输入 xlsx 文件的路径 (xlsx_path): ")

    txt_folder = all_data_folder  # txt_folder 的本地地址和 all_data_folder 的地址是一样的

    # 动态生成 data_selection_folder 和 data_separation_folder 的路径
    parent_folder = os.path.dirname(all_data_folder)
    data_selection_folder = os.path.join(parent_folder, "data selection")
    data_separation_folder = os.path.join(parent_folder, "data separation")

    # 创建文件夹
    if not os.path.exists(data_selection_folder):
        os.makedirs(data_selection_folder)
    if not os.path.exists(data_separation_folder):
        os.makedirs(data_separation_folder)

    while True:
        choice = input("请输入操作编号 (1: data selection, 2: data separate, 3: txt selection, 其他: 退出): ")
        if choice == '1':
            process_xlsx_and_copy_csv(xlsx_path, all_data_folder, data_selection_folder)
        elif choice == '2':
            process_folder(data_selection_folder, data_separation_folder)
        elif choice == '3':
            # 提供完整的三个参数
            copy_txt_files(data_separation_folder, txt_folder, data_separation_folder)
        else:
            print("退出程序。")
            break

if __name__ == "__main__":
    main()