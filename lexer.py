# 1- lexer

import re
from collections import namedtuple

Token = namedtuple('Token', ['type', 'value'])

TOKEN_SPEC = [
    ('FLOAT',    r'\d+\.\d+'),          # números con punto decimal
    ('NUMERO',   r'\d+'),               # números enteros
    ('ID',       r'[A-Za-z_]\w*'),      # identificadores y palabras clave
    ('OP',       r'[+\-*/=<>]'),        # operadores + - / * = < >
    ('DOT',      r'\.'),                # punto para System.out .
    ('IPAREN',   r'\('),                # Parentesis izquierdo (
    ('DPAREN',   r'\)'),                # Parentesis derecho )               
    ('ILlave',   r'\{'),                # Llave izquierda { 
    ('DLlave',   r'\}'),                # Llave derecha }
    ('PUNTO_COMA',  r';'),              # punto y coma ;
    ('WS',       r'\s+'),               # espacio en blanco
    ('UNKNOWN',  r'.'),                 # Si todo lo anterior no se cumple, termine aqui.
]

master_pat = re.compile('|'.join(f'(?P<{n}>{p})' for n,p in TOKEN_SPEC))

def tokenize(code):
    print("[Lexer] Iniciando tokenización...")
    tokens = []
    for mo in master_pat.finditer(code):
        kind = mo.lastgroup
        val = mo.group()
        if kind == 'WS':
            continue
        if kind == 'UNKNOWN': #Si hay un unkown marcara error
            raise SyntaxError(f"[Lexer Error] Caracter inesperado: '{val}'")
        tokens.append(Token(kind, val))
    print(f"[Lexer] Tokens: {tokens}\n")
    return tokens

if __name__ == "__main__":
    sample = "int x = 1; float y = 2.5; System.out.println(x+y);"
    tokenize(sample)
