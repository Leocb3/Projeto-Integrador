from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import subprocess

app = Flask(__name__)
CORS(app)

def get_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="252411",
        database="calendario"
    )

@app.route('/usuarios/login', methods=['POST'])
def login_usuario():
    data = request.get_json()
    email = data.get('email')
    senha = data.get('senha')

    # Imprime os dados recebidos para depuração
    print(f"Email recebido: {email}, Senha recebida: {senha}")

    con = get_db_connection()
    cursor = con.cursor()
    query = 'SELECT id FROM usuarios WHERE email = %s AND senha = %s'
    cursor.execute(query, (email, senha))
    usuario = cursor.fetchone()
    con.close()
    
    if usuario:
        # Login bem-sucedido, iniciando o Pygame
        subprocess.Popen(['python', 'pi_pgame.py', str(usuario[0])])  # Passa o ID do usuário como argumento
        
        return jsonify({'message': 'Login bem-sucedido! Pygame iniciado.', 'usuario_id': usuario[0]}), 200
    else:
        return jsonify({'message': 'Credenciais inválidas.'}), 401

@app.route('/usuarios/criar', methods=['POST'])
def create_usuario():
    data = request.get_json()
    email = data.get('email')
    usuario = data.get('usuario')
    senha = data.get('senha')
    con = get_db_connection()
    cursor = con.cursor()
    query = 'INSERT INTO usuarios (email, login, senha) VALUES (%s, %s, %s)'
    cursor.execute(query, (email, usuario, senha))
    con.commit()
    con.close()
    return jsonify({'message': f'Usuário {usuario} inserido com sucesso!'}), 201

@app.route('/usuarios', methods=['GET'])
def read_usuarios():
    con = get_db_connection()
    cursor = con.cursor()
    query = 'SELECT * FROM usuarios'
    cursor.execute(query)
    resultados = cursor.fetchall()
    con.close()
    return jsonify(resultados), 200

@app.route('/usuarios/<int:id>', methods=['PUT'])
def update_usuario(id):
    data = request.get_json()
    new_email = data.get('email')
    new_login = data.get('login')
    new_senha = data.get('senha')
    con = get_db_connection()
    cursor = con.cursor()
    query = 'UPDATE usuarios SET email = %s, login = %s, senha = %s WHERE id = %s'
    cursor.execute(query, (new_email, new_login, new_senha, id))
    con.commit()
    con.close()
    return jsonify({'message': f'Usuário com ID {id} atualizado com sucesso!'}), 200

@app.route('/usuarios/<int:id>', methods=['DELETE'])
def delete_usuario(id):
    con = get_db_connection()
    cursor = con.cursor()
    query = 'DELETE FROM usuarios WHERE id = %s'
    cursor.execute(query, (id,))
    con.commit()
    con.close()
    return jsonify({'message': f'Usuário com ID {id} removido com sucesso!'}), 200

@app.route('/eventos/criar', methods=['POST'])
def create_evento():
    data = request.get_json()
    usuario_id = data.get('usuario_id')
    titulo = data.get('titulo')
    descricao = data.get('descricao')
    data_evento = data.get('data_evento')
    horario = data.get('horario')
    con = get_db_connection()
    cursor = con.cursor()
    query = 'INSERT INTO eventos (usuario_id, titulo, descricao, data_evento, horario) VALUES (%s, %s, %s, %s, %s)'
    cursor.execute(query, (usuario_id, titulo, descricao, data_evento, horario)) 
    con.commit()
    con.close()
    return jsonify({'message': f'Evento criado com sucesso!'}), 201


@app.route('/eventos', methods=['GET'])
def read_eventos():
    con = get_db_connection()
    cursor = con.cursor()
    query = 'SELECT id, usuario_id, titulo, descricao, data_evento, HOUR(horario) AS hora, MINUTE(horario) AS minuto FROM eventos'
    cursor.execute(query)
    resultados = cursor.fetchall()
    con.close()
    
    eventos_formatados = []
    for evento in resultados:
        id_evento, usuario_id, titulo, descricao, data_evento, hora, minuto = evento
        horario_formatado = f"{hora:02}:{minuto:02}"  # Formato hh:mm
        eventos_formatados.append((id_evento, usuario_id, titulo, descricao, data_evento, horario_formatado))

    return jsonify(eventos_formatados), 200


@app.route('/eventos/<int:usuario_id>', methods=['GET'])
def read_evento(usuario_id):
    con = get_db_connection()
    cursor = con.cursor()
    query = 'SELECT * FROM eventos WHERE usuario_id = %s'
    cursor.execute(query, (usuario_id,))
    resultado = cursor.fetchone()
    con.close()
    
    if resultado:
        return jsonify(resultado), 200
    else:
        return jsonify({'message': 'Evento não encontrado.'}), 404

@app.route('/eventos/<int:id>', methods=['PUT'])
def update_evento(id):
    data = request.get_json()
    new_usuario_id = data.get('usuario_id')
    new_titulo = data.get('titulo')
    new_descricao = data.get('descricao')
    new_data_evento = data.get('data_evento')
    new_horario = data.get('horario')  
    con = get_db_connection()
    cursor = con.cursor()
    query = 'UPDATE eventos SET usuario_id = %s, titulo = %s, descricao = %s, data_evento = %s, horario = %s WHERE id = %s'
    cursor.execute(query, (new_usuario_id, new_titulo, new_descricao, new_data_evento, new_horario, id))  # Atualiza com o novo horário
    con.commit()
    con.close()
    return jsonify({'message': f'Evento com ID {id} atualizado com sucesso!'}), 200


@app.route('/eventos/<int:id>', methods=['DELETE'])
def delete_evento(id):
    con = get_db_connection()
    cursor = con.cursor()
    query = 'DELETE FROM eventos WHERE id = %s'
    cursor.execute(query, (id,))
    con.commit()
    con.close()
    return jsonify({'message': f'Evento com ID {id} removido com sucesso!'}), 200

@app.route('/eventos/concluir/<int:id>', methods=['DELETE'])
def concluir_evento(id):
    con = get_db_connection()
    cursor = con.cursor()
    
    cursor.execute('SELECT usuario_id FROM eventos WHERE id = %s', (id,))
    usuario = cursor.fetchone()
    
    if usuario:
        usuario_id = usuario[0]

        cursor.execute('DELETE FROM eventos WHERE id = %s', (id,))
        
        cursor.execute('UPDATE usuarios SET pontuação = pontuação + 1 WHERE id = %s', (usuario_id,))
        
        con.commit()
        con.close()
        return jsonify({'message': 'Evento concluído e pontuação do usuário atualizada com sucesso!'}), 200
    else:
        con.close()
        return jsonify({'message': 'Evento não encontrado.'}), 404



if __name__ == '__main__':
    app.run(debug=True)
