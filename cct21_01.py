"""
Tela de Consulta de Movimentação
Tabela CCT02
Módulo: inv21_01.py
Jul/2026
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import cct00_0      # módulo de banco de dados
import cct21_02


def abrir_lista(root):

    # Evita abrir várias janelas iguais
    for widget in root.winfo_children():
        if isinstance(widget, tk.Toplevel) and widget.title() == "Cadastro Movimento":
            widget.lift()
            return

    # Criar janela
    janela = tk.Toplevel(root)
    janela.title("Cadastro Movimento")
    janela.geometry("1600x450")
    janela.grab_set()

    # Atalho ESC para fechar
    janela.bind("<Escape>", lambda e: janela.destroy())

    # -----------------------------
    #       BOTÕES SUPERIORES
    # -----------------------------
    frame_botoes = ttk.Frame(janela, padding=10)
    frame_botoes.pack(fill="x")

    ttk.Button(frame_botoes, text="INCLUIR", width=12,
               command=lambda: cct21_02.abrir_janela_cct02(janela, tree) ).pack(side="left", padx=5)

    ttk.Button(frame_botoes, text="DELETAR", width=12,
               command=lambda: cct21_02.abrir_janela_cct02(janela, tree) ).pack(side="left", padx=5)
    
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

    colunas = ("CCT02_00", "CCT02_02", "CCT02_03", "CCT02_11", "CCT02_01", "CCT02_08", "CCT02_04", "CCT02_05", "CCT02_07")

    tree = ttk.Treeview(frame_grid, columns=colunas, show="headings", height=15)

    tree.heading("CCT02_00", text="Id")
    tree.heading("CCT02_02", text="Banco")
    tree.heading("CCT02_03", text="Conta Corrente")
    tree.heading("CCT02_11", text="Descrição Banco")
    tree.heading("CCT02_01", text="Natureza")
    tree.heading("CCT02_08", text="Descrição Natureza")
    tree.heading("CCT02_04", text="Valor R$")
    tree.heading("CCT02_05", text="Data")
    tree.heading("CCT02_07", text="Observação")
    
  
    tree.column("CCT02_00", width=60)
    tree.column("CCT02_02", width=80)
    tree.column("CCT02_03", width=100)
    tree.column("CCT02_11", width=250)
    tree.column("CCT02_01", width=80)
    tree.column("CCT02_08", width=200)
    tree.column("CCT02_04", width=150)
    tree.column("CCT02_05", width=80)
    tree.column("CCT02_07", width=250)
        
    tree.pack(fill="both", expand=True)

    # -----------------------------
    #       CARREGAR DADOS
    # -----------------------------
    conn = cct00_0.conectar()
    registros = cct00_0.listar_registros_cct02(conn)

    for reg in registros:
        tree.insert("", tk.END, values=reg)

    conn.close()

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
        cct00_0.excluir_registro_cct02(conn, codigo)
        conn.close()

        # Limpa o grid
        for i in tree.get_children():
            tree.delete(i)

        # Recarrega os dados do banco
        conn = cct00_0.conectar()
        registros = cct00_0.listar_registros_cct02(conn)
        conn.close()
        for reg in registros:
            tree.insert("", tk.END, values=reg)

        messagebox.showinfo("Sucesso", "Registro excluído com sucesso!", parent=janela)

    # Devolve o foco para a janela do grid
    janela.lift()
    janela.focus_force()


