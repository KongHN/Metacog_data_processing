from data_selection import process_xlsx_and_copy_csv
from data_separation import process_folder
from txt_selection import copy_txt_files

def main():
    # 设定每个文件夹读取和输出的路径
    all_data_folder = r"F:\科研\02Metacog-617\data test\test\all data"
    data_selection_folder = r"F:\科研\02Metacog-617\data test\test\data selection"
    data_separation_folder = r"F:\科研\02Metacog-617\data test\test\data separation"
    txt_folder = r"F:\科研\02Metacog-617\data test\test\all data"
    xlsx_path = r'F:\科研\02Metacog-617\data test\Database_Information.xlsx'

    while True:
        choice = input("请输入操作编号 (1: data selection, 2: data separate, 3: txt selection, 其他: 退出): ")
        if choice == '1':
            process_xlsx_and_copy_csv(xlsx_path, all_data_folder, data_selection_folder)
        elif choice == '2':
            process_folder(data_selection_folder, data_separation_folder)
        elif choice == '3':
            copy_txt_files(txt_folder, data_separation_folder)
        else:
            print("退出程序。")
            break

if __name__ == "__main__":
    main()