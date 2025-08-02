# 5- intermedio

from parser import *

class IntermediateGenerator:
    def __init__(self):
        self.code = []
        self.temp_count = 0

    def new_temp(self):
        t = f"t{self.temp_count}"
        self.temp_count += 1
        return t

    def generate(self, ast):
        print("[Intermediate] Generando código intermedio...")
        self.visit(ast)
        for instr in self.code:
            print(" ", instr)
        print()
        return self.code

    def visit(self, node):
        meth = 'visit_' + node.__class__.__name__
        return getattr(self, meth)(node)

    def visit_Block(self, blk):
        for s in blk.stmts:
            self.visit(s)

    def visit_Declaration(self, node):
        if node.expr:
            val = self.visit(node.expr)
            self.code.append((node.name, '=', val))

    def visit_Assign(self, node):
        val = self.visit(node.expr)
        self.code.append((node.name, '=', val))

    def visit_BinOp(self, node):
        l = self.visit(node.left)
        r = self.visit(node.right)
        t = self.new_temp()
        self.code.append((t, node.op, l, r))
        return t

    def visit_Num(self, node):
        return str(node.value)

    def visit_Var(self, node):
        return node.name

    def visit_Print(self, node):
        val = self.visit(node.expr)
        self.code.append(('print', val))

    def visit_While(self, node):
        # muy simplificado, sin etiquetas reales
        self.visit(node.cond)
        self.visit(node.body)

    def visit_For(self, node):
        self.visit(node.start)
        self.visit(node.cond)
        self.visit(node.body)
