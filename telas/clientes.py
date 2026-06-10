import tkinter as tk
from tkinter import ttk, messagebox

from conexao import conectar


def abrir_tela_clientes():

    janela = tk.Toplevel()

    janela.title("Cadastro de Clientes")
    janela.geometry("900x600")
    janela.resizable(False, False)

    id_selecionado = None

    # ==================================================
    # FUNÇÕES
    # ==================================================

    def carregar_clientes():

        tabela.delete(*tabela.get_children())

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT
                id_cliente,
                nome,
                cpf,
                email
            FROM clientes
        """)

        dados = cursor.fetchall()

        for linha in dados:
            tabela.insert("", tk.END, values=linha)

        conexao.close()

    def limpar_campos():

        nonlocal id_selecionado

        id_selecionado = None

        entry_nome.delete(0, tk.END)
        entry_cpf.delete(0, tk.END)
        entry_email.delete(0, tk.END)

    def salvar_cliente():

        nome = entry_nome.get()
        cpf = entry_cpf.get()
        email = entry_email.get()

        if nome == "" or cpf == "":

            messagebox.showerror(
                "Erro",
                "Nome e CPF são obrigatórios."
            )

            return

        try:

            conexao = conectar()
            cursor = conexao.cursor()

            cursor.execute("""
                INSERT INTO clientes
                (
                    nome,
                    cpf,
                    email
                )
                VALUES (%s,%s,%s)
            """, (
                nome,
                cpf,
                email
            ))

            conexao.commit()
            conexao.close()

            carregar_clientes()
            limpar_campos()

            messagebox.showinfo(
                "Sucesso",
                "Cliente cadastrado."
            )

        except Exception as erro:

            messagebox.showerror(
                "Erro",
                str(erro)
            )

    def selecionar_cliente(event):

        nonlocal id_selecionado

        item = tabela.focus()

        if not item:
            return

        valores = tabela.item(item)["values"]

        limpar_campos()

        id_selecionado = valores[0]

        entry_nome.insert(0, valores[1])
        entry_cpf.insert(0, valores[2])
        entry_email.insert(0, valores[3])

    def atualizar_cliente():

        if id_selecionado is None:

            messagebox.showwarning(
                "Aviso",
                "Selecione um cliente."
            )

            return

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            UPDATE clientes
            SET
                nome=%s,
                cpf=%s,
                email=%s
            WHERE id_cliente=%s
        """, (
            entry_nome.get(),
            entry_cpf.get(),
            entry_email.get(),
            id_selecionado
        ))

        conexao.commit()
        conexao.close()

        carregar_clientes()
        limpar_campos()

        messagebox.showinfo(
            "Sucesso",
            "Cliente atualizado."
        )

    def excluir_cliente():

        if id_selecionado is None:

            messagebox.showwarning(
                "Aviso",
                "Selecione um cliente."
            )

            return

        resposta = messagebox.askyesno(
            "Confirmação",
            "Deseja excluir este cliente?"
        )

        if not resposta:
            return

        try:

            conexao = conectar()
            cursor = conexao.cursor()

            cursor.execute("""
                DELETE FROM clientes
                WHERE id_cliente=%s
            """, (id_selecionado,))

            conexao.commit()
            conexao.close()

            carregar_clientes()
            limpar_campos()

            messagebox.showinfo(
                "Sucesso",
                "Cliente excluído."
            )

        except Exception:

            messagebox.showerror(
                "Erro",
                "Cliente vinculado a vendas."
            )

    # ==================================================
    # TÍTULO
    # ==================================================

    titulo = tk.Label(
        janela,
        text="Gerenciamento de Clientes",
        font=("Arial", 18, "bold")
    )

    titulo.pack(pady=10)

    # ==================================================
    # FORMULÁRIO
    # ==================================================

    frame_form = tk.Frame(janela)
    frame_form.pack(pady=10)

    tk.Label(
        frame_form,
        text="Nome"
    ).grid(row=0, column=0)

    entry_nome = tk.Entry(
        frame_form,
        width=35
    )

    entry_nome.grid(
        row=1,
        column=0,
        padx=5
    )

    tk.Label(
        frame_form,
        text="CPF"
    ).grid(row=0, column=1)

    entry_cpf = tk.Entry(
        frame_form,
        width=20
    )

    entry_cpf.grid(
        row=1,
        column=1,
        padx=5
    )

    tk.Label(
        frame_form,
        text="E-mail"
    ).grid(row=0, column=2)

    entry_email = tk.Entry(
        frame_form,
        width=30
    )

    entry_email.grid(
        row=1,
        column=2,
        padx=5
    )

    # ==================================================
    # BOTÕES
    # ==================================================

    frame_botoes = tk.Frame(janela)
    frame_botoes.pack(pady=10)

    tk.Button(
        frame_botoes,
        text="Salvar",
        width=12,
        command=salvar_cliente
    ).grid(row=0, column=0, padx=5)

    tk.Button(
        frame_botoes,
        text="Atualizar",
        width=12,
        command=atualizar_cliente
    ).grid(row=0, column=1, padx=5)

    tk.Button(
        frame_botoes,
        text="Excluir",
        width=12,
        command=excluir_cliente
    ).grid(row=0, column=2, padx=5)

    tk.Button(
        frame_botoes,
        text="Limpar",
        width=12,
        command=limpar_campos
    ).grid(row=0, column=3, padx=5)

    # ==================================================
    # TABELA
    # ==================================================

    colunas = (
        "ID",
        "Nome",
        "CPF",
        "E-mail"
    )

    tabela = ttk.Treeview(
        janela,
        columns=colunas,
        show="headings",
        height=15
    )

    for coluna in colunas:

        tabela.heading(
            coluna,
            text=coluna
        )

    tabela.column("ID", width=50)
    tabela.column("Nome", width=250)
    tabela.column("CPF", width=150)
    tabela.column("E-mail", width=250)

    tabela.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    tabela.bind(
        "<<TreeviewSelect>>",
        selecionar_cliente
    )

    carregar_clientes()