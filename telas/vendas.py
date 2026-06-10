import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

from conexao import conectar


def abrir_tela_vendas():

    janela = tk.Toplevel()

    janela.title("Registro de Vendas")
    janela.geometry("1000x650")
    janela.resizable(False, False)

    carrinho = []

    clientes = {}
    livros = {}

    # ==================================================
    # FUNÇÕES DE CARREGAMENTO
    # ==================================================

    def carregar_clientes():

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT id_cliente, nome
            FROM clientes
            ORDER BY nome
        """)

        dados = cursor.fetchall()

        lista = []

        for id_cliente, nome in dados:

            clientes[nome] = id_cliente
            lista.append(nome)

        combo_cliente["values"] = lista

        conexao.close()

    def carregar_livros():

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT id_livro, nome
            FROM livros
            ORDER BY nome
        """)

        dados = cursor.fetchall()

        lista = []

        for id_livro, nome in dados:

            livros[nome] = id_livro
            lista.append(nome)

        combo_livro["values"] = lista

        conexao.close()

    # ==================================================
    # TOTAL
    # ==================================================

    def atualizar_total():

        total = 0

        for item in carrinho:

            total += item["quantidade"] * item["preco"]

        label_total.config(
            text=f"Total: R$ {total:.2f}"
        )

    # ==================================================
    # CARRINHO
    # ==================================================

    def adicionar_item():

        livro_nome = combo_livro.get()

        if livro_nome == "":
            messagebox.showwarning(
                "Aviso",
                "Selecione um livro."
            )
            return

        try:
            quantidade = int(entry_quantidade.get())
        except:
            messagebox.showerror(
                "Erro",
                "Quantidade inválida."
            )
            return

        id_livro = livros[livro_nome]

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT preco, quantidade_estoque
            FROM livros
            WHERE id_livro=%s
        """, (id_livro,))

        preco, estoque = cursor.fetchone()

        conexao.close()

        if estoque <= 0:

            messagebox.showerror(
                "Erro",
                "Livro sem estoque."
            )
            return

        if quantidade > estoque:

            messagebox.showerror(
                "Erro",
                f"Estoque disponível: {estoque}"
            )
            return

        carrinho.append({

            "id_livro": id_livro,
            "nome": livro_nome,
            "quantidade": quantidade,
            "preco": float(preco)

        })

        tabela.insert(
            "",
            tk.END,
            values=(
                livro_nome,
                quantidade,
                f"R$ {(quantidade * float(preco)):.2f}"
            )
        )

        atualizar_total()

        entry_quantidade.delete(0, tk.END)

    # ==================================================
    # LIMPAR
    # ==================================================

    def limpar_venda():

        carrinho.clear()

        tabela.delete(*tabela.get_children())

        combo_cliente.set("")
        combo_livro.set("")

        combo_pagamento.set("")

        entry_quantidade.delete(0, tk.END)

        atualizar_total()

    # ==================================================
    # FINALIZAR
    # ==================================================

    def finalizar_venda():

        if combo_cliente.get() == "":

            messagebox.showwarning(
                "Aviso",
                "Selecione um cliente."
            )
            return

        if len(carrinho) == 0:

            messagebox.showwarning(
                "Aviso",
                "Adicione itens à venda."
            )
            return

        id_cliente = clientes[combo_cliente.get()]

        metodo = combo_pagamento.get()

        if metodo == "":

            messagebox.showwarning(
                "Aviso",
                "Selecione o pagamento."
            )
            return

        total = 0

        for item in carrinho:

            total += item["quantidade"] * item["preco"]

        conexao = conectar()
        cursor = conexao.cursor()

        # venda

        cursor.execute("""
            INSERT INTO vendas
            (
                id_cliente,
                data_venda,
                metodo_pagamento,
                valor_total
            )
            VALUES (%s,%s,%s,%s)
        """, (
            id_cliente,
            date.today(),
            metodo,
            total
        ))

        id_venda = cursor.lastrowid

        # itens

        for item in carrinho:

            cursor.execute("""
                INSERT INTO itens_venda
                (
                    id_venda,
                    id_livro,
                    quantidade,
                    preco_unitario
                )
                VALUES (%s,%s,%s,%s)
            """, (
                id_venda,
                item["id_livro"],
                item["quantidade"],
                item["preco"]
            ))

            cursor.execute("""
                UPDATE livros
                SET quantidade_estoque =
                quantidade_estoque - %s
                WHERE id_livro=%s
            """, (
                item["quantidade"],
                item["id_livro"]
            ))

        conexao.commit()
        conexao.close()

        comprovante = f"""
VENDA Nº {id_venda}

Cliente:
{combo_cliente.get()}

Pagamento:
{metodo}

Total:
R$ {total:.2f}
"""

        messagebox.showinfo(
            "Venda concluída",
            comprovante
        )

        limpar_venda()

    # ==================================================
    # TÍTULO
    # ==================================================

    tk.Label(
        janela,
        text="Registro de Vendas",
        font=("Arial", 18, "bold")
    ).pack(pady=10)

    # ==================================================
    # FORM
    # ==================================================

    frame = tk.Frame(janela)
    frame.pack()

    tk.Label(frame, text="Cliente").grid(row=0, column=0)

    combo_cliente = ttk.Combobox(
        frame,
        width=35
    )

    combo_cliente.grid(
        row=1,
        column=0,
        padx=5
    )

    tk.Label(frame, text="Livro").grid(row=0, column=1)

    combo_livro = ttk.Combobox(
        frame,
        width=35
    )

    combo_livro.grid(
        row=1,
        column=1,
        padx=5
    )

    tk.Label(
        frame,
        text="Quantidade"
    ).grid(row=0, column=2)

    entry_quantidade = tk.Entry(
        frame,
        width=10
    )

    entry_quantidade.grid(
        row=1,
        column=2
    )

    tk.Button(
        frame,
        text="Adicionar",
        command=adicionar_item
    ).grid(
        row=1,
        column=3,
        padx=10
    )

    # ==================================================
    # TABELA
    # ==================================================

    tabela = ttk.Treeview(

        janela,

        columns=(
            "Livro",
            "Quantidade",
            "Subtotal"
        ),

        show="headings",
        height=12

    )

    tabela.heading("Livro", text="Livro")
    tabela.heading("Quantidade", text="Quantidade")
    tabela.heading("Subtotal", text="Subtotal")

    tabela.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )

    # ==================================================
    # RODAPÉ
    # ==================================================

    frame2 = tk.Frame(janela)
    frame2.pack()

    label_total = tk.Label(
        frame2,
        text="Total: R$ 0.00",
        font=("Arial", 12, "bold")
    )

    label_total.grid(
        row=0,
        column=0,
        padx=20
    )

    combo_pagamento = ttk.Combobox(
        frame2,
        values=[
            "PIX",
            "Cartão de Débito",
            "Cartão de Crédito"
        ]
    )

    combo_pagamento.grid(
        row=0,
        column=1,
        padx=20
    )

    tk.Button(
        frame2,
        text="Finalizar Venda",
        command=finalizar_venda
    ).grid(
        row=0,
        column=2,
        padx=10
    )

    tk.Button(
        frame2,
        text="Limpar",
        command=limpar_venda
    ).grid(
        row=0,
        column=3,
        padx=10
    )

    carregar_clientes()
    carregar_livros()