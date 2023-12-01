from ply.lex import lex
from logging import getLogger
from .. import ConfigLoader

logger = getLogger("Interpreter")


class Lexer:
    # 保留关键字
    reserved = {
        "switch": "SWITCH",
        "case": "CASE",
        "default": "DEFAULT",
        "endswitch": "ENDSWITCH",
        "step": "STEP",
        "endstep": "ENDSTEP",
        "call": "CALL",
        "callpy": "CALLPY",
        "wait": "WAIT",
        "beep": "BEEP",
        "speak": "SPEAK",
        "hangup": "HANGUP",
    }

    tokens = [
        "NEWLINE",
        "VAR",
        "ID",
        "STR",
    ] + list(reserved.values())

    # 直接返回的词法符号
    literals = ["+", "="]
    # 忽略用#开头的注释
    t_ignore_COMMENT = r"\#.*"
    # 忽略空白符和制表符
    t_ignore = " \t"

    def __init__(self, configLoader):
        self._lexer = lex(module=self)
        self._f = None
        self._configLoader = configLoader

    def getLexer(self):
        return self._lexer

    def load(self, path):
        """
        载入脚本文件
        """
        self._f = None
        with open(path, "r", encoding="utf8") as f:
            self._f = f.read()
        if not self._f:  # 读取失败
            logger.error(f"Failed to load file {path}")
            return
        self._lexer.input(self._f)  # 载入到词法分析器
        self._lexer.lineno = 1

    # 载入一段字符串
    def load_str(self, str):
        self._f = str
        self._lexer.input(str)
        self._lexer.lineno = 1

    # 获取下一个词法符号
    def token(self):
        if not self._f:
            raise RuntimeError("Load file before get token")
        return self._lexer.token()

    def t_NEWLINE(self, t):
        r"\n+"
        t.lexer.lineno += len(t.value)
        return t

    # 获取标识符
    def t_ID(self, t):
        r"[a-zA-Z_][a-zA-Z_0-9]*"
        t.type = self.reserved.get(t.value, "ID")  # 查找与t.value相同的保留字,如果没有则返回ID
        return t

    def t_VAR(self, t):
        r"\$[a-zA-Z_0-9]*"
        t.value = t.value[1:]  # 去掉$
        return t

    def t_STR(self, t):
        r"""("((\\\")|[^\n\"])*")|('((\\\')|[^\n\'])*')"""
        t.value = t.value[1:-1]  # 去掉引号
        return t

    def t_error(self, t):
        msg = f"line {t.lexer.lineno}: Unexpected symbol {t.value}"
        if self._configLoader.getJobConfig().get("halt-onerror"):
            raise RuntimeError(msg)
        logger.error(msg)
        t.lexer.skip(1)


if __name__ == "__main__":
    c = ConfigLoader("../data/default_config.yaml")
    l = Lexer(c)
    l.load_str("""step name endstep""")
    token = l.token()
    while token:
        print(token)
        token = l.token()
