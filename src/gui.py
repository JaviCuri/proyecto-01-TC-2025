import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tokenizer import tokenize_line
from parser_ll1 import parse_tokens
from main import extract_candidate_lines


class DarkStyle:
    def apply(self, root):
        style = ttk.Style(root)

        # Tema base
        style.theme_use("default")

        # COLORES BASE
        bg = "#0f0f0f"
        bg_darker = "#0a0a0a"
        panel = "#161b22"
        text = "#e6edf3"
        blue = "#58a6ff"
        blue_dark = "#1f6feb"
        orange = "#f78166"
        border = "#30363d"

        # ROOT
        root.configure(bg=bg)

        # General ttk config
        style.configure(
            ".", 
            background=bg,
            foreground=text,
            fieldbackground=panel,
            bordercolor=border,
            focuscolor=blue,
            font=("Segoe UI", 10)
        )

        # Buttons
        style.configure(
            "TButton",
            background=blue_dark,
            foreground="white",
            padding=8,
            relief="flat",
            borderwidth=0,
            focusthickness=3,
            anchor="center",
            font=("Segoe UI", 11, "bold")
        )
        style.map(
            "TButton",
            background=[("active", blue)],
            foreground=[("active", "#ffffff")]
        )

        # Frames
        style.configure("DarkFrame.TFrame", background=bg)
        style.configure("Panel.TFrame", background=panel)

        # Treeview
        style.configure(
            "Treeview",
            background=panel,
            foreground=text,
            fieldbackground=panel,
            rowheight=26,
            bordercolor=border,
            borderwidth=1,
            font=("Consolas", 10)
        )

        style.configure(
            "Treeview.Heading",
            background=bg_darker,
            foreground=blue,
            font=("Segoe UI", 11, "bold")
        )

        style.map(
            "Treeview",
            background=[("selected", blue_dark)],
            foreground=[("selected", "white")]
        )


class TCApp:
    def __init__(self, root):
        DarkStyle().apply(root)

        self.root = root
        self.root.title("Analizador LL(1) — Dark Edition")
        self.root.geometry("1200x800")
        self.root.resizable(False, False)

        self.bg = "#0f0f0f"
        self.panel = "#161b22"
        self.text = "#e6edf3"
        self.blue = "#58a6ff"
        self.orange = "#f78166"

        # HEADER
        header = tk.Frame(root, bg=self.bg)
        header.pack(fill="x", pady=10)

        tk.Label(
            header, text="Analizador Sintáctico LL(1)",
            font=("Segoe UI", 26, "bold"), fg=self.blue, bg=self.bg
        ).pack()

        tk.Label(
            header,
            text="Proyecto 1 — INFO1148 (Procesamiento de expresiones aritméticas en Java)",
            font=("Segoe UI", 12), fg=self.text, bg=self.bg
        ).pack()

        # BOTONES
        btn_frame = ttk.Frame(root, style="DarkFrame.TFrame")
        btn_frame.pack(pady=15)

        self.add_button(btn_frame, "📂 Seleccionar archivo Java", self.load_file, 0)
        self.add_button(btn_frame, "✏️ Analizar expresión manual", self.analyze_manual_expression, 1)
        self.add_button(btn_frame, "🧹 Limpiar pantalla", self.clear_output, 2)

        # OUTPUT PANEL
        self.canvas = tk.Canvas(root, bg=self.bg, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        scrollbar.place(relx=0.98, rely=0.3, relheight=0.69)

        self.output_frame = ttk.Frame(self.canvas, style="Panel.TFrame")
        self.canvas.create_window((0, 0), window=self.output_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.output_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    # -----------------------------
    def add_button(self, parent, text, command, col):
        btn = ttk.Button(parent, text=text, command=command)
        btn.grid(row=0, column=col, padx=15)

    # ==============================================================
    def load_file(self):
        path = filedialog.askopenfilename(filetypes=[("Java files", "*.java")])
        if not path:
            return

        self.write_header(f"📄 Archivo cargado:\n{path}")

        lines = extract_candidate_lines(path)
        if not lines:
            self.write("⚠ No se encontraron expresiones válidas.\n")
            return

        self.write(f"🔍 Se encontraron {len(lines)} expresiones:\n")

        for idx, line in enumerate(lines, 1):
            self.show_expression(idx, line)

    # ==============================================================
    def show_expression(self, idx, code):
        self.write(f"\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n✨ Expresión {idx}: {code}\n")

        tokens = tokenize_line(code)
        self.write(f"🟦 Tokens: {tokens}\n")

        _, valid, steps = parse_tokens(tokens, return_steps=True)

        # TABLA
        table_wrap = ttk.Frame(self.output_frame, style="Panel.TFrame")
        table_wrap.pack(pady=8, fill="x")

        cols = ("Pila", "Entrada", "Producción usada")
        table = ttk.Treeview(table_wrap, columns=cols, show="headings", height=12)
        table.pack(side="left")

        for col in cols:
            table.heading(col, text=col)
            table.column(col, width=320 if col != "Producción usada" else 460)

        scroll = ttk.Scrollbar(table_wrap, orient="vertical", command=table.yview)
        scroll.pack(side="right", fill="y")
        table.configure(yscrollcommand=scroll.set)

        for step in steps:
            table.insert("", "end", values=(step["pila"], step["entrada"], step["prod"]))

        self.write(f"\n🟧 Resultado final: {'✔ Válida' if valid else '❌ Inválida'}\n")

    # ==============================================================
    def analyze_manual_expression(self):
        win = tk.Toplevel(self.root)
        win.title("Ingresar expresión")
        win.geometry("400x180")
        win.configure(bg=self.bg)

        tk.Label(win, text="Ingrese la expresión:", fg=self.text, bg=self.bg, font=("Segoe UI", 11)).pack(pady=10)
        entry = tk.Entry(win, width=40, font=("Segoe UI", 12), bg=self.panel, fg=self.text, insertbackground=self.text)
        entry.pack()

        def run():
            expr = entry.get().strip()
            if expr:
                self.write("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                self.write(f"\n📝 Expresión manual:\n{expr}")
                self.show_expression("Manual", expr)
                win.destroy()

        ttk.Button(win, text="Analizar", command=run).pack(pady=15)

    # ==============================================================
    def clear_output(self):
        for w in self.output_frame.winfo_children():
            w.destroy()

    # ==============================================================
    def write(self, text):
        tk.Label(
            self.output_frame,
            text=text,
            fg=self.text,
            bg=self.panel,
            justify="left",
            anchor="w",
            font=("Segoe UI", 11)
        ).pack(fill="x", padx=15, pady=2)

    def write_header(self, text):
        tk.Label(
            self.output_frame,
            text=text,
            fg=self.orange,
            bg=self.bg,
            font=("Segoe UI", 13, "bold"),
            anchor="w",
            justify="left"
        ).pack(fill="x", padx=15, pady=5)


def run_gui():
    root = tk.Tk()
    app = TCApp(root)
    root.mainloop()


if __name__ == "__main__":
    run_gui()
