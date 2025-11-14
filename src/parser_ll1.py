from collections import deque

EPSILON = "ε"
ENDMARK = "$"

# Tabla sintáctica LL(1)
PARSING_TABLE = {
    "S": {
        "id":     ["STMT", "S"],
        "System": ["STMT", "S"],
        ENDMARK:  [EPSILON],
    },
    "STMT": {
        "id":     ["ASSIGN", ";"],
        "System": ["PRINT", ";"],
    },
    "ASSIGN": {
        "id": ["id", "=", "EXPR"],
    },
    "PRINT": {
        "System": ["System", ".", "out", ".", "println", "(", "EXPR", ")"],
    },
    "EXPR": {
        "(":   ["TERM", "EXPR'"],
        "id":  ["TERM", "EXPR'"],
        "num": ["TERM", "EXPR'"],
    },
    "EXPR'": {
        "+": ["+", "TERM", "EXPR'"],
        "-": ["-", "TERM", "EXPR'"],
        ")": [EPSILON],
        ";": [EPSILON],
        ENDMARK: [EPSILON],
    },
    "TERM": {
        "(":   ["FACTOR", "TERM'"],
        "id":  ["FACTOR", "TERM'"],
        "num": ["FACTOR", "TERM'"],
    },
    "TERM'": {
        "*": ["*", "FACTOR", "TERM'"],
        "/": ["/", "FACTOR", "TERM'"],
        "%": ["%", "FACTOR", "TERM'"],
        "+": [EPSILON],
        "-": [EPSILON],
        ")": [EPSILON],
        ";": [EPSILON],
        ENDMARK: [EPSILON],
    },
    "FACTOR": {
        "(":   ["(", "EXPR", ")"],
        "id":  ["id"],
        "num": ["num"],
    },
}


def parse_tokens(tokens, return_log=False, return_steps=False):
    """
    Parser LL(1) con tres modos:
      - return_log=True → devuelve string con la traza textual
      - return_steps=True → devuelve lista estructurada paso a paso
      - ambos pueden ser usados a la vez

    Retorno:
      log, resultado, steps
    """

    log = ""
    trace_steps = []  

    def add(msg):
        nonlocal log
        log += msg + "\n"
        if not return_log and not return_steps:
            print(msg)

    input_queue = deque(tokens + [ENDMARK])
    stack = deque([ENDMARK, "S"])

    add(f"📥 Tokens de entrada: {tokens}")
    add("🔍 Iniciando análisis LL(1)...")

    while stack:
        top = stack.pop()
        current = input_queue[0]

        pila_str = " ".join(list(stack) + [top])
        entrada_str = " ".join(list(input_queue))

        prod_str = ""

        # ---------------------------
        # Caso terminal
        # ---------------------------
        if top not in PARSING_TABLE and top != EPSILON:
            if top == current:
                prod_str = f"match '{top}'"
                add(f"✔ Se empareja terminal '{top}'")
                input_queue.popleft()
            else:
                prod_str = f"ERROR: se esperaba {top}"
                add(f"❌ Error sintáctico: se esperaba '{top}' y llegó '{current}'")

                if return_steps:
                    trace_steps.append({
                        "pila": pila_str,
                        "entrada": entrada_str,
                        "prod": prod_str
                    })

                if return_log and return_steps:
                    return log, False, trace_steps
                elif return_steps:
                    return None, False, trace_steps
                elif return_log:
                    return log, False
                else:
                    return False

        # ---------------------------
        # Caso epsilon
        # ---------------------------
        elif top == EPSILON:
            prod_str = "ε"
            add("λ (epsilon), no se consume entrada.")

        # ---------------------------
        # Caso no terminal
        # ---------------------------
        else:
            if current in PARSING_TABLE[top]:
                production = PARSING_TABLE[top][current]
                prod_str = f"{top} → {' '.join(production)}"
                add(f"▶ {prod_str}")

                for symbol in reversed(production):
                    if symbol != EPSILON:
                        stack.append(symbol)
            else:
                prod_str = f"ERROR: M[{top}, {current}] vacío"
                add(f"❌ Error sintáctico: no hay regla para M[{top}, {current}]")

                if return_steps:
                    trace_steps.append({
                        "pila": pila_str,
                        "entrada": entrada_str,
                        "prod": prod_str
                    })

                if return_log and return_steps:
                    return log, False, trace_steps
                elif return_steps:
                    return None, False, trace_steps
                elif return_log:
                    return log, False
                else:
                    return False

        if return_steps:
            trace_steps.append({
                "pila": pila_str,
                "entrada": entrada_str,
                "prod": prod_str
            })

        if top == ENDMARK and current == ENDMARK:
            add("\n🎉 Análisis completado: la cadena es válida según la gramática.")

            if return_steps and return_log:
                return log, True, trace_steps
            elif return_steps:
                return None, True, trace_steps
            elif return_log:
                return log, True
            else:
                return True

    add("❌ No se pudo completar el análisis.")
    if return_steps and return_log:
        return log, False, trace_steps
    elif return_steps:
        return None, False, trace_steps
    elif return_log:
        return log, False
    return False
