"""
Tela de Inclusão de Movimentação
Tabela CCT02
Módulo: cct21_01.py
Jul/2026
"""
import tkinter as tk
from tkinter import ttk, messagebox
import cct00_0   # conexão


def abrir_janela_cct02(root, tree):

    janela = tk.Toplevel(root)
    janela.title("Inclusão de Movimento Conta Corrente")
    janela.geometry("600x450")
    janela.grab_set()
    janela.bind("<Escape>", lambda e: janela.destroy())

    frame = ttk.Frame(janela, padding=10)
    frame.pack(fill="both", expand=True)

    campos = {}

    # ============================
    # BANCO (CCT01)
    # ============================
    ttk.Label(frame, text="Banco:").grid(row=0, column=0, sticky="w", pady=5)

    conn = cct00_0.conectar()
    bancos = cct00_0.listar_registros_cct01(conn)
    conn.close()

    lista_bancos = [f"{b[0]} - {b[1]}" for b in bancos]

    combo_banco = ttk.Combobox(frame, values=lista_bancos, state="readonly", width=30)
    combo_banco.grid(row=0, column=1, sticky="w", pady=5)
    campos["CCT02_02"] = combo_banco

    # CAMPOS AUTOMÁTICOS DO BANCO
    campos["CCT02_03"] = ttk.Entry(frame, width=30, state="readonly")  # descrição Banco
    campos["CCT02_11"] = ttk.Entry(frame, width=30, state="readonly")  # Conta Corrente-Digito

    ttk.Label(frame, text="Descrição Banco:").grid(row=2, column=0, sticky="w", pady=5)
    campos["CCT02_03"].grid(row=2, column=1, sticky="w", pady=5)

    ttk.Label(frame, text="Conta Corrente:").grid(row=1, column=0, sticky="w", pady=5)
    campos["CCT02_11"].grid(row=1, column=1, sticky="w", pady=5)

    def atualizar_banco(event=None):
        sel = combo_banco.get()
        if not sel:
            return

        codigo = sel.split(" - ")[0]
        conn = cct00_0.conectar()
        dado = cct00_0.listar_registros_reduzido_cct01(conn,codigo)
        conn.close()

        if dado:
            conta, descricao = dado
            campos["CCT02_03"].config(state="normal")
            campos["CCT02_11"].config(state="normal")

            campos["CCT02_03"].delete(0, tk.END)
            campos["CCT02_11"].delete(0, tk.END)

            campos["CCT02_03"].insert(0, conta)
            campos["CCT02_11"].insert(0, descricao)

            campos["CCT02_03"].config(state="readonly")
            campos["CCT02_11"].config(state="readonly")

    combo_banco.bind("<<ComboboxSelected>>", atualizar_banco)

    # ============================
    # NATUREZA (CCT00)
    # ============================
    ttk.Label(frame, text="Natureza:").grid(row=3, column=0, sticky="w", pady=5)

    conn = cct00_0.conectar()
    naturezas = cct00_0.listar_registros_reduzido_cct00(conn)
    conn.close()

    lista_nat = [f"{n[0]} - {n[1]}" for n in naturezas]

    combo_nat = ttk.Combobox(frame, values=lista_nat, state="readonly", width=30)
    combo_nat.grid(row=3, column=1, sticky="w", pady=5)
    campos["CCT02_01"] = combo_nat

    campos["CCT02_08"] = ttk.Entry(frame, width=30, state="readonly")

    ttk.Label(frame, text="Descrição Natureza:").grid(row=4, column=0, sticky="w", pady=5)
    campos["CCT02_08"].grid(row=4, column=1, sticky="w", pady=5)

    def atualizar_nat(event=None):
        sel = combo_nat.get()
        if not sel:
            return

        codigo = sel.split(" - ")[0]

        conn = cct00_0.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT CCT00_08 FROM CCT00 WHERE CCT00_01=?", (codigo,))
        dado = cursor.fetchone()
        conn.close()

        if dado:
            descricao = dado[0]
            campos["CCT02_08"].config(state="normal")
            campos["CCT02_08"].delete(0, tk.END)
            campos["CCT02_08"].insert(0, descricao)
            campos["CCT02_08"].config(state="readonly")

    combo_nat.bind("<<ComboboxSelected>>", atualizar_nat)

    # ============================
    # VALOR / DATA / OBS
    # ============================
    ttk.Label(frame, text="Valor:").grid(row=5, column=0, sticky="w", pady=5)
    campos["CCT02_04"] = ttk.Entry(frame, width=30)
    campos["CCT02_04"].grid(row=5, column=1, sticky="w", pady=5)

    ttk.Label(frame, text="Data (DD/MM/AAAA):").grid(row=6, column=0, sticky="w", pady=5)
    campos["CCT02_05"] = ttk.Entry(frame, width=30)
    campos["CCT02_05"].grid(row=6, column=1, sticky="w", pady=5)

    ttk.Label(frame, text="Observação:").grid(row=7, column=0, sticky="w", pady=5)
    campos["CCT02_07"] = ttk.Entry(frame, width=40)
    campos["CCT02_07"].grid(row=7, column=1, sticky="w", pady=5)

    # ============================
    # SALVAR
    # ============================
    def gravar():

        registro = {}

        # BANCO
        banco_sel = campos["CCT02_02"].get()
        if banco_sel:
            registro["CCT02_02"] = banco_sel.split(" - ")[0]
        else:
            messagebox.showwarning("Atenção", "Selecione o banco.")
            return

        registro["CCT02_03"] = campos["CCT02_03"].get()
        registro["CCT02_11"] = campos["CCT02_11"].get()

        # NATUREZA
        nat_sel = campos["CCT02_01"].get()
        if nat_sel:
            registro["CCT02_01"] = nat_sel.split(" - ")[0]
        else:
            messagebox.showwarning("Atenção", "Selecione a natureza.")
            return

        registro["CCT02_08"] = campos["CCT02_08"].get()

        # VALOR
        valor = campos["CCT02_04"].get().replace(".", "").replace(",", ".")
        try:
            float(valor)
        except:
            messagebox.showwarning("Atenção", "Valor inválido.")
            return
        registro["CCT02_04"] = valor

        # DATA
        data = campos["CCT02_05"].get()
        try:
            dia, mes, ano = data.split("/")
            registro["CCT02_05"] = f"{ano}{mes}{dia}"
        except:
            messagebox.showwarning("Atenção", "Data inválida.")
            return

        registro["CCT02_07"] = campos["CCT02_07"].get()

        # GRAVAR NO BANCO
        conn = cct00_0.conectar()
        cct00_0.inserir_registro_cct02(conn, registro)
        conn.close()

        messagebox.showinfo("Sucesso", "Registro incluído com sucesso!")
        limpar_campos()

        def limpar_campos():
            # limpa combo banco
            campos["CCT02_02"].set("")

            # limpa conta corrente e descrição banco
            campos["CCT02_03"].config(state="normal")
            campos["CCT02_03"].delete(0, tk.END)
            campos["CCT02_03"].config(state="readonly")

            campos["CCT02_11"].config(state="normal")
            campos["CCT02_11"].delete(0, tk.END)
            campos["CCT02_11"].config(state="readonly")

            # limpa combo natureza
            campos["CCT02_01"].set("")

            # limpa descrição natureza
            campos["CCT02_08"].config(state="normal")
            campos["CCT02_08"].delete(0, tk.END)
            campos["CCT02_08"].config(state="readonly")

            # limpa valor, data e observação
            campos["CCT02_04"].delete(0, tk.END)
            campos["CCT02_05"].delete(0, tk.END)
            campos["CCT02_07"].delete(0, tk.END)

    def atualizar_grid_cct02(tree):
        for i in tree.get_children():
            tree.delete(i)

        conn = cct00_0.conectar()
        registros = cct00_0.listar_registros_cct02(conn)
        conn.close()

        for reg in registros:
            tree.insert("", tk.END, values=reg)

    def retornar():
        janela.destroy()
        atualizar_grid_cct02(tree)

    ttk.Button(frame, text="Retornar", width=15, command=retornar).grid(row=8, column=1, pady=20)
    ttk.Button(frame, text="Salvar", width=15, command=gravar).grid(row=8, column=0, pady=20)
 


