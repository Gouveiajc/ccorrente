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
def inserir_registro_cct00(conn, cod, desc, tipo, obs):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO cct00 (cct00_01, cct00_08, cct00_09, cct00_07) VALUES (?,?,?,?)",
        (cod, desc, tipo, obs)
    )
    conn.commit()

def excluir_registro_cct00(conn, cod):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cct00 WHERE cct00_01=?", (cod,))
    conn.commit()

def listar_registros_cct00(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT cct00_01, cct00_08, cct00_09, cct00_07 FROM cct00 ORDER BY cct00_01")
    return cursor.fetchall()

def listar_registros_reduzido_cct00(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT cct00_01, cct00_08 FROM cct00 ORDER BY cct00_01")
    return cursor.fetchall()

def existe_codigo_cct00(conn, cod):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM cct00 WHERE cct00_01=?", (cod,))
    return cursor.fetchone()[0] > 0

def alterar_registro_cct00(conn, cod, desc, tipo, obs):
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

def listar_registros_reduzido_cct01(conn,codigo):
    cursor = conn.cursor()
    cursor.execute("SELECT cct01_03, cct01_11 FROM CCT01 WHERE CCT01_02=?",(codigo,))
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

# ============================================================
#   TABELA CCT02
# ============================================================
def listar_registros_cct02(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT cct02_00, cct02_02, cct02_03, cct02_11, cct02_01, cct02_08, cct02_04, cct02_05, cct02_07 FROM cct02 ORDER BY cct02_02, cct02_03, cct02_05")
    return cursor.fetchall()

def inserir_registro_cct02(conn, registro):
    """
    Insere um registro na tabela cct02.
    'registro' é um dicionário contendo todos os campos da tela.
    """

    sql = """
        INSERT INTO CCT02 (
            CCT02_02, -- CODIGO BANCO
            CCT02_03, -- CONTA CORRENTE - DIGITO
            CCT02_11, -- DESCRIÇÃO BANCO
            CCT02_01, -- NATUREZA
            CCT02_08, -- DESCRIÇÃO NATUREZA
            CCT02_04, -- VALOR
            CCT02_05, -- DATA
            CCT02_07  -- OBSERVAÇÃO
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?
        )
    """
    valores = (
        registro["CCT02_02"],
        registro["CCT02_03"],
        registro["CCT02_11"],
        registro["CCT02_01"],
        registro["CCT02_08"],
        registro["CCT02_04"],
        registro["CCT02_05"],
        registro["CCT02_07"]
    )

    cursor = conn.cursor()
    cursor.execute(sql, valores)
    conn.commit()

