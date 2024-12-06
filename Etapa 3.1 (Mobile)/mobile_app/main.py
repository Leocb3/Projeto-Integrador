from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
import sqlite3

# Tela de Login
class LoginScreen(Screen):
    def login(self):
        email = self.ids.email.text
        senha = self.ids.senha.text
        conexao = sqlite3.connect("mobile_app.db")
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email = ? AND senha = ?", (email, senha))
        user = cursor.fetchone()
        conexao.close()

        if user:
            self.manager.current = "dashboard"
        else:
            self.ids.login_error.text = "Email ou senha incorretos!"

# Tela de Registro
class RegisterScreen(Screen):
    def register(self):
        email = self.ids.email.text
        senha = self.ids.senha.text
        conexao = sqlite3.connect("mobile_app.db")
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO usuarios (email, senha) VALUES (?, ?)", (email, senha))
        conexao.commit()
        conexao.close()
        self.manager.current = "login"

# Tela Principal
class DashboardScreen(Screen):
    pass

# Tela de Visualizar Tarefas
class VerTarefasScreen(Screen):
    def on_pre_enter(self):
        self.carregar_tarefas()

    def carregar_tarefas(self):
        self.ids.tarefas_container.clear_widgets()
        conexao = sqlite3.connect("mobile_app.db")
        cursor = conexao.cursor()
        cursor.execute("SELECT id, titulo, data FROM tarefas")
        tarefas = cursor.fetchall()
        conexao.close()

        for tarefa in tarefas:
            self.ids.tarefas_container.add_widget(
                Label(text=f"{tarefa[1]} - {tarefa[2]}", size_hint_y=None, height=40)
            )

# Tela para Criar Tarefas
class CriarTarefaScreen(Screen):
    def salvar_tarefa(self):
        titulo = self.ids.titulo.text
        data = self.ids.data.text
        conexao = sqlite3.connect("mobile_app.db")
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO tarefas (titulo, data) VALUES (?, ?)", (titulo, data))
        conexao.commit()
        conexao.close()
        self.manager.current = "ver_tarefas"

# Função para criar banco de dados
def criar_banco():
    conexao = sqlite3.connect("mobile_app.db")
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY,
            email TEXT,
            senha TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY,
            titulo TEXT,
            data TEXT
        )
    """)
    conexao.close()

# Aplicativo principal
class TaskApp(App):
    def build(self):
        criar_banco()
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(RegisterScreen(name="register"))
        sm.add_widget(DashboardScreen(name="dashboard"))
        sm.add_widget(VerTarefasScreen(name="ver_tarefas"))
        sm.add_widget(CriarTarefaScreen(name="criar_tarefa"))
        sm.current = "login"
        return sm

if __name__ == "__main__":
    TaskApp().run()
