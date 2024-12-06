from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import os

# Configuração da aplicação Flask
app = Flask(__name__)

# Diretório base e caminho do banco de dados
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'instance', 'users.db')

# Configuração do banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializando o SQLAlchemy
db = SQLAlchemy(app)

# Modelo de Usuário
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Criar o banco de dados, se não existir
with app.app_context():
    if not os.path.exists(db_path):
        print(f"Criando banco de dados: {db_path}")
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        db.create_all()
    else:
        print(f"Banco de dados já existe: {db_path}")

# Rota para exibir a página de login
@app.route("/")
def login_page():
    return render_template("login.html")

# Rota para Registro
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")

    if not email or not username or not password:
        return jsonify({"message": "Por favor, preencha todos os campos."}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "E-mail já registrado!"}), 400

    new_user = User(email=email, username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Usuário registrado com sucesso!"}), 201

# Rota para Login
@app.route("/login", methods=["POST"])
def login():
    data = request.form
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Por favor, preencha todos os campos."}), 400

    user = User.query.filter_by(email=email).first()
    if not user or user.password != password:
        return jsonify({"message": "E-mail ou senha inválidos."}), 401

    return jsonify({"message": "Login bem-sucedido!"}), 200

# Inicialização do servidor
if __name__ == "__main__":
    app.run(debug=True)
