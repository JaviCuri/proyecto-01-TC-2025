# Manual de Usuario – Analizador Sintáctico LL(1)
Proyecto 1 — INFO1148: Teoría de la Computación  
Autor: **Javier Curipan**  
Año: **2025**

---

## 1. Introducción
Este software implementa un analizador sintáctico LL(1) para un subconjunto del lenguaje Java. Permite:

- Analizar expresiones aritméticas y asignaciones simples.
- Procesar llamadas a `System.out.println()`.
- Mostrar tokens generados.
- Visualizar la traza completa del análisis LL(1).
- Mostrar tabla LL(1) con pila, entrada y producción aplicada.
- Usar una interfaz gráfica moderna en modo oscuro.

---

## 2. Requisitos del Sistema

### Software requerido
- Python **3.9+**
- Tkinter (incluido en Windows/macOS; en Linux instalar manualmente)

### Sistemas soportados
- Windows 10/11
- Linux (Ubuntu, Arch, etc.)
- macOS

---

## 3. Estructura del Proyecto
```
proyecto-01-TC-2025/
│── input/
│     └── ejemplo.java
│
│── outputs/
│     ├── first.json
│     ├── tabla_sintactica.csv
│
│── src/
│     ├── gui.py
│     ├── parser_ll1.py
│     ├── tokenizer.py
│     ├── main.py
│
│── informe/
│     └── proyecto1.pdf
```

---

## 4. Cómo ejecutar el programa
Desde la raíz del proyecto, ejecutar:

```bash
python src/gui.py
```

---

## 5. Uso de la Interfaz Gráfica

### Botones principales

#### 📂 Seleccionar archivo Java
Permite abrir un archivo `.java`; el sistema analiza automáticamente:

- asignaciones
- expresiones aritméticas
- llamadas `println`

#### ✏️ Analizar expresión manual
Permite ingresar una expresión como:

```
a = 5 + 3 * 2;
System.out.println(a);
```

#### 🧹 Limpiar pantalla
Elimina toda la salida previa.

---

## 6. Análisis de un archivo

El programa:

1. Detecta líneas candidatas.
2. Tokeniza cada expresión.
3. Genera una **tabla LL(1) paso a paso** con:
   - **Pila**
   - **Entrada**
   - **Producción aplicada**
4. Indica si la expresión es válida para la gramática definida.

---

## 7. Análisis Manual

Permite ingresar cualquier expresión soportada, mostrando:

- Tokens
- Tabla LL(1)
- Resultado final

---

## 8. Posibles errores y soluciones

| Mensaje | Explicación | Solución |
|--------|-------------|----------|
| *Error sintáctico: se esperaba X* | La expresión no cumple la gramática | Revisar formato y operadores |
| *No se encontraron expresiones válidas* | El archivo no contiene líneas analizables | Usar otro archivo |
| *La GUI no inicia* | Tkinter no está instalado | Instalar Tkinter |

---

## 9. Información del Autor

- **Estudiante:** Javier Curipan  
- **Curso:** INFO1148 – Teoría de la Computación  
- **Semestre:** II – 2025  
- **Profesor:** Marcos Lévano

