# 3 tabla de simbolos

class SymbolTable:
    def __init__(self):
        self.table = {}  # name -> tipo ('int'/'float')

    def declare(self, name, typ):
        if name in self.table:
            raise Exception(f"[Semantic Error] Variable '{name}' ya declarada")
        self.table[name] = typ
        print(f"[SymbolTable] Declarada {name}:{typ}")

    def lookup(self, name):
        if name not in self.table:
            raise Exception(f"[Semantic Error] Variable '{name}' no declarada")
        return self.table[name]

    def __str__(self):
        return str(self.table)
