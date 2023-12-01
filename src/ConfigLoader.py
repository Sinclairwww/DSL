from yaml import load, CLoader
from schema import Schema, Optional


class ConfigLoader:
    def __init__(self, path=""):
        if path:
            self.load(path)
        pass

    # 获取配置文件解析出的对象
    def getConfig(self):
        return self._config

    # 加载配置文件，进行完整性检查，并处理缺省值
    def load(self, path="./config.yaml", encoding="utf8"):
        with open(path, "r", encoding=encoding) as f:
            config = load(f, CLoader)
        if self._validate(config):
            self._config = config
        else:
            self._config = {}
        self._updateDefault()

    def getRuntimeConfig(self):
        return self._config.get("runtime")

    # 获取脚本解析部分的配置
    def getJobConfig(self):
        return self._config.get("job")

    # 获取RunPy模块的配置
    def getScriptsConfig(self):
        return self._config.get("scripts")

    def _updateDefault(self):
        with open("./src/data/default_config.yaml", "r", encoding="utf-8") as f:
            default = load(f, CLoader)
        default.update(self._config)
        self._config = default

    # 使用schema库的Schema类定义了一个配置的模式。这个模式定义了配置中的各个键的名称、类型和默认值
    def _validate(self, config):
        schema = Schema(
            {
                Optional("pwd", default="."): str,
                "runtime": {
                    "user-db": str,
                },
                "job": {
                    "path": str,
                    "halt-onerror": bool,
                },
                "scripts": {"halt-onerror": bool, "dirs": [str]},
            }
        )
        return schema.validate(config)
