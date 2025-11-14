import re

KEYWORDS = {"System", "out", "println"}
SYMBOLS = {"=", "+", "-", "*", "/", "%", "(", ")", ";", ".", ","}

TOKEN_REGEX = re.compile(r"""
    ([A-Za-z_][A-Za-z0-9_]*)   |  
    (\d+)                      |  
    (==|!=|<=|>=|&&|\|\|)      |   
    ([=+\-*/%();.,])               
""", re.VERBOSE)


def tokenize_line(line: str):
    """
    Recibe una línea de código Java (simplificada)
    y retorna una lista de tokens lógicos para el parser LL(1).
    """
    tokens = []

    for match in TOKEN_REGEX.finditer(line):
        ident, num, op_long, sym = match.groups()

        if ident is not None:
            if ident in KEYWORDS:
                tokens.append(ident)  # System, out, println
            else:
                tokens.append("id")
        elif num is not None:
            tokens.append("num")
        elif op_long is not None:
            tokens.append(op_long)
        elif sym is not None:
            tokens.append(sym)

    return tokens
