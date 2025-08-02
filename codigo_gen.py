# 6- generador de código de alto nivel legible

from parser import *

class CodeGenerator:
    def __init__(self):
        self.lines = []
        self.indent = 0

    def emit(self, txt):
        self.lines.append('    '*self.indent + txt)

    def generate(self, ast):
        self.visit(ast)
        return '\n'.join(self.lines)

    def visit(self, node):
        meth = 'visit_' + node.__class__.__name__
        return getattr(self, meth)(node)

    def visit_Block(self, blk):
        for s in blk.stmts:
            self.visit(s)

    def visit_Declaration(self, node):
        if node.expr:
            expr = self.visit(node.expr)
            self.emit(f"{node.name} = {expr}")
        else:
            self.emit(f"{node.name} = None")

    def visit_Assign(self, node):
        expr = self.visit(node.expr)
        self.emit(f"{node.name} = {expr}")

    def visit_BinOp(self, node):
        l = self.visit(node.left)
        r = self.visit(node.right)
        return f"({l} {node.op} {r})"

    def visit_Num(self, node):
        return str(node.value)

    def visit_Var(self, node):
        return node.name

    def visit_Print(self, node):
        expr = self.visit(node.expr)
        self.emit(f"print({expr})")

    def visit_While(self, node):
        cond = self.visit(node.cond)
        self.emit(f"while {cond}:")
        self.indent += 1
        self.visit(node.body)
        self.indent -= 1

    def visit_For(self, node):
        start = self.visit(node.start)
        cond = node.cond
        if isinstance(cond, BinOp) and cond.op == '<':
            end = self.visit(cond.right)
        else:
            end = self.visit(cond)
        v = node.var
        self.emit(f"for {v} in range({start}, {end}):")
        self.indent += 1
        self.visit(node.body)
        self.indent -= 1
