CREATE DATABASE IF NOT EXISTS livraria;
USE livraria;

CREATE TABLE livros (
  id_livro INT NOT NULL AUTO_INCREMENT,
  nome VARCHAR(40) NOT NULL,
  isbn VARCHAR(20),
  preco DECIMAL(10,2),
  genero VARCHAR(20),
  quantidade_estoque INT NOT NULL,
  PRIMARY KEY (id_livro),
  UNIQUE (isbn)
) DEFAULT CHARSET=utf8mb4;

CREATE TABLE autores (
  id_autor INT NOT NULL AUTO_INCREMENT,
  nome VARCHAR(30) NOT NULL,
  PRIMARY KEY (id_autor)
) DEFAULT CHARSET=utf8mb4;

CREATE TABLE livro_autor (
  id_livro INT NOT NULL,
  id_autor INT NOT NULL,
  PRIMARY KEY (id_livro, id_autor),
  FOREIGN KEY (id_livro) REFERENCES livros(id_livro),
  FOREIGN KEY (id_autor) REFERENCES autores(id_autor)
) DEFAULT CHARSET=utf8mb4;

CREATE TABLE clientes (
  id_cliente INT NOT NULL AUTO_INCREMENT,
  nome VARCHAR(30) NOT NULL,
  cpf VARCHAR(11) NOT NULL,
  email VARCHAR(50) NOT NULL,
  PRIMARY KEY (id_cliente),
  UNIQUE (cpf),
  UNIQUE (email)
) DEFAULT CHARSET=utf8mb4;

CREATE TABLE vendas (
  id_venda INT NOT NULL AUTO_INCREMENT,
  id_cliente INT NOT NULL,
  data_venda DATE NOT NULL,
  metodo_pagamento VARCHAR(20),
  valor_total DECIMAL(10,2),
  PRIMARY KEY (id_venda),
  FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
  ON DELETE RESTRICT
) DEFAULT CHARSET=utf8mb4;

CREATE TABLE itens_venda (
  id_item INT NOT NULL AUTO_INCREMENT,
  id_venda INT NOT NULL,
  id_livro INT NOT NULL,
  quantidade INT NOT NULL,
  preco_unitario DECIMAL(10,2),
  PRIMARY KEY (id_item),
  FOREIGN KEY (id_venda) REFERENCES vendas(id_venda)
  ON DELETE CASCADE,
  FOREIGN KEY (id_livro) REFERENCES livros(id_livro)
  ON DELETE RESTRICT
) DEFAULT CHARSET=utf8mb4;
