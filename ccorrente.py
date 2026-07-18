'''
Programa de Controle de Conta Corrente
JC 07/2026
Ver. 1
'''

import tkinter as tk
from tkinter import Menu
import cct11_01
import cct12_01
import cct21_01


class App:

    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Controle de Conta Corrente")

        # Inicia maximizado com botões X, minimizar e maximizar (Linux)
        try:
            self.root.attributes("-zoomed", True)
        except:
            self.root.state("zoomed")

        # ESC volta ao tamanho normal
        self.root.bind("<Escape>", lambda e: self.root.state("normal"))

        # Captura do clique no X
        self.root.protocol("WM_DELETE_WINDOW", self.sair)

        self.criar_menu()

    # -----------------------------
    #       MENU PRINCIPAL
    # -----------------------------
    def criar_menu(self):
        menu_bar = Menu(self.root)

        # MENU CADASTRO
        menu_cadastro = Menu(menu_bar, tearoff=0)
        menu_cadastro.add_command(
            label="Tipo de Natureza",
            command=lambda: cct11_01.abrir_lista(self.root)
        )
        menu_cadastro.add_command(
            label="Conta Corrente", 
            command=lambda: cct12_01.abrir_lista(self.root)
        )
        
        menu_bar.add_cascade(label="Cadastro", menu=menu_cadastro)
        
        # MENU MANUTENÇÃO
        menu_manutencao = Menu(menu_bar, tearoff=0)
        menu_manutencao.add_command(
            label="Movimento", 
            command=lambda: cct21_01.abrir_lista(self.root)
        )

        menu_bar.add_cascade(label="Manutenção", menu=menu_manutencao)

        # MENU Orçamento
        menu_impressao = Menu(menu_bar, tearoff=0)

        menu_impressao.add_command(
            label="Orçamento", 
            command=lambda: cct41_01.gerar_pdf_movim(root)
        )
        menu_bar.add_cascade(label="Orçamento", menu=menu_impressao)

    # MENU IMPRESSÃO
        menu_impressao = Menu(menu_bar, tearoff=0)

        menu_impressao.add_command(
            label="Impressão de Movimentação", 
            command=lambda: cct51_01.gerar_pdf_movim(root)
        )
        menu_bar.add_cascade(label="Impressão", menu=menu_impressao)
        # MENU SAIR
        menu_bar.add_command(label="Sair", command=self.sair)

        self.root.config(menu=menu_bar)

    # -----------------------------
    #       FUNÇÕES DO MENU
    # -----------------------------
    def cadastrar_classe(self):
        print("Cadastro de Classe de Ativos selecionado")

    def cadastrar_ativos(self):
        print("Cadastro de Ativos selecionado")

    def manutencao(self):
        print("Menu Manutenção selecionado")

    def impressao(self):
        print("Menu Impressão selecionado")

    def sair(self):
        self.root.quit()


# -----------------------------
#       INICIAR APLICAÇÃO
# -----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
