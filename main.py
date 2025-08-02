# main.py
#Robert Martinez 1-21-1494 MINI COMPILADOR
from lexer import tokenize
from parser import Parser
from semantico import SemanticAnalyzer
from intermedio import IntermediateGenerator
from codigo_gen import CodeGenerator
import io
import contextlib

def main():
    print("=== Mini-Compilador Java→Python ===\n")
    print("Introduce tu código línea a línea. Escribe 'END' para terminar:\n")
    lines = []
    while True:
        l = input()
        if l.strip().upper() == 'END':
            break
        lines.append(l + '\n')

    source = ''.join(lines)
    try:
        # 1. Léxico
        tokens = tokenize(source)
        # 2. Sintáctico
        ast    = Parser(tokens).parse()
        # 3. Semántico
        sem    = SemanticAnalyzer()
        sem.analyze(ast)
        # 4. Intermedio
        inter  = IntermediateGenerator()
        inter.generate(ast)
        # 5. Generación de código Python
        cg     = CodeGenerator()
        py_code = cg.generate(ast)
        print("=== Código Python generado ===")
        print(py_code)

        # 6. Ejecución del código generado (en python)
        print("\n=== Ejecución del código ===")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            exec(py_code, {})
        salida = buf.getvalue().strip()
        print(salida)

    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
