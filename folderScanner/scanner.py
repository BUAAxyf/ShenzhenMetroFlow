import os


def scan_folder(file_folder: str) -> list[str]:
    """
    读取file_folder目录下的所有文件名, 返回所有文件名构成的列表
    """
    try:
        # 获取文件夹中的所有文件名
        file_names = os.listdir(file_folder)
        # 过滤出文件名，排除目录
        files = [f for f in file_names if os.path.isfile(os.path.join(file_folder, f))]
        return files
    except FileNotFoundError:
        print(f"Error: The directory '{file_folder}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")


def all_pics(file_dir):
    """
    # 获取文件夹下所有png/jpg路径
    """
    pic_list = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if file.endswith('.png') or file.endswith('.jpg'):  # 检验文件拓展名
                file_path = os.path.join(root, file)
                pic_list.append(file_path)
    return pic_list


def all_files(file_dir, end =""):
    """
    获取文件夹下所有特定类型文件的路径
    """
    file_list=[]
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if file.endswith(end): # 检验文件拓展名
                file_path = os.path.join(root, file)
                file_list.append(file_path)
    return file_list


def rename_to_en(file_path):
    """
    重命名文件夹下所有文件名为英文
    """
    pass


