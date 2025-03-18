from data_selection import filter_and_save_files
from data_separation import process_folder
from txt_selection import copy_txt_files

def main():
    # 设定每个文件夹读取和输出的路径
    all_data_folder = r"C:\Users\孔昊男\Desktop\all data"
    data_selection_folder = r"C:\Users\孔昊男\Desktop\data selection"
    data_separation_folder = r"C:\Users\孔昊男\Desktop\data separation"
    txt_folder = r"C:\Users\孔昊男\Desktop\txt"

    while True:
        choice = input("请输入操作编号 (1: data selection, 2: data separate, 3: txt selection, 其他: 退出): ")
        if choice == '1':
            filter_and_save_files(all_data_folder, data_selection_folder)
        elif choice == '2':
            process_folder(data_selection_folder, data_separation_folder)
        elif choice == '3':
            copy_txt_files(txt_folder, data_separation_folder)
        else:
            print("退出程序。")
            break

if __name__ == "__main__":
    main()