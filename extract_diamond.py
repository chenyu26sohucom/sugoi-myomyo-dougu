#!/usr/bin/env python3

import argparse
import os
import textwrap

def find_files(root_folder, filename):
    matched_files = []
    for dirpath, _, filenames in os.walk(root_folder):
        if filename in filenames:
            matched_files.append(os.path.join(dirpath, filename))
    return matched_files

def extract_sequences_from_file(input_fasta, identifiers, out_file):
    with open(input_fasta, 'r') as fasta_file:
        for line in fasta_file:
            fields = line.split()
            if fields and fields[0] in identifiers:
                out_file.write(line)

def extract_sequences_from_folders(folders, filename, identifiers, out_file):
    for folder in folders:
        matched_files = find_files(folder, filename)
        for input_fasta in matched_files:
            extract_sequences_from_file(input_fasta, identifiers, out_file)

def main():
    description = textwrap.dedent("""\
        根据标识符提取Diamond文件中对应的行内容。
        标识符文件可能需要从extract_filenames.py搞来
        如果只有单个输入文件，使用 -i。
        如果有多个输入文件，并且在不同文件夹里，使用 -n 和 -f。
        另外，如果这些文件夹有命名规律，比如 p01，p02 到 p5000，使用 -n, -p, -c 5000。
    """)
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-i', '--input', type=str, help="输入的单个文件")
    parser.add_argument('-f', '--folders', type=str, help="包含多个文件夹的路径（用逗号分隔）")
    parser.add_argument('-p', '--prefix', type=str, help="文件夹的前缀")
    parser.add_argument('-c', '--count', type=int, help="文件夹后面的编号")
    parser.add_argument('-n', '--filename', type=str, help="需要查找的文件名")
    parser.add_argument('-l', '--list', type=str, required=True, help="包含标识符的文件")
    parser.add_argument('-o', '--output', type=str, required=True, help="输出的文件")

    args = parser.parse_args()

    with open(args.list, 'r') as id_file:
        identifiers = set(line.strip() for line in id_file)

    with open(args.output, 'w') as out_file:
        if args.input:
            extract_sequences_from_file(args.input, identifiers, out_file)

        if args.folders and args.filename:
            folders = args.folders.split(',')
            extract_sequences_from_folders(folders, args.filename, identifiers, out_file)

        if args.prefix and args.count and args.filename:
            folders = [f"{args.prefix}{str(i).zfill(len(str(args.count)))}" for i in range(1, args.count + 1)]
            extract_sequences_from_folders(folders, args.filename, identifiers, out_file)

    print(f"提取的序列已写入 {args.output}。")

if __name__ == "__main__":
    main()
