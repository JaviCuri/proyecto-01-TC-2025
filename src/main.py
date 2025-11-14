import sys
from tokenizer import tokenize_line
from parser_ll1 import parse_tokens


def extract_candidate_lines(filepath: str):
    """
    Lee el archivo Java y devuelve lineas que probablemente
    contengan expresiones según nuestra gramática:
    - asignaciones 'id = EXPR;'
    - println 'System.out.println(EXPR);'
    """
    candidates = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if not stripped:
                continue
            if "=" in stripped or "println" in stripped:
                candidates.append(stripped)
    return candidates


def main():
    if len(sys.argv) < 2:
        print("Uso: python src/main.py input/ejemplo.java")
        sys.exit(1)

    java_file = sys.argv[1]
    lines = extract_candidate_lines(java_file)

    if not lines:
        print("No se encontraron expresiones candidatas en el archivo.")
        return

    print(f"📄 Archivo: {java_file}")
    print(f"Se encontraron {len(lines)} líneas candidatas:\n")

    for idx, line in enumerate(lines, start=1):
        print(f"\n==============================")
        print(f"🔹 Línea {idx}: {line}")
        tokens = tokenize_line(line)
        print(f"🔹 Tokens: {tokens}")
        is_valid = parse_tokens(tokens)
        print(f"✅ Válida: {is_valid}")


if __name__ == "__main__":
    main()
