# 抽象语法树节点类
class ASTNode:
    def __init__(self, type, *childs):
        self.type = type
        self.childs = list(childs)
