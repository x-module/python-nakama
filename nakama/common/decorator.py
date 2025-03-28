# -*- coding: utf-8 -*-
def singleton(cls):
    instances = {}  # 保存类标签到实例的映射
    def wrapper(*args, **kwargs):
        if cls not in instances:  # 如果类没有实例化过
            instances[cls] = cls(*args, **kwargs)  # 创建实例并保存
        return instances[cls]  # 返回已存在的实例

    return wrapper
