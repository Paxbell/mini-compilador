# 4-semantico

from parser import *
from tabla_simbolos import SymbolTable

class SemanticAnalyzer:
    def __init__(self):
        self.symtab = SymbolTable()

    def analyze(self, ast):
        print("[Semantic] Iniciando análisis semántico...")
        self.visit(ast)
        print(f"[Semantic] Tabla de símbolos final: {self.symtab}\n")

    def visit(self, node):
        meth = 'visit_' + node.__class__.__name__
        return getattr(self, meth)(node)

    def visit_Block(self, blk):
        for stmt in blk.stmts:
            self.visit(stmt)

    def visit_Declaration(self, node):
        # declara la variable
        self.symtab.declare(node.name, node.type)
        if node.expr:
            expr_type = self.visit(node.expr)
            if expr_type != node.type:
                raise Exception(f"[Semantic Error] Asignación de '{node.name}' espera {node.type}, got {expr_type}")

    def visit_Assign(self, node):
        var_type = self.symtab.lookup(node.name)
        expr_type = self.visit(node.expr)
        if var_type != expr_type:
            raise Exception(f"[Semantic Error] Asignación a '{node.name}' de tipo {expr_type}, espera {var_type}")

    def visit_Var(self, node):
        return self.symtab.lookup(node.name)

    def visit_Num(self, node):
        return node.type

    def visit_BinOp(self, node):
        lt = self.visit(node.left)
        rt = self.visit(node.right)
        if lt != rt:
            raise Exception(f"[Semantic Error] Operando {lt} vs {rt} incompatibles")
        return lt

    def visit_Print(self, node):
        return self.visit(node.expr)

    def visit_While(self, node):
        cond_type = self.visit(node.cond)
        if cond_type != 'int':
            raise Exception(f"[Semantic Error] Condición de while debe ser int, got {cond_type}")
        self.visit(node.body)

    def visit_For(self, node):
        # variable de bucle se declara implícitamente como int
        if node.var not in self.symtab.table:
            self.symtab.declare(node.var, 'int')
        start_t = self.visit(node.start)
        cond_t  = self.visit(node.cond)
        if start_t!='int' or cond_t!='int':
            raise Exception("[Semantic Error] Bucle for solo admite int")
        self.visit(node.body)
