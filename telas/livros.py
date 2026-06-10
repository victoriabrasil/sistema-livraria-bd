import tkinter as tk
from tkinter import ttk, messagebox

from conexao import conectar


def abrir_tela_livros():

    janela = tk.Toplevel()

    janela.title("Cadastro de Livros")
    janela.geometry("950x600")
    janela.resizable(False, False)

    id_selecionado = None

    # ==================================================
    # FUNÇÕES
    # ==================================================

    def carregar_livros():

        tabela.delete(*tabela.get_children())

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT
                id_livro,
                nome,
                isbn,
                preco,
                genero,
                quantidade_estoque
            FROM livros
        """)

        dados = cursor.fetchall()

        for linha in dados:
            tabela.insert("", tk.END, values=linha)

        conexao.close()

    def limpar_campos():

        nonlocal id_selecionado

        id_selecionado = None

        entry_nome.delete(0, tk.END)
        entry_isbn.delete(0, tk.END)
        entry_preco.delete(0, tk.END)
        combo_genero.set("")
        entry_estoque.delete(0, tk.END)

    def salvar_livro():

        nome = entry_nome.get()
        isbn = entry_isbn.get()
        preco = entry_preco.get()
        genero = combo_genero.get()
        estoque = entry_estoque.get()

        if not nome:
            messagebox.showerror(
                "Erro",
                "Informe o nome do livro."
            )
            return

        try:

            conexao = conectar()
            cursor = conexao.cursor()

            cursor.execute("""
                INSERT INTO livros
                (
                    nome,
                    isbn,
                    preco,
                    genero,
                    quantidade_estoque
                )
                VALUES (%s,%s,%s,%s,%s)
            """, (
                nome,
                isbn,
                preco,
                genero,
                estoque
            ))

            conexao.commit()

            conexao.close()

            carregar_livros()
            limpar_campos()

            messagebox.showinfo(
                "Sucesso",
                "Livro cadastrado."
            )

        except Exception as erro:
            messagebox.showerror(
                "Erro",
                str(erro)
            )

    def selecionar_livro(event):

        nonlocal id_selecionado

        item = tabela.focus()

        if not item:
            return

        dados = tabela.item(item)

        valores = dados["values"]

        id_selecionado = valores[0]

        limpar_campos()

        id_selecionado = valores[0]

        entry_nome.insert(0, valores[1])
        entry_isbn.insert(0, valores[2])
        entry_preco.insert(0, valores[3])
        combo_genero.set(valores[4])
        entry_estoque.insert(0, valores[5])

    def atualizar_livro():

        if id_selecionado is None:

            messagebox.showwarning(
                "Aviso",
                "Selecione um livro."
            )

            return

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            UPDATE livros
            SET
                nome=%s,
                isbn=%s,
                preco=%s,
                genero=%s,
                quantidade_estoque=%s
            WHERE id_livro=%s
        """, (
            entry_nome.get(),
            entry_isbn.get(),
            entry_preco.get(),
            combo_genero.get(),
            entry_estoque.get(),
            id_selecionado
        ))

        conexao.commit()
        conexao.close()

        carregar_livros()
        limpar_campos()

        messagebox.showinfo(
            "Sucesso",
            "Livro atualizado."
        )

    def excluir_livro():

        if id_selecionado is None:

            messagebox.showwarning(
                "Aviso",
                "Selecione um livro."
            )

            return

        resposta = messagebox.askyesno(
            "Confirmar",
            "Deseja excluir este livro?"
        )

        if not resposta:
            return

        try:

            conexao = conectar()
            cursor = conexao.cursor()

            cursor.execute("""
                DELETE FROM livros
                WHERE id_livro=%s
            """, (id_selecionado,))

            conexao.commit()
            conexao.close()

            carregar_livros()
            limpar_campos()

            messagebox.showinfo(
                "Sucesso",
                "Livro excluído."
            )

        except Exception:

            messagebox.showerror(
                "Erro",
                "Livro vinculado a vendas."
            )

    # ==================================================
    # TÍTULO
    # ==================================================

    titulo = tk.Label(
        janela,
        text="Gerenciamento de Livros",
        font=("Arial", 18, "bold")
    )

    titulo.pack(pady=10)

    # ==================================================
    # FORMULÁRIO
    # ==================================================

    frame_form = tk.Frame(janela)
    frame_form.pack()

    tk.Label(frame_form, text="Título").grid(row=0, column=0)

    entry_nome = tk.Entry(frame_form, width=40)
    entry_nome.grid(row=1, column=0, padx=5)

    tk.Label(frame_form, text="ISBN").grid(row=0, column=1)

    entry_isbn = tk.Entry(frame_form, width=25)
    entry_isbn.grid(row=1, column=1, padx=5)

    tk.Label(frame_form, text="Preço").grid(row=2, column=0)

    entry_preco = tk.Entry(frame_form, width=20)
    entry_preco.grid(row=3, column=0)

    tk.Label(frame_form, text="Gênero").grid(row=2, column=1)

    combo_genero = ttk.Combobox(
        frame_form,
        values=[
            "Romance",
            "Fantasia",
            "Terror",
            "Suspense",
            "Drama",
            "Distopia",
            "História",
            "Mistério",
            "Clássico",
            "Ficção Científica",
            "Autoajuda"
        ]
    )

    combo_genero.grid(row=3, column=1)

    tk.Label(frame_form, text="Estoque").grid(row=2, column=2)

    entry_estoque = tk.Entry(frame_form, width=10)
    entry_estoque.grid(row=3, column=2)

    # ==================================================
    # BOTÕES
    # ==================================================

    frame_botoes = tk.Frame(janela)
    frame_botoes.pack(pady=10)

    tk.Button(
        frame_botoes,
        text="Salvar",
        width=12,
        command=salvar_livro
    ).grid(row=0, column=0, padx=5)

    tk.Button(
        frame_botoes,
        text="Atualizar",
        width=12,
        command=atualizar_livro
    ).grid(row=0, column=1, padx=5)

    tk.Button(
        frame_botoes,
        text="Excluir",
        width=12,
        command=excluir_livro
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
        "Título",
        "ISBN",
        "Preço",
        "Gênero",
        "Estoque"
    )

    tabela = ttk.Treeview(
        janela,
        columns=colunas,
        show="headings",
        height=15
    )

    for coluna in colunas:
        tabela.heading(coluna, text=coluna)

    tabela.column("ID", width=50)
    tabela.column("Título", width=250)

    tabela.pack(fill="both", expand=True)

    tabela.bind(
        "<<TreeviewSelect>>",
        selecionar_livro
    )

    carregar_livros()