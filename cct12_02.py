'''
Programa de Cadastro de Cadastro de Contas Corrente
Inclusão
JC Jul/2026
Ver 1
Banco de Dados cct.db
Tabela cct01
Módulo: cct12_02.py
'''
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import cct00_0

def abrir_janela_inv01(root, tree):
    # Evita abrir mais de uma janela de inclusão
    for widget in root.winfo_children():
        if isinstance(widget, tk.Toplevel) and widget.title() == "Inclusão de Conta Corrente":
            widget.lift()
            widget.focus_force()
            return

    janela = tk.Toplevel(root)
    janela.title("Inclusão de Conta Corrente")
    janela.geometry("550x350")

    janela.transient(root)
    janela.grab_set()
    janela.bind("<Escape>", lambda e: janela.destroy())

    frame = ttk.Frame(janela, padding=20)
    frame.pack(fill="both", expand=True)

    # --- CAMPOS ---
    ttk.Label(frame, text="Código Banco :").grid(row=0, column=0, sticky="w", pady=5)
    entry_codigo = ttk.Entry(frame, width=10)
    entry_codigo.grid(row=0, column=1, sticky="w", pady=5)

    ttk.Label(frame, text="Conta Corrente:").grid(row=1, column=0, sticky="w", pady=5)
    entry_conta = ttk.Entry(frame, width=30)
    entry_conta.grid(row=1, column=1, sticky="w", pady=5)

    ttk.Label(frame, text="Descrição Banco:").grid(row=3, column=0, sticky="w", pady=5)
    entry_desc = ttk.Entry(frame, width=250)
    entry_desc.grid(row=3, column=1, sticky="w", pady=5)

    ttk.Label(frame, text="Saldo:").grid(row=4, column=0, sticky="w", pady=5)
    entry_saldo = ttk.Entry(frame, width=10)
    entry_saldo.grid(row=4, column=1, sticky="w", pady=5)

    ttk.Label(frame, text="Data:").grid(row=5, column=0, sticky="w", pady=5)
    entry_data = ttk.Entry(frame, width=10)
    entry_data.grid(row=5, column=1, sticky="w", pady=5)

    def to_uppercase(event):
        # Transforma em maiúsculo sem perder a posição do cursor
        posicao = entry_desc.index(tk.INSERT)
        texto = entry_desc.get().upper()
        entry_desc.delete(0, tk.END)
        entry_desc.insert(0, texto)
        entry_desc.icursor(posicao)

    entry_desc.bind("<KeyRelease>", to_uppercase)

    # --- FUNÇÃO SALVAR ---
    def salvar():
        cod = entry_codigo.get().strip()
        conta = entry_conta.get().strip()
        desc = entry_desc.get().strip()
        saldo = entry_saldo.get().strip()
        data = entry_data.get().strip()

        try:
            saldo_float = float(saldo.replace(',', '.')) # Aceita vírgula ou ponto
            
            conn = cct00_0.conectar()
            
            # 1. Verifica duplicidade de código
            if cct00_0.existe_codigo_cct01(conn, cod, conta):
                messagebox.showwarning("Atenção", f"O código {cod} conta {conta} já existe.", parent=janela)
                return

            # 3. Grava registro
            cct00_0.inserir_registro_cct01(conn, cod, conta, desc, saldo_float, data)
            
            # 4. Atualiza o Treeview (Inserindo apenas o novo para performance)
            # Se preferir recarregar tudo, mantenha seu loop de delete/insert aqui
            tree.insert("", tk.END, values=(cod, conta, desc, saldo_float, data))
            
            messagebox.showinfo("Sucesso", "Registro incluído com sucesso!", parent=janela)

            # Limpa campos e foca no código
            entry_codigo.delete(0, tk.END)
            entry_conta.delete(0,tk.END)
            entry_desc.delete(0, tk.END)
            entry_saldo.delete(0, tk.END)
            entry_data.delete(0, tk.END)
            entry_codigo.focus()

        except Exception as e:
            messagebox.showerror("Erro Fatal", f"Erro ao salvar: {e}", parent=janela)
        finally:
            if conn:
                conn.close()

    # --- BOTÕES ---
    frame_botoes = ttk.Frame(janela, padding=10)
    frame_botoes.pack()

    ttk.Button(frame_botoes, text="Salvar", width=12, command=salvar).grid(row=0, column=0, padx=10)
    ttk.Button(frame_botoes, text="Retornar", width=12, command=janela.destroy).grid(row=0, column=1, padx=10)

    entry_codigo.focus()
