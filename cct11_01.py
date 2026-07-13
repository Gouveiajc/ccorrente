"""
Programa de Cadastro de Tipos de Natureza
Tela Inicial 
JC Jul/2026
Ver 1
Banco de Dados cct.db
Tabela cct00
Módulo: cct11_01.py
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import cct00_0      # módulo de banco de dados
import cct11_02
import cct11_03

def abrir_lista(root):

    # Evita abrir várias janelas iguais
    for widget in root.winfo_children():
        if isinstance(widget, tk.Toplevel) and widget.title() == "Consulta de Tipos de Natureza":
            widget.lift()
            return

    # Criar janela
    janela = tk.Toplevel(root)
    janela.title("Consulta de Tipos de Natureza")
    janela.geometry("750x450")
    janela.grab_set()

    # Atalho ESC para fechar
    janela.bind("<Escape>", lambda e: janela.destroy())

    # -----------------------------
    #       BOTÕES SUPERIORES
    # -----------------------------
    frame_botoes = ttk.Frame(janela, padding=10)
    frame_botoes.pack(fill="x")

    # Os callbacks serão adicionados depois da criação do grid
    # (por isso usamos lambda vazio aqui temporariamente)
    btn_incluir = ttk.Button(frame_botoes, text="INCLUIR", width=12)
    btn_incluir.pack(side="left", padx=5)

    btn_alterar = ttk.Button(frame_botoes, text="ALTERAR", width=12)
    btn_alterar.pack(side="left", padx=5)

    ttk.Button(frame_botoes, text="DELETAR", width=12,
               command=lambda: deletar_registro(tree)).pack(side="left", padx=5)

    ttk.Button(frame_botoes, text="RETORNAR", width=12,
               command=janela.destroy).pack(side="right", padx=5)

    # -----------------------------
    #       GRID (TREEVIEW)
    # -----------------------------
    frame_grid = ttk.Frame(janela, padding=10)
    frame_grid.pack(fill="both", expand=True)

    # Label para mensagens
    label_aviso = ttk.Label(frame_grid, text="", foreground="red", font=("Arial", 10, "bold"))
    label_aviso.pack(anchor="w", pady=(0, 5))

    colunas = ("CCT00_01", "CCT00_08", "CCT00_09", "CCT00_07")

    tree = ttk.Treeview(frame_grid, columns=colunas, show="headings", height=15)

    tree.heading("CCT00_01", text="Natureza")
    tree.heading("CCT00_08", text="Descrição")
    tree.heading("CCT00_09", text="Tipo")
    tree.heading("CCT00_07", text="Observação")

    tree.column("CCT00_01", width=80)
    tree.column("CCT00_08", width=250)
    tree.column("CCT00_09", width=100)
    tree.column("CCT00_07", width=150)

    tree.pack(fill="both", expand=True)

    # -----------------------------
    #   FUNÇÃO PARA ATUALIZAR GRID
    # -----------------------------
    def atualizar_grid():
        # Limpa o grid
        for i in tree.get_children():
            tree.delete(i)

        # Recarrega os dados
        conn = cct00_0.conectar()
        registros = cct00_0.listar_registros(conn)
        for reg in registros:
            tree.insert("", tk.END, values=reg)

        conn.close()

    # -----------------------------
    #   CARREGAR DADOS INICIAIS
    # -----------------------------
    atualizar_grid()

    # -----------------------------
    #   CONECTAR CALLBACKS
    # -----------------------------
    btn_incluir.config(
        command=lambda: cct11_02.abrir_janela(janela, atualizar_grid)
    )

    btn_alterar.config(
        command=lambda: cct11_03.alterar_registro(tree, atualizar_grid)
    )

# -----------------------------
#       FUNÇÕES AUXILIARES
# -----------------------------
def deletar_registro(tree):
    item = tree.selection()
    janela = tree.master  # janela do grid

    if not item:
        messagebox.showwarning("Atenção", "Selecione um registro para deletar.", parent=janela)
        return

    valores = tree.item(item, "values")
    codigo = valores[0]
    desc   = valores[1]

    if messagebox.askyesno("Confirmar", f"Excluir o registro: \nCódigo: {codigo} \nDescrição: {desc}?", parent=janela):
        conn = cct00_0.conectar()
        cct00_0.excluir_registro(conn, codigo)
        conn.close()

        # Limpa o grid
        for i in tree.get_children():
            tree.delete(i)

        # Recarrega os dados do banco
        conn = cct00_0.conectar()
        registros = cct00_0.listar_registros(conn)
        for reg in registros:
            if len(reg) == 4:
                tree.insert("", tk.END, values=reg)

        messagebox.showinfo("Sucesso", "Registro excluído com sucesso!", parent=janela)

    janela.lift()
    janela.focus_force()
