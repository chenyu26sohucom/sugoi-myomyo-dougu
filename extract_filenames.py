#!/usr/bin/env python3

import os
import argparse

def extract_filenames(folder_prefix, folder_count, class_folders, output_file, suffix, path_format):
    # 打开输出文件
    with open(output_file, "w") as outfile:
        # 遍历从p01到p50的每个文件夹
        for i in range(1, folder_count + 1):
            folder_name = f"{folder_prefix}{i:02d}"
            for class_folder in class_folders:
                # 使用 path_format 格式化路径
                class_folder_path = path_format.format(folder=folder_name, class_folder=class_folder)
                if os.path.exists(class_folder_path):
                    # 获取分类文件夹中的所有文件
                    for file_name in os.listdir(class_folder_path):
                        if file_name.endswith(suffix):
                            # 去掉文件的后缀
                            file_name_without_suffix = file_name[: -len(suffix)]
                            # 写入输出文件
                            outfile.write(file_name_without_suffix + "\n")
    print(f"文件名提取并写入 {output_file} 完成。")

def main():
    parser = argparse.ArgumentParser(description="提取文件名并去掉后缀，如果文件位于不同文件夹下，提取文件名就很费劲，所以用这个脚本解决。一般来说，最后的输出结果会作为标识符，用于脚本extract_diamond.py或者extract_sequence.py")
    parser.add_argument('-p', '--prefix', type=str, required=True, help="目标文件夹的前缀")
    parser.add_argument('-c', '--count', type=int, required=True, help="目标文件夹的数量")
    parser.add_argument('-o', '--output', type=str, required=True, help="输出文件的路径")
    parser.add_argument('-l', '--list', type=str, required=True, nargs='+', help="分类文件夹的名称列表，用空格分隔")
    parser.add_argument('-d', '--suffix', type=str, required=True, help="要去掉的文件后缀，例如 '.nexus'")
    parser.add_argument('-f', '--format', type=str, required=True, help="分类文件夹路径的格式，使用 {folder} 和 {class_folder} 作为占位符，例如 '{folder}/avp_classify_mid-sensitive/classification/{class_folder}'")

    args = parser.parse_args()

    extract_filenames(args.prefix, args.count, args.list, args.output, args.suffix, args.format)

if __name__ == "__main__":
    main()
