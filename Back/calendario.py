import mysql.connector

conexao = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="252411",
    database="calendario"
)

def criar_db():
    cursor = conexao.cursor()
    query = '''CREATE DATABASE calendario'''
    cursor.execute(query)
    conexao.commit()
    print("Database criada!")
    conexao.close()

def criar_tabela_usuarios():
    cursor = conexao.cursor()
    query ='''
    CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    login VARCHAR(50) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);'''
    cursor.execute(query)
    conexao.commit()
    print("Tabela criada!")
    conexao.close()

def criar_tabela_eventos():
    cursor = conexao.cursor()    
    query ='''
CREATE TABLE eventos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    titulo VARCHAR(255) NOT NULL,
    descricao TEXT,
    data_evento DATE NOT NULL,
    dia_da_semana VARCHAR(10) GENERATED ALWAYS AS (DAYNAME(data_evento)) STORED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id));'''
    cursor.execute(query)
    conexao.commit()
    print("Tabela criada!")
    conexao.close()

def insert_usuario(usuario,senha):
    cursor = conexao.cursor()
    query =f'''INSERT INTO usuarios (login, senha) VALUES ('{usuario}', '{senha}');'''
    cursor.execute(query)
    conexao.commit()
    print(f"Usuário {usuario} inserido na tabela")
    conexao.close()

def select_usuarios():
    cursor = conexao.cursor()
    query = '''SELECT * FROM usuarios;'''
    cursor.execute(query)
    resultados = cursor.fetchall()
    print('ID    LOGIN    SENHA   DATA_CRIAÇÃO')
    for linha in resultados:
        print(linha)
    conexao.commit()
    conexao.close()

def update_usuarios(id,new_login,new_senha):
    cursor = conexao.cursor()
    query = f'''UPDATE usuarios SET login= '{new_login}',senha='{new_senha}' WHERE id = {id};'''
    cursor.execute(query)
    conexao.commit()
    print(f'Atualizado com sucesso!\nNovo login: {new_login}')
    conexao.close()

def delete_usuarios(id):
    cursor = conexao.cursor()
    query = f'''DELETE FROM usuarios WHERE id =  {id};'''
    cursor.execute(query)
    conexao.commit()
    print(f'Usuário com ID {id} removido com sucesso!')
    conexao.close()

#EVENTOS
def insert_evento(usuario_id,titulo,descricao,data):
    cursor = conexao.cursor()
    query =f'''INSERT INTO eventos (usuario_id, titulo, descricao, data_evento) VALUES ('{usuario_id}', '{titulo}','{descricao}','{data}');'''
    cursor.execute(query)
    conexao.commit()
    print(f"Evento {titulo} inserido na tabela")
    conexao.close()

def select_eventos():
    cursor = conexao.cursor()
    query = '''SELECT * FROM eventos;'''
    cursor.execute(query)
    resultados = cursor.fetchall()
    print('ID    Usuario    Titulo      Descrição       Data_evento     Dia_semana    DATA_CRIAÇÃO')
    for linha in resultados:
        print(linha)
    conexao.commit()
    conexao.close()

def update_eventos(id,new_usuario_id,new_titulo, new_descricao, new_data_evento):
    cursor = conexao.cursor()
    query = f'''UPDATE eventos SET usuario_id= '{new_usuario_id}',titulo='{new_titulo}',descricao= '{new_descricao}',data_evento='{new_data_evento}' WHERE id = '{id}';'''
    cursor.execute(query)
    conexao.commit()
    print(f'Atualizado com sucesso!\nNovo evento: {new_titulo}')
    conexao.close()

def delete_eventos(id):
    cursor = conexao.cursor()
    query = f'''DELETE FROM eventos WHERE id = {id};'''
    cursor.execute(query)
    conexao.commit()
    print(f'Evento com ID {id} removido com sucesso!')
    conexao.close()

#MAIN
if __name__ == '__main__':
    conexao.close()
