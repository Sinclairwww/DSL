from logging import getLogger
from termcolor import cprint
from inputimeout import inputimeout, TimeoutOccurred
import re

from . import ConfigLoader

logger = getLogger("Runtime")


class Runtime:
    KEYWORDS = [
        "是",
        "否",
        "话费",
        "投诉",
        "客服",
        "充值",
    ]

    def __init__(self, number, config: ConfigLoader, enable_timeout=True):
        self._conf = config
        self._enable_timeout = enable_timeout
        self._variables = {
            "_input": "",
            "_input_keyword": "",
            "_number": number,
            "_ret": "",
        }
        pass

    # 实现脚本中的speak命令
    def speak(self, str):
        cprint(f"客服: {str}", "yellow")

    # 等待用户输入, 如果时间超过timeStr，则超时
    def wait(self, timeStr):
        self.speak(f"我将等待 {timeStr} 秒")
        if self._enable_timeout:
            try:
                str = inputimeout(prompt="Me: ", timeout=int(timeStr))
            except TimeoutOccurred:
                str = "timeout"
                logger.info("输入超时.")
        else:
            str = input()
        self.assign("_input", str)
        self._extractKeywords(str)
        self._extractNumbers(str)

    def hangup(self):
        """
        挂断连接，终止脚本

        """
        logger.info(f"用户{self._variables.get('_number')}挂断电话")

    def assign(self, var, val):
        """
        为变量赋值

        :param var str: 变量名
        :param val Any: 要赋的值（会被转换为字符串）
        """
        self._variables[var] = str(val)
        pass

    def beep(self):
        """
        实现发送滴声的方法（为电话客服设计）

        """
        print("滴滴滴...")
        pass

    def getvar(self, varname):
        """
         获取变量的值

        :param varname str: 变量名
        """
        if varname not in self._variables:
            self._variables[varname] = ""
        return self._variables[varname]

    def _extractKeywords(self, str):
        # 从用户输入中提取关键词
        for key in self.KEYWORDS:
            if key in str:
                self._variables["_input_keyword"] = key
                break

    def _extractNumbers(self, str):
        # 从用户输入中提取数字
        match = re.findall(r"\d+", str)
        if match:
            self.assign("_input_number", match[0])

    def _getConfig(self):
        return self._conf.getRuntimeConfig()
