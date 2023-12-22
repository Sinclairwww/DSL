from . import ConfigLoader
import os
import importlib.util
import inspect
import logging

logger = logging.getLogger("RunPy")


def getInstance():
    global runpy
    return runpy


class RunPy:
    def __init__(self):
        self._configLoader = None
        self._fileList = []
        self._nameFuncMap = {}
        pass

    # RunPy使用单例模式，所有模块间共享一个RunPy实例，通过此调用获取
    @classmethod
    def getInstance(cls):
        return runpy

    # 初始化全局RunPy实例
    def init(self, configLoader):
        if self._configLoader:
            return
        self._configLoader = configLoader

        dirs = self._getConfig().get("dirs")  # 获取脚本目录列表
        for dir in dirs:  # 遍历目录列表，获取所有脚本文件
            self._getFiles(dir)

        # 将所有脚本文件导入
        for file in self._fileList:
            spec = importlib.util.spec_from_file_location("script", file)  # 从文件加载模块
            foo = importlib.util.module_from_spec(spec)  # 创建一个模块对象
            spec.loader.exec_module(foo)  # 执行加载模块

    # 为全局RunPy实例注册脚本函数的装饰器
    def register(self, name):
        def wrapper1(func):
            if name in self._nameFuncMap:
                logger.warning(
                    f"Reregistering Script {name}, the old will be overwritten."
                )
            self._nameFuncMap[name] = func

            def wrapper2():
                ret = func()
                return ret

            return wrapper2

        return wrapper1

    def callFunc(self, funcName, *args):
        """
        调用名为funcName的已注册的脚本
        如果调用前未注册该脚本，则会抛出RuntimeError
        :param funcName str: 要调用的脚本名称
        """
        func = self._nameFuncMap.get(funcName, None)

        ret = func(*args)
        return ret

    def _getConfig(self):
        return self._configLoader.getScriptsConfig()

    def _getFiles(self, path):
        # 遍历指定目录下的所有文件，将所有以.py结尾的文件加入到文件列表中
        for dirpath, _, filenames in os.walk(path):
            for name in filenames:
                if name[-3:] != ".py":
                    continue
                self._fileList.append(os.path.join(dirpath, name))


runpy = RunPy()
