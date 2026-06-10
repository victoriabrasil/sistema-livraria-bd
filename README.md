# Sistema de Livraria - Banco de Dados

Projeto acadêmico desenvolvido para as disciplinas de Laboratório de Banco de Dados e Laboratório de Engenharia de Software.

## Funcionalidades

- Login
- Cadastro de livros
- Cadastro de clientes
- Registro de vendas
- Controle de estoque
- Histórico de vendas
- Integração com banco de dados MySQL

## Tecnologias Utilizadas

- Python 3
- Tkinter
- MySQL
- MySQL Workbench
- Git e GitHub
- Visual Studio Code

## Estrutura do Projeto

livraria-vscode/

main.py
conexao.py

telas/
├── login.py
├── livros.py
├── clientes.py
├── vendas.py
└── historico_vendas.py

banco/
├── schema.sql
├── dados.sql
└── consultas.sql

## Banco de Dados

O banco de dados é composto pelas tabelas:

- livros
- autores
- livro_autor
- clientes
- vendas
- itens_venda

## Consultas Implementadas

- Listagem de vendas com clientes
- Relatório completo de vendas
- Total gasto por cliente
- Livros mais vendidos
- Consulta de estoque baixo
