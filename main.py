import tkinter as tk
from tkinter import ttk
from telas.login import abrir_login
from telas.livros import abrir_tela_livros
from telas.clientes import abrir_tela_clientes
from telas.vendas import abrir_tela_vendas
from telas.historico_vendas import abrir_historico_vendas
from conexao import conectar

def atualizar_dashboard():

    conexao = conectar()
    cursor = conexao.cursor()

    # livros

    cursor.execute("""
        SELECT COUNT(*)
        FROM livros
    """)

    total_livros = cursor.fetchone()[0]

    # clientes

    cursor.execute("""
        SELECT COUNT(*)
        FROM clientes
    """)

    total_clientes = cursor.fetchone()[0]

    # vendas

    cursor.execute("""
        SELECT COUNT(*)
        FROM vendas
    """)

    total_vendas = cursor.fetchone()[0]

    # faturamento

    cursor.execute("""
        SELECT IFNULL(SUM(valor_total),0)
        FROM vendas
    """)

    faturamento = cursor.fetchone()[0]

    conexao.close()

    lbl_livros.config(
        text=f"📚 Livros cadastrados: {total_livros}"
    )

    lbl_clientes.config(
        text=f"👥 Clientes cadastrados: {total_clientes}"
    )

    lbl_vendas.config(
        text=f"🛒 Vendas realizadas: {total_vendas}"
    )

    lbl_faturamento.config(
        text=f"💰 Faturamento: R$ {float(faturamento):.2f}"
    )

janela = tk.Tk()

janela.withdraw()

# Configurações da janela
janela.title("Sistema de Livraria")
janela.geometry("800x500")
janela.resizable(False, False)

# Título
titulo = tk.Label(
    janela,
    text="Sistema de Livraria",
    font=("Arial", 20, "bold")
)

titulo.pack(pady=30)

frame_dashboard = tk.Frame(janela)
frame_dashboard.pack(pady=10)

lbl_livros = tk.Label(
    frame_dashboard,
    font=("Arial", 12, "bold")
)

lbl_livros.pack(pady=3)

lbl_clientes = tk.Label(
    frame_dashboard,
    font=("Arial", 12, "bold")
)

lbl_clientes.pack(pady=3)

lbl_vendas = tk.Label(
    frame_dashboard,
    font=("Arial", 12, "bold")
)

lbl_vendas.pack(pady=3)

lbl_faturamento = tk.Label(
    frame_dashboard,
    font=("Arial", 12, "bold")
)

lbl_faturamento.pack(pady=3)

# Frame dos botões
frame_botoes = tk.Frame(janela)
frame_botoes.pack(pady=20)

# Botão Livros
btn_livros = tk.Button(
    frame_botoes,
    text="Livros",
    width=20,
    height=2,
    command=abrir_tela_livros
)

btn_livros.grid(row=0, column=0, padx=10)

# Botão Clientes
btn_clientes = tk.Button(
    frame_botoes,
    text="Clientes",
    width=20,
    height=2,
    command=abrir_tela_clientes
)

btn_clientes.grid(row=0, column=1, padx=10)

# Botão Vendas
btn_vendas = tk.Button(
    frame_botoes,
    text="Vendas",
    width=20,
    height=2,
    command=abrir_tela_vendas
)

# Botão Histórico Vendas
btn_historico = tk.Button(
    frame_botoes,
    text="Histórico",
    width=20,
    height=2,
    command=abrir_historico_vendas
)

btn_historico.grid(
    row=1,
    column=1,
    padx=10,
    pady=10
)

btn_vendas.grid(row=0, column=2, padx=10)

def atualizar_periodicamente():

    atualizar_dashboard()

    janela.after(
        5000,
        atualizar_periodicamente
    )

atualizar_periodicamente()

abrir_login(janela)
janela.mainloop()