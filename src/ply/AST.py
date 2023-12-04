# 抽象语法树节点类


class ASTNode:
    def __init__(self, type, *childs):
        self.type = type
        self.childs = list(childs)

    # 递归打印节点与子节点
    def print(self, depth=0):
        print("\t" * depth, end="")
        print(self.type)
        for child in self.childs:
            # 如果子节点不是ASTNode，抛出异常
            if not isinstance(child, ASTNode):
                raise RuntimeError(child)
            child.print(depth=depth + 1)
