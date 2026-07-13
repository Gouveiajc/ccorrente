'''
Programa de Investimentos
Conexão com o Banco CCT.DB e Queries
JC Jan/2026
Ver 1
Banco de Dados cct.db
Módulo cct00_0.py
'''
#parte a
import sqlite3
from tkinter import messagebox

# ============================================================
#   CONEXÃO COM O BANCO
# ============================================================
def conectar():
    return sqlite3.connect("cct.db")

# ============================================================
#   TABELA CCT00
# ============================================================
def inserir_registro(conn, cod, desc, tipo, obs):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO cct00 (cct00_01, cct00_08, cct00_09, cct00_07) VALUES (?,?,?,?)",
        (cod, desc, tipo, obs)
    )
    conn.commit()

def excluir_registro(conn, cod):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cct00 WHERE cct00_01=?", (cod,))
    conn.commit()

def listar_registros(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT cct00_01, cct00_08, cct00_09, cct00_07 FROM cct00 ORDER BY cct00_01")
    return cursor.fetchall()

def existe_codigo(conn, cod):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM cct00 WHERE cct00_01=?", (cod,))
    return cursor.fetchone()[0] > 0

def alterar_registro(conn, cod, desc, tipo, obs):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE cct00
            SET cct00_08 = ?, cct00_09 = ?, cct00_07 = ?
            WHERE cct00_01 = ?
        """, (desc, tipo, obs, cod))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao alterar registro: {e}")

# ============================================================
#   TABELA CCT01
# ============================================================
def listar_registros_cct01(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT cct01_02, cct01_03, cct01_11, cct01_10, cct01_05 FROM CCT01 ORDER BY cct01_02, cct01_03")
    return cursor.fetchall()

def inserir_registro_cct01(conn, cod, conta, desc, saldo, data):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO cct01 (cct01_02, cct01_03, cct01_11, cct01_10, cct01_05) VALUES (?,?,?,?,?)",
        (cod, conta, desc, saldo, data)
    )
    conn.commit()

def excluir_registro_cct01(conn, cod, conta):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cct01 WHERE cct01_02=? AND cct01_03=?", (cod,conta,))
    conn.commit()

def existe_codigo_cct01(conn, cod, conta):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM cct01 WHERE cct01_02=? AND cct01_03=?", (cod,conta,))
    return cursor.fetchone()[0] > 0
