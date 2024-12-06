import sqlite3

# Função para criar o banco de dados e as tabelas
def criar_banco():
    conexao = sqlite3.connect("mobile_app.db")
    cursor = conexao.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tarefas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        data TEXT NOT NULL,
        hora TEXT NOT NULL,
        descricao TEXT,
        status INTEGER DEFAULT 0
    )
    """)
    conexao.commit()
    conexao.close()

# Função para adicionar tarefas
def adicionar_tarefa(titulo, data, hora, descricao):
    conexao = sqlite3.connect("mobile_app.db")
    cursor = conexao.cursor()
    cursor.execute("""
    INSERT INTO tarefas (titulo, data, hora, descricao) VALUES (?, ?, ?, ?)
    """, (titulo, data, hora, descricao))
    conexao.commit()
    conexao.close()

# Função para excluir tarefas
def deletar_tarefa(tarefa_id):
    conexao = sqlite3.connect("mobile_app.db")
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM tarefas WHERE id = ?", (tarefa_id,))
    conexao.commit()
    conexao.close()

# Inicializar o banco de dados
criar_banco()
