from importlib.resources import files
import shutil
import os
from .PhiCloudLib import logger

def copy_data():
    # 获取包名称和目标工作目录
    package_name = 'phi_cloud_action'
    work_dir = os.getcwd()

    # 获取包内 data 文件夹
    try:
        # 使用 files() 来访问包内的 data 文件夹
        data_dir = files(package_name) / 'data'

        # 遍历 data 文件夹中的所有文件和文件夹
        for item in data_dir.iterdir():
            if item.is_dir():  # 如果是文件夹
                dest_folder = os.path.join(work_dir, item.name)
                # 如果目标文件夹不存在，创建它
                os.makedirs(dest_folder, exist_ok=True)

                # 遍历文件夹中的内容并拷贝
                for sub_item in item.iterdir():
                    dest_file = os.path.join(dest_folder, sub_item.name)
                    if sub_item.is_file():
                        # 拷贝文件到目标目录
                        shutil.copy(sub_item, dest_file)
                        logger.info(f"已将 {sub_item.name} 从 {item.name} 拷贝到当前目录了喵")

        logger.info("所有文件已成功拷贝到当前目录了喵")
        logger.info(f"可以查看 examples 文件夹中的示例代码了喵")
    except Exception as e:
        logger.error(f"发生错误: {e}")

if __name__ == '__main__':
    # 执行拷贝操作
    copy_data()
