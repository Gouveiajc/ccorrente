'''
Programa de Cadastro de Tipos de Natureza
Inclusão
JC Jul/2026
Ver 1
Banco de Dados cct.db
Tabela cct00
Módulo cct11_02.py
'''
import tkinter as tk
from tkinter import ttk, messagebox
import cct00_0
def abrir_janela(root, atualizar_grid_callback=None):

    janela = tk.Toplevel(root)
    janela.title("Inclusão de Tipo de Ativo")
    janela.geometry("450x300")
    janela.grab_set()

    # -----------------------------
    # CAMPOS
    # -----------------------------
    frame = ttk.Frame(janela, padding=20)
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text="Código:").grid(row=0, column=0, sticky="w", pady=5)
    entry_codigo = ttk.Entry(frame, width=10)
    entry_codigo.grid(row=0, column=1, sticky="w", pady=5)

    ttk.Label(frame, text="Descrição:").grid(row=1, column=0, sticky="w", pady=5)
    entry_descricao = ttk.Entry(frame, width=30)
    entry_descricao.grid(row=1, column=1, sticky="w", pady=5)

    ttk.Label(frame, text="Tipo:").grid(row=2, column=0, sticky="w", pady=5)
    entry_tipo = ttk.Entry(frame, width=10)
    entry_tipo.grid(row=2, column=1, sticky="w", pady=5)

    ttk.Label(frame, text="Observação:").grid(row=3, column=0, sticky="w", pady=5)
    entry_obs = ttk.Entry(frame, width=50)
    entry_obs.grid(row=3, column=1, sticky="w", pady=5)
 
    # -----------------------------
    # FUNÇÃO SALVAR
    # -----------------------------
    def salvar():
        cod = entry_codigo.get().strip()
        desc = entry_descricao.get().strip()
        tipo = entry_tipo.get().strip()
        obs = entry_obs.get().strip()

        # Validação
        if not cod or not desc or not tipo:
            messagebox.showwarning("Atenção", "Preencha todos os campos!", parent=janela)
            return

        conn = cct00_0.conectar()

        #Verifica se Existe Registro
        if cct00_0.existe_codigo(conn,cod):
            messagebox.showinfo("Erro", "Registro já Existe!", parent=janela)
            return
        else:
            # Gravação
            cct00_0.inserir_registro(conn, cod, desc, tipo, obs)
            conn.close()

        if atualizar_grid_callback:
            atualizar_grid_callback()

        messagebox.showinfo("Sucesso", "Registro incluído com sucesso!", parent=janela)
        janela.destroy()

    # -----------------------------
    # BOTÕES
    # -----------------------------
    frame_botoes = ttk.Frame(janela, padding=10)
    frame_botoes.pack()

    ttk.Button(frame_botoes, text="Salvar", width=12, command=salvar).grid(row=0, column=0, padx=10)
    ttk.Button(frame_botoes, text="Cancelar", width=12, command=janela.destroy).grid(row=0, column=1, padx=10)


