import os   
def create_file(self,filename):
    """
    创建日志文件夹和日志文件
    :param filename:
    :return:
    """
    path = filename[0:filename.rfind("/")]
    if not os.path.isdir(path):  # 无文件夹时创建
        os.makedirs(path)
    if not os.path.isfile(filename):  # 无文件时创建
        fd = open(filename, mode="w", encoding="utf-8")
        fd.close()
    else:
        pass

def Save_file(content):
    path="C:\\temp_data\\"
    filename = path+"result.txt"
    if not os.path.isdir(path):  # 无文件夹时创建
        os.makedirs(path)
    if not os.path.isfile(filename):  # 无文件时创建
        fd = open(filename, mode="w", encoding="utf-8")
        fd.write(content)
        fd.close()
    else:
        pass