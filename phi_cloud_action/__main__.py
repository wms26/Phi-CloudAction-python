from . import PhiCloudLib
import inspect
from . import example

def list_class_methods_with_file(cls):
    """列出类中的所有方法及其文件路径"""
    methods_with_file = []
    
    # 遍历类中的所有方法
    for method_name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
        # 获取方法的源文件路径
        file_path = inspect.getfile(method)
        methods_with_file.append((method_name, file_path))
    
    return methods_with_file

# 获取 example 模块中的所有方法及其文件路径
methods_with_file = list_class_methods_with_file(example)

# 格式化输出每个方法和文件路径，每行一个方法
methods_str = '\n'.join([f"{method_name} (文件路径: {file_path})" for method_name, file_path in methods_with_file])

# 使用 logger 输出方法及其文件路径
PhiCloudLib.logger.info(f"目前的所有的示例方法及文件位置喵:\n{methods_str}")
