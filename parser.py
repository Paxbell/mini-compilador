# 2 parser

from lexer import tokenize, Token
from collections import namedtuple

# Nodos AST
Num         = namedtuple('Num',        ['value', 'type'])  #int o float
Var         = namedtuple('Var',        ['name'])
BinOp       = namedtuple('BinOp',      ['left', 'op', 'right'])
Declaration = namedtuple('Declaration',['name', 'expr', 'type'])
Assign      = namedtuple('Assign',     ['name', 'expr'])
Print       = namedtuple('Print',      ['expr'])
While       = namedtuple('While',      ['cond', 'body'])
For         = namedtuple('For',        ['var', 'start', 'cond', 'body'])
Block       = namedtuple('Block',      ['stmts'])

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else Token('EOF','')

    def eat(self, typ=None, val=None):
        tok = self.peek()
        if typ and tok.type != typ:
            raise SyntaxError(f"[Parser Error] Esperaba token {typ}, encontró {tok}")
        if val and tok.value != val:
            raise SyntaxError(f"[Parser Error] Esperaba '{val}', encontró '{tok.value}'")
        self.pos += 1
        return tok

    def parse(self):
        stmts = []
        while self.peek().type != 'EOF':
            stmts.append(self.statement())
        ast = Block(stmts)
        print(f"[Parser] AST: {ast}\n")
        return ast

    def statement(self):
        tok = self.peek()
        # 1) Declaración: int x; o int x = expr;
        if tok.type=='ID' and tok.value in ('int','float'):
            return self.declaration()
        # 2) System.out.print/println
        if tok.type=='ID' and tok.value=='System':
            return self.sysout_stmt()
        # 3) print(expr);
        if tok.type=='ID' and tok.value=='print':
            return self.print_stmt()
        # 4) Asignación: x = expr;
        if tok.type=='ID' and self.tokens[self.pos+1].type=='OP' and self.tokens[self.pos+1].value=='=':
            return self.assign()
        # 5) while(cond){...}
        if tok.type=='ID' and tok.value=='while':
            return self.while_stmt()
        # 6) for(...)
        if tok.type=='ID' and tok.value=='for':
            return self.for_stmt()
        raise SyntaxError(f"[Parser Error] Sentencia no reconocida: {tok}")

    def declaration(self):
        tipo = self.eat('ID').value       # int o float
        name = self.eat('ID').value
        expr = None
        if self.peek().type=='OP' and self.peek().value=='=':
            self.eat('OP','=')
            expr = self.expr()
        self.eat('PUNTO_COMA')
        return Declaration(name, expr, tipo)

    def assign(self):
        name = self.eat('ID').value
        self.eat('OP','=')
        expr = self.expr()
        self.eat('PUNTO_COMA')
        return Assign(name, expr)

    def sysout_stmt(self):
        self.eat('ID','System')
        self.eat('DOT')
        self.eat('ID','out')
        self.eat('DOT')
        method = self.eat('ID').value
        if method not in ('print','println'):
            raise SyntaxError(f"[Parser Error] Método desconocido: {method}")
        self.eat('IPAREN')
        expr = self.expr()
        self.eat('DPAREN')
        self.eat('PUNTO_COMA')
        return Print(expr)

    def print_stmt(self):
        self.eat('ID','print')
        self.eat('IPAREN')
        expr = self.expr()
        self.eat('DPAREN')
        self.eat('PUNTO_COMA')
        return Print(expr)

    def while_stmt(self):
        self.eat('ID','while')
        self.eat('IPAREN')
        cond = self.expr()
        self.eat('DPAREN')
        body = self.block()
        return While(cond, body)

    def for_stmt(self):
        self.eat('ID','for')
        self.eat('IPAREN')
        # for(int i=0; i<10; i++)
        self.eat('ID')  # tipo ignorado en bucle
        var = self.eat('ID').value
        self.eat('OP','=')
        start = self.expr()
        self.eat('PUNTO_COMA')
        cond = self.expr()
        self.eat('PUNTO_COMA')
        self.eat('ID', var)
        self.eat('OP','+')
        self.eat('OP','+')
        self.eat('DPAREN')
        body = self.block()
        return For(var, start, cond, body)

    def block(self):
        self.eat('ILlave')
        stmts = []
        while self.peek().type!='DLlave':
            stmts.append(self.statement())
        self.eat('DLlave')
        return Block(stmts)

    def expr(self):
        node = self.term()
        while self.peek().type=='OP' and self.peek().value in ('+','-','<'):
            op = self.eat('OP').value
            right = self.term()
            node = BinOp(node, op, right)
        return node

    def term(self):
        node = self.factor()
        while self.peek().type=='OP' and self.peek().value in ('*','/'):
            op = self.eat('OP').value
            right = self.factor()
            node = BinOp(node, op, right)
        return node

    def factor(self):
        tok = self.peek()
        if tok.type=='NUMERO':
            self.eat('NUMERO')
            return Num(int(tok.value), 'int')
        if tok.type=='FLOAT':
            self.eat('FLOAT')
            return Num(float(tok.value), 'float')
        if tok.type=='ID':
            return Var(self.eat('ID').value)
        if tok.type=='IPAREN':
            self.eat('IPAREN')
            node = self.expr()
            self.eat('DPAREN')
            return node
        raise SyntaxError(f"[Parser Error] Factor no reconocido: {tok}")
