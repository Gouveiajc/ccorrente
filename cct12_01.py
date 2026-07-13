"""
Programa de Cadastro de Contas Corrente
Tela Inicial
JC Jul/2026
Ver 1
Banco de Dados cct.db
Tabela cct01
Módulo: cct12_01.py
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import cct00_0      # módulo de banco de dados
import cct12_02

def abrir_lista(root):

    # Evita abrir várias janelas iguais
    for widget in root.winfo_children():
        if isinstance(widget, tk.Toplevel) and widget.title() == "Consulta de Conta Corrente":
            widget.lift()
            return

    # Criar janela
    janela = tk.Toplevel(root)
    janela.title("Consulta de Conta Corrente")
    janela.geometry("750x450")
    janela.grab_set()

    # Atalho ESC para fechar
    janela.bind("<Escape>", lambda e: janela.destroy())

    # -----------------------------
    #       BOTÕES SUPERIORES
    # -----------------------------
    frame_botoes = ttk.Frame(janela, padding=10)
    frame_botoes.pack(fill="x")

    ttk.Button(frame_botoes, text="INCLUIR", width=12,
               command=lambda: cct12_02.abrir_janela_inv01(janela, tree) ).pack(side="left", padx=5)

 #   ttk.Button(frame_botoes, text="ALTERAR", width=12,
 #              command=lambda: cct12_03.alterar_registro(tree)).pack(side="left", padx=5)

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

    colunas = ("CCT01_02", "CCT01_03", "CCT01_11", "CCT01_10", "CCT01_05")

    tree = ttk.Treeview(frame_grid, columns=colunas, show="headings", height=15)

    tree.heading("CCT01_02", text="Código Banco")
    tree.heading("CCT01_03", text="Conta Corrente-Digito")
    tree.heading("CCT01_11", text="Descrição Banco")
    tree.heading("CCT01_10", text="Saldo")
    tree.heading("CCT01_05", text="Data")
  
    tree.column("CCT01_02", width=80)
    tree.column("CCT01_03", width=80)
    tree.column("CCT01_11", width=250)
    tree.column("CCT01_10", width=100)
    tree.column("CCT01_05", width=80)
    
    tree.pack(fill="both", expand=True)

    # -----------------------------
    #       CARREGAR DADOS
    # -----------------------------
    conn = cct00_0.conectar()
    registros = cct00_0.listar_registros_cct01(conn)

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
    conta  = valores[1]
    desc = valores[2]

    if messagebox.askyesno("Confirmar", f"Excluir o registro: \nCódigo: {codigo}\nConta: {conta} \nDescrição: {desc}?", parent=janela):
        conn = cct00_0.conectar()
        cct00_0.excluir_registro_cct01(conn, codigo, conta)
        conn.close()

        # Limpa o grid
        for i in tree.get_children():
            tree.delete(i)

        # Recarrega os dados do banco
        conn = cct00_0.conectar()
        registros = cct00_0.listar_registros_cct01(conn)
        conn.close()
        for reg in registros:
            tree.insert("", tk.END, values=reg)

        messagebox.showinfo("Sucesso", "Registro excluído com sucesso!", parent=janela)

    # Devolve o foco para a janela do grid
    janela.lift()
    janela.focus_force()