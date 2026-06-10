import tkinter as tk
from tkinter import messagebox


def abrir_login(janela_principal):

    login = tk.Tk()

    login.title("Login")
    login.geometry("350x250")
    login.resizable(False, False)

    # ==========================
    # FUNÇÃO LOGIN
    # ==========================

    def fazer_login():

        usuario = entry_usuario.get()
        senha = entry_senha.get()

        if usuario == "admin" and senha == "123":

            login.destroy()

            janela_principal.deiconify()

        else:

            messagebox.showerror(
                "Erro",
                "Usuário ou senha inválidos."
            )

    # ==========================
    # TÍTULO
    # ==========================

    tk.Label(
        login,
        text="Sistema de Livraria",
        font=("Arial", 18, "bold")
    ).pack(pady=20)

    # ==========================
    # USUÁRIO
    # ==========================

    tk.Label(
        login,
        text="Usuário"
    ).pack()

    entry_usuario = tk.Entry(
        login,
        width=30
    )

    entry_usuario.pack(pady=5)

    # ==========================
    # SENHA
    # ==========================

    tk.Label(
        login,
        text="Senha"
    ).pack()

    entry_senha = tk.Entry(
        login,
        width=30,
        show="*"
    )

    entry_senha.pack(pady=5)

    # ==========================
    # BOTÃO
    # ==========================

    tk.Button(
        login,
        text="Entrar",
        width=20,
        command=fazer_login
    ).pack(pady=20)

    login.mainloop()