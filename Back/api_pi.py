from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

def get_db_connection():
    try:
        return mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="252411",
            database="calendario"
        )
    except Error as e:
        print(f"Error: {e}")
        raise

@app.errorhandler(400)
def bad_request_error(error):
    return jsonify({'message': 'Bad Request', 'error': str(error)}), 400

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'message': 'Not Found', 'error': str(error)}), 404

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'message': 'Internal Server Error', 'error': str(error)}), 500

#USUARIOS
@app.route('/usuarios', methods=['POST'])
def create_usuario():
    try:
        data = request.get_json()
        email = data.get('email')
        usuario = data.get('login')
        senha = data.get('senha')
        con = get_db_connection()
        cursor = con.cursor()
        query = 'INSERT INTO usuarios (email, login, senha) VALUES (%s, %s, %s)'
        cursor.execute(query, (email, usuario, senha))
        con.commit()
        con.close()
        return jsonify({'message': f'Usuário {usuario} inserido com sucesso!'}), 201
    except Error as e:
        return jsonify({'message': 'Database Error', 'error': str(e)}), 500
    except Exception as e:
        return jsonify({'message': 'Unexpected Error', 'error': str(e)}), 500

@app.route('/usuarios', methods=['GET'])
def read_usuarios():
    try:
        con = get_db_connection()
        cursor = con.cursor()
        query = 'SELECT * FROM usuarios'
        cursor.execute(query)
        resultados = cursor.fetchall()
        con.close()
        return jsonify(resultados), 200
    except Error as e:
        return jsonify({'message': 'Database Error', 'error': str(e)}), 500
    except Exception as e:
        return jsonify({'message': 'Unexpected Error', 'error': str(e)}), 500

@app.route('/usuarios/<int:id>', methods=['PUT'])
def update_usuario(id):
    try:
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
    except Error as e:
        return jsonify({'message': 'Database Error', 'error': str(e)}), 500
    except Exception as e:
        return jsonify({'message': 'Unexpected Error', 'error': str(e)}), 500

@app.route('/usuarios/<int:id>', methods=['DELETE'])
def delete_usuario(id):
    try:
        con = get_db_connection()
        cursor = con.cursor()
        query = 'DELETE FROM usuarios WHERE id = %s'
        cursor.execute(query, (id,))
        con.commit()
        con.close()
        return jsonify({'message': f'Usuário com ID {id} removido com sucesso!'}), 200
    except Error as e:
        return jsonify({'message': 'Database Error', 'error': str(e)}), 500
    except Exception as e:
        return jsonify({'message': 'Unexpected Error', 'error': str(e)}), 500

#EVENTOS
@app.route('/eventos', methods=['POST'])
def create_evento():
    try:
        data = request.get_json()
        usuario_id = data.get('usuario_id')
        titulo = data.get('titulo')
        descricao = data.get('descricao')
        data_evento = data.get('data_evento')
        con = get_db_connection()
        cursor = con.cursor()
        query = 'INSERT INTO eventos (usuario_id, titulo, descricao, data_evento) VALUES (%s, %s, %s, %s)'
        cursor.execute(query, (usuario_id, titulo, descricao, data_evento))
        con.commit()
        con.close()
        return jsonify({'message': f'Evento {titulo} inserido com sucesso!'}), 201
    except Error as e:
        return jsonify({'message': 'Database Error', 'error': str(e)}), 500
    except Exception as e:
        return jsonify({'message': 'Unexpected Error', 'error': str(e)}), 500

@app.route('/eventos', methods=['GET'])
def read_eventos():
    try:
        con = get_db_connection()
        cursor = con.cursor()
        query = 'SELECT * FROM eventos'
        cursor.execute(query)
        resultados = cursor.fetchall()
        con.close()
        return jsonify(resultados), 200
    except Error as e:
        return jsonify({'message': 'Database Error', 'error': str(e)}), 500
    except Exception as e:
        return jsonify({'message': 'Unexpected Error', 'error': str(e)}), 500

@app.route('/eventos/<int:id>', methods=['PUT'])
def update_evento(id):
    try:
        data = request.get_json()
        new_usuario_id = data.get('usuario_id')
        new_titulo = data.get('titulo')
        new_descricao = data.get('descricao')
        new_data_evento = data.get('data_evento')
        con = get_db_connection()
        cursor = con.cursor()
        query = 'UPDATE eventos SET usuario_id = %s, titulo = %s, descricao = %s, data_evento = %s WHERE id = %s'
        cursor.execute(query, (new_usuario_id, new_titulo, new_descricao, new_data_evento, id))
        con.commit()
        con.close()
        return jsonify({'message': f'Evento com ID {id} atualizado com sucesso!'}), 200
    except Error as e:
        return jsonify({'message': 'Database Error', 'error': str(e)}), 500
    except Exception as e:
        return jsonify({'message': 'Unexpected Error', 'error': str(e)}), 500

@app.route('/eventos/<int:id>', methods=['DELETE'])
def delete_evento(id):
    try:
        con = get_db_connection()
        cursor = con.cursor()
        query = 'DELETE FROM eventos WHERE id = %s'
        cursor.execute(query, (id,))
        con.commit()
        con.close()
        return jsonify({'message': f'Evento com ID {id} removido com sucesso!'}), 200
    except Error as e:
        return jsonify({'message': 'Database Error', 'error': str(e)}), 500
    except Exception as e:
        return jsonify({'message': 'Unexpected Error', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
