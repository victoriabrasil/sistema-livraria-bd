import tkinter as tk
from tkinter import ttk, messagebox

from conexao import conectar


def abrir_historico_vendas():

    janela = tk.Toplevel()

    janela.title("Histórico de Vendas")
    janela.geometry("1100x650")
    janela.resizable(False, False)

    # ==================================================
    # FUNÇÕES
    # ==================================================

    def carregar_vendas():

        tabela_vendas.delete(*tabela_vendas.get_children())

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT
                v.id_venda,
                c.nome,
                v.data_venda,
                v.metodo_pagamento,
                v.valor_total
            FROM vendas v
            JOIN clientes c
                ON v.id_cliente = c.id_cliente
            ORDER BY v.id_venda DESC
        """)

        dados = cursor.fetchall()

        for linha in dados:

            tabela_vendas.insert(
                "",
                tk.END,
                values=linha
            )

        conexao.close()

    def mostrar_itens(event):

        tabela_itens.delete(*tabela_itens.get_children())

        item = tabela_vendas.focus()

        if not item:
            return

        valores = tabela_vendas.item(item)["values"]

        id_venda = valores[0]

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT
                l.nome,
                iv.quantidade,
                iv.preco_unitario,
                (iv.quantidade * iv.preco_unitario)
            FROM itens_venda iv
            JOIN livros l
                ON iv.id_livro = l.id_livro
            WHERE iv.id_venda = %s
        """, (id_venda,))

        itens = cursor.fetchall()

        for linha in itens:

            tabela_itens.insert(
                "",
                tk.END,
                values=linha
            )

        conexao.close()

    def exibir_comprovante():

        item = tabela_vendas.focus()

        if not item:

            messagebox.showwarning(
                "Aviso",
                "Selecione uma venda."
            )

            return

        venda = tabela_vendas.item(item)["values"]

        texto = f"""
Venda Nº {venda[0]}

Cliente:
{venda[1]}

Data:
{venda[2]}

Pagamento:
{venda[3]}

Total:
R$ {venda[4]}
"""

        messagebox.showinfo(
            "Comprovante",
            texto
        )

    # ==================================================
    # TÍTULO
    # ==================================================

    tk.Label(
        janela,
        text="Histórico de Vendas",
        font=("Arial", 18, "bold")
    ).pack(pady=10)

    # ==================================================
    # TABELA DE VENDAS
    # ==================================================

    frame_vendas = tk.Frame(janela)
    frame_vendas.pack(pady=10)

    colunas_vendas = (
        "ID",
        "Cliente",
        "Data",
        "Pagamento",
        "Total"
    )

    tabela_vendas = ttk.Treeview(
        frame_vendas,
        columns=colunas_vendas,
        show="headings",
        height=10
    )

    for coluna in colunas_vendas:

        tabela_vendas.heading(
            coluna,
            text=coluna
        )

    tabela_vendas.column("ID", width=60)
    tabela_vendas.column("Cliente", width=250)
    tabela_vendas.column("Data", width=120)
    tabela_vendas.column("Pagamento", width=180)
    tabela_vendas.column("Total", width=100)

    tabela_vendas.pack()

    tabela_vendas.bind(
        "<<TreeviewSelect>>",
        mostrar_itens
    )

    # ==================================================
    # TABELA DE ITENS
    # ==================================================

    tk.Label(
        janela,
        text="Itens da Venda",
        font=("Arial", 14, "bold")
    ).pack(pady=10)

    colunas_itens = (
        "Livro",
        "Quantidade",
        "Preço Unitário",
        "Subtotal"
    )

    tabela_itens = ttk.Treeview(
        janela,
        columns=colunas_itens,
        show="headings",
        height=8
    )

    for coluna in colunas_itens:

        tabela_itens.heading(
            coluna,
            text=coluna
        )

    tabela_itens.column("Livro", width=400)
    tabela_itens.column("Quantidade", width=100)
    tabela_itens.column("Preço Unitário", width=150)
    tabela_itens.column("Subtotal", width=150)

    tabela_itens.pack()

    # ==================================================
    # BOTÕES
    # ==================================================

    frame_botoes = tk.Frame(janela)
    frame_botoes.pack(pady=20)

    tk.Button(
        frame_botoes,
        text="Atualizar",
        width=15,
        command=carregar_vendas
    ).grid(row=0, column=0, padx=10)

    tk.Button(
        frame_botoes,
        text="Comprovante",
        width=15,
        command=exibir_comprovante
    ).grid(row=0, column=1, padx=10)

    carregar_vendas()