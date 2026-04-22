import os
 
 
def find_large_files(path, size_limit):
    """
    查找指定路径下大于指定大小的文件，并返回文件路径和大小的字典。
 
    参数:
        path (str): 搜索的路径。
        size_limit (int): 文件大小限制，单位为字节。
 
    返回:
        dict: 包含文件路径和大小的字典，键为文件路径，值为文件大小。
    """
    large_files = {}
 
    # 检查路径是否有效
    if not os.path.exists(path):
        print(f"路径 '{path}' 不存在.")
        return large_files
 
    # 检查大小限制是否为正数
    if size_limit <= 0:
        print("大小限制必须为正数.")
        return large_files
 
    try:
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                # 获取文件大小
                try:
                    file_size = os.path.getsize(file_path)
                    # 判断文件大小是否大于指定大小，如果是则添加到字典中
                    if file_size > size_limit:
                        large_files[file_path] = file_size
                        print(f'{file_path}: {file_size / (1024 * 1024):.2f} MB')
                except PermissionError:
                    print(f"没有权限访问文件 '{file_path}'.")
                except Exception as e:
                    print(f"在获取文件大小时出错: {e}")
        # 根据文件大小降序排列
        large_files = {k: v for k, v in sorted(large_files.items(), key=lambda x: x[1], reverse=True)}
    except Exception as e:
        print(f"在查找大文件时出错: {e}")
 
    return large_files
 
 
def save_results_to_txt(files_dict, output_file, size_limit_mb):
    """
    将查找结果保存到txt文件
 
    参数:
        files_dict (dict): 文件路径和大小的字典
        output_file (str): 输出文件路径
        size_limit_mb (float): 大小限制（MB）
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            # 写入标题信息
            f.write("=" * 60 + "\n")
            f.write(f"大文件查找结果报告\n")
            f.write(f"生成时间: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"大小限制: > {size_limit_mb:.2f} MB\n")
            f.write(f"找到文件数: {len(files_dict)}\n")
            f.write("=" * 60 + "\n")
             
            if files_dict:
                f.write("文件路径                       文件大小(MB)\n")
                f.write("-" * 60 + "\n")
                 
                total_size = 0
                for file, size in files_dict.items():
                    size_mb = size / (1024 * 1024)
                    f.write(f"{file}    {size_mb:.2f} MB\n")
                    total_size += size
                 
                f.write("-" * 60 + "\n")
                f.write(f"总计: {len(files_dict)} 个文件\n")
                f.write(f"总大小: {total_size / (1024 * 1024):.2f} MB\n")
            else:
                f.write("没有找到大于指定大小的文件。\n")
         
        print(f"结果已保存到文件: {output_file}\n")
    except Exception as e:
        print(f"保存结果到文件时出错: {e}\n")
 
 
def main():
    # 指定路径
    
    root = r"D:\\"
     
    size_limit_mb = 50
    size_limit_bytes = size_limit_mb * 1024 * 1024
     
    print(f"开始在路径 '{root}' 中查找大于 {size_limit_mb} MB 的文件...\n")
    print("-" * 50)
     
    # 查找大文件
    found_files = find_large_files(root, size_limit_bytes)
     
    # 输出结果到控制台
    if found_files:
        print("*" * 50)
        print("对以上结果根据文件大小降序排列:")
        for file, size in found_files.items():
            print(f'{file}: {size / (1024 * 1024):.2f} MB')
         
        # 保存结果到txt文件
        output_filename = f"large_files_report_{__import__('datetime').datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        # 可以选择指定完整路径，比如保存到桌面
        # output_path = os.path.join(os.path.expanduser("~"), "Desktop", output_filename)
        output_path = output_filename  # 保存在当前目录
         
        save_results_to_txt(found_files, output_path, size_limit_mb)
    else:
        print("没有找到大于50MB的文件。\n")
 
 
if __name__ == '__main__':
    main()