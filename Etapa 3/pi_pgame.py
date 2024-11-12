import pygame
import sys
import mysql.connector
import random
from datetime import datetime

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PINK = (255, 105, 180)
DARK_GRAY = (55,58,62)
GRAY = (169, 169, 169)

if len(sys.argv) > 1:
    user_id = int(sys.argv[1])
else:
    user_id = 2  # VALOR PARA TESTES

def get_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="252411",
        database="calendario"
    )

WIDTH, HEIGHT = 1280, 720
FPS = 60

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.gameStateManager = GameStateManager('Tela_inicial')
        self.Agenda = Agenda(self.screen, self.gameStateManager)

        self.Personalizacao = Personalizacao(self.screen, self.gameStateManager)
        self.CriarTarefa = CriarTarefa(self.screen, self.gameStateManager)
        self.VerTarefas = VerTarefas(self.screen, self.gameStateManager)
        self.DeletarTarefas = DeletarTarefas(self.screen, self.gameStateManager)
        self.AlterarTarefas = AlterarTarefas(self.screen, self.gameStateManager)

        self.player_sprite = self.load_player_sprite()
        
        self.Tela_inicial = Tela_inicial(self.screen, self.gameStateManager, self.player_sprite)
        self.Minigame = Minigame(self.screen, self.gameStateManager, self.player_sprite)

        self.states = {
            'Tela_inicial': self.Tela_inicial,
            'Agenda': self.Agenda,
            'Minigame': self.Minigame,
            'Personalizacao': self.Personalizacao,
            'CriarTarefa': self.CriarTarefa,
            'VerTarefas': self.VerTarefas,
            'DeletarTarefas': self.DeletarTarefas,
            'AlterarTarefas': self.AlterarTarefas
        }
    
    def wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = ""

        for word in words:
            if font.size(current_line + word)[0] < max_width:
                current_line += word + ' '
            else:
                lines.append(font.render(current_line, True, BLACK))
                current_line = word + ' '
        if current_line:
            lines.append(font.render(current_line, True, BLACK))
        
        return lines

    def load_player_sprite(self):
        return pygame.image.load(f'sprites/sprite{self.Personalizacao.selected_index}.png')

    def run(self):
        icone = pygame.image.load('sprites/icon1.png')
        pygame.display.set_icon(icone)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if self.gameStateManager.get_state() == "CriarTarefa":
                    #MOLDURA0 selecionada - titulo
                    if event.type == pygame.KEYDOWN and self.CriarTarefa.selected_frame == 0:
                        if event.key == pygame.K_BACKSPACE:
                            self.CriarTarefa.user_text[0] = self.CriarTarefa.user_text[0][:-1]
                        else:
                            if event.unicode.isalnum() or event.unicode == ' ':
                                if len(self.CriarTarefa.user_text[0]) < 32:
                                    self.CriarTarefa.user_text[0] += event.unicode
                    # MOLDURA1 selecionada - data
                    if event.type == pygame.KEYDOWN and self.CriarTarefa.selected_frame == 1:
                        if event.key == pygame.K_BACKSPACE:
                            self.CriarTarefa.user_text[1] = self.CriarTarefa.user_text[1][:-1]
                        elif event.unicode.isdigit():
                            if len(self.CriarTarefa.user_text[1]) == 0 and event.unicode in '0123':
                                self.CriarTarefa.user_text[1] += event.unicode
                            elif len(self.CriarTarefa.user_text[1]) == 1:
                                if self.CriarTarefa.user_text[1][0] == '3' and event.unicode in '01':
                                    self.CriarTarefa.user_text[1] += event.unicode + "/"
                                elif self.CriarTarefa.user_text[1][0] != '3':
                                    self.CriarTarefa.user_text[1] += event.unicode + "/"
                            elif len(self.CriarTarefa.user_text[1]) == 2:
                                self.CriarTarefa.user_text[1] += "/"
                            elif len(self.CriarTarefa.user_text[1]) == 3 and event.unicode in '01':
                                self.CriarTarefa.user_text[1] += event.unicode
                            elif len(self.CriarTarefa.user_text[1]) == 4:
                                if self.CriarTarefa.user_text[1][3] == '1' and event.unicode in '012':
                                    self.CriarTarefa.user_text[1] += event.unicode + "/"
                                elif self.CriarTarefa.user_text[1][3] == '0':
                                    self.CriarTarefa.user_text[1] += event.unicode + "/"
                            elif len(self.CriarTarefa.user_text[1]) == 5:
                                self.CriarTarefa.user_text[1] += "/"
                            elif len(self.CriarTarefa.user_text[1]) in [6, 7, 8, 9]:
                                self.CriarTarefa.user_text[1] += event.unicode
                            if len(self.CriarTarefa.user_text[1]) == 10:
                                day = int(self.CriarTarefa.user_text[1][:2])
                                month = int(self.CriarTarefa.user_text[1][3:5])
                                if month in [4, 6, 9, 11] and day > 30:
                                    self.CriarTarefa.user_text[1] = self.CriarTarefa.user_text[1][:-2]
                                elif month == 2:
                                    year = int(self.CriarTarefa.user_text[1][6:])
                                    if year % 4 == 0 and day > 29:
                                        self.CriarTarefa.user_text[1] = self.CriarTarefa.user_text[1][:-2]
                                    elif day > 28 and year+2 %4 != 0:
                                        self.CriarTarefa.user_text[1] = self.CriarTarefa.user_text[1][:-2]
                    #HORARIO
                    if event.type == pygame.KEYDOWN and self.CriarTarefa.selected_frame == 2:
                        if event.key == pygame.K_BACKSPACE:
                            self.CriarTarefa.user_text[2] = self.CriarTarefa.user_text[2][:-1]
                        elif event.unicode.isdigit():
                            if len(self.CriarTarefa.user_text[2]) == 0 and event.unicode in '012':
                                self.CriarTarefa.user_text[2] += event.unicode
                            elif len(self.CriarTarefa.user_text[2]) == 1:
                                if self.CriarTarefa.user_text[2][0] == '2' and event.unicode in '0123':
                                    self.CriarTarefa.user_text[2] += event.unicode + ":"
                                elif self.CriarTarefa.user_text[2][0] != '2':
                                    self.CriarTarefa.user_text[2] += event.unicode + ":"
                            elif len(self.CriarTarefa.user_text[2]) == 2:
                                self.CriarTarefa.user_text[2] += ":"
                            elif len(self.CriarTarefa.user_text[2]) == 3 and event.unicode in '012345':
                                self.CriarTarefa.user_text[2] += event.unicode
                            elif len(self.CriarTarefa.user_text[2]) == 4:
                                self.CriarTarefa.user_text[2] += event.unicode
                    #MOLDURA3 selecionada - descrição
                    if event.type == pygame.KEYDOWN and self.CriarTarefa.selected_frame == 3:
                        if event.key == pygame.K_BACKSPACE:
                            self.CriarTarefa.user_text[3] = self.CriarTarefa.user_text[3][:-1]
                        else:
                            if event.unicode.isalnum() or event.unicode == ' ':
                                if len(self.CriarTarefa.user_text[3]) < 220:
                                    self.CriarTarefa.user_text[3] += event.unicode

            self.player_sprite = self.load_player_sprite()
            self.Minigame.player_sprite = self.player_sprite
            self.Tela_inicial.player_sprite = self.player_sprite
            
            self.states[self.gameStateManager.get_state()].run()

            pygame.display.update()
            self.clock.tick(FPS)
                

class CriarTarefa:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        self.back_button = pygame.Rect(150 - 64, 600, 175, 75)
        self.concluir_button = pygame.Rect(1100 - 64, 600, 175, 75)
        self.font = pygame.font.Font('PublicPixel.ttf', 18)
        self.user_text = ["", "", "", ""]
        self.selected_frame = None
        self.frame_rects = [
            pygame.Rect(640-400, 200, 800, 75),
            pygame.Rect(640-400, 275, 800, 75),
            pygame.Rect(640-400, 350, 800, 75),
            pygame.Rect(640-400, 425, 800, 150)
        ]

        self.show_confirmation = False

    def wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = ""

        for word in words:
            if font.size(current_line + word)[0] < max_width:
                current_line += word + ' '
            else:
                lines.append(font.render(current_line.strip(), True, BLACK))
                current_line = word + ' '
        if current_line:
            lines.append(font.render(current_line.strip(), True, BLACK))

        return lines

    def criar_evento(self, user_id, title, desc, data, hora):
        usuario_id = user_id
        titulo = title
        descricao = desc
        data_evento = data
        horario = hora
        con = get_db_connection()
        cursor = con.cursor()
        query = 'INSERT INTO eventos (usuario_id, titulo, descricao, data_evento, horario) VALUES (%s, %s, %s, %s, %s)'
        cursor.execute(query, (usuario_id, titulo, descricao, data_evento, horario)) 
        con.commit()
        con.close()
    
    def alterar_evento(self, user_id, title, desc, data, hora, evento_id):
        usuario_id = user_id
        titulo = title
        descricao = desc
        data_evento = data
        horario = hora
        con = get_db_connection()
        cursor = con.cursor()
        query = 'UPDATE eventos SET usuario_id = %s, titulo = %s, descricao = %s, data_evento = %s, horario = %s WHERE id = %s'
        cursor.execute(query, (usuario_id, titulo, descricao, data_evento, horario, evento_id))
        con.commit()
        con.close()


    def format_date(self, date_string):
        if len(date_string) == 10:
            day = date_string[:2]
            month = date_string[3:5]
            year = date_string[6:10]
            formatted_date = f"{year}-{month}-{day}"
            return formatted_date
        return date_string

    def wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = ""

        for word in words:
            if font.size(current_line + word)[0] < max_width:
                current_line += word + ' '
            else:
                lines.append(font.render(current_line, True, BLACK))
                current_line = word + ' '
        if current_line:
            lines.append(font.render(current_line, True, BLACK))
        
        return lines
    
    def draw_back_button(self):
        pygame.draw.rect(self.display, DARK_GRAY, self.back_button)
        text = self.font.render("Voltar", True, WHITE)
        text_rect = text.get_rect(center=self.back_button.center)
        self.display.blit(text, text_rect)

        pygame.draw.rect(self.display, BLACK, pygame.Rect(150 -69, 600-5, 185, 85), 5)

    def draw_concluir_button(self):
        pygame.draw.rect(self.display, DARK_GRAY, self.concluir_button)
        text = self.font.render("Salvar", True, WHITE)
        text_rect = text.get_rect(center=self.concluir_button.center)
        self.display.blit(text, text_rect)

        pygame.draw.rect(self.display, BLACK, pygame.Rect(1100 -69, 600-5, 185, 85), 5)

    def draw_confirmation_dialog(self):
        if self.show_confirmation:
            dialog_width, dialog_height = 400, 200
            dialog_x = (self.display.get_width() - dialog_width) // 2
            dialog_y = (self.display.get_height() - dialog_height) // 2

            pygame.draw.rect(self.display, GRAY, (dialog_x, dialog_y, dialog_width, dialog_height))
            pygame.draw.rect(self.display, BLACK, (dialog_x, dialog_y, dialog_width, dialog_height), 3)

            confirmation_text = self.font.render("Salvar tarefa?", True, BLACK)
            confirm_text = self.font.render("Sim", True, GREEN)
            cancel_text = self.font.render("Não", True, RED)

            confirmation_rect = confirmation_text.get_rect(center=(dialog_x + dialog_width // 2, dialog_y + 50))
            self.display.blit(confirmation_text, confirmation_rect)

            confirm_button_rect = pygame.Rect(dialog_x + 50, dialog_y + 150, 100, 40)
            cancel_button_rect = pygame.Rect(dialog_x + 250, dialog_y + 150, 100, 40)

            self.display.blit(confirm_text, (confirm_button_rect.centerx - confirm_text.get_width() // 2, confirm_button_rect.centery - confirm_text.get_height() // 2))
            self.display.blit(cancel_text, (cancel_button_rect.centerx - cancel_text.get_width() // 2, cancel_button_rect.centery - cancel_text.get_height() // 2))

            return confirm_button_rect, cancel_button_rect
        return None, None

    def draw_text_boxes(self):
        for index, rect in enumerate(self.frame_rects):
            color = DARK_BLUE if self.selected_frame == index else BLACK
            pygame.draw.rect(self.display, color, rect, 4)
            if self.idd == 0:
                if index == 0:
                    texto = "Título:"
                if index == 1:
                    texto = "Data:"
                if index == 2:
                    texto = "Horário:"
                if index == 3:
                    
                    if len(self.user_text[3]) <1:
                        text_surface = self.font.render("Descrição:", True, (20,20,20))
                        text_rect = text_surface.get_rect(center=rect.center)
                        self.display.blit(text_surface, text_rect)
                    else:
                        wrapped_lines = self.wrap_text(self.user_text[index], self.font, rect.width - 10)
                        for i, line in enumerate(wrapped_lines):
                            line_rect = line.get_rect(topleft=(rect.x + 5, rect.y + 5 + i * self.font.get_height()))
                            self.display.blit(line, line_rect)
                else:
                    if len(self.user_text[index])<1:
                        text_surface = self.font.render(texto, True, (20,20,20))
                        text_rect = text_surface.get_rect(center=rect.center)
                        self.display.blit(text_surface, text_rect)
                    else:
                        text_surface = self.font.render(self.user_text[index], True, BLACK)
                        text_rect = text_surface.get_rect(center=rect.center)
                        self.display.blit(text_surface, text_rect)
            elif self.idd > 0:
                if index == 0:
                    texto = self.titulo
                if index == 1:
                    texto = self.data
                if index == 2:
                    texto = self.horario
                if index == 3:
                    if len(self.user_text[3]) <1:
                        wrapped_lines = self.wrap_text(self.descrição, self.font, rect.width - 10)
                        for i, line in enumerate(wrapped_lines):
                            line_rect = line.get_rect(topleft=(rect.x + 5, rect.y + 5 + i * self.font.get_height()))
                            self.display.blit(line, line_rect)
                    else:
                        wrapped_lines = self.wrap_text(self.user_text[index], self.font, rect.width - 10)
                        for i, line in enumerate(wrapped_lines):
                            line_rect = line.get_rect(topleft=(rect.x + 5, rect.y + 5 + i * self.font.get_height()))
                            self.display.blit(line, line_rect)
                else:
                    if len(self.user_text[index])<1:
                        text_surface = self.font.render(texto, True, (20,20,20))
                        text_rect = text_surface.get_rect(center=rect.center)
                        self.display.blit(text_surface, text_rect)
                    else:
                        text_surface = self.font.render(self.user_text[index], True, BLACK)
                        text_rect = text_surface.get_rect(center=rect.center)
                        self.display.blit(text_surface, text_rect)

    def run(self):
        pygame.display.set_caption("Criar Tarefa")
        if self.idd == 0:
            self.background = pygame.image.load('sprites/agenda1.png')
        else:
            self.background = pygame.image.load('sprites/agenda4.png')
        self.display.blit(self.background, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        pygame.draw.rect(self.display, BLACK, pygame.Rect(237, 197, 806,381))
        pygame.draw.rect(self.display, WHITE, pygame.Rect(240, 200, 800,375))
        pygame.draw.rect(self.display, GRAY, pygame.Rect(240, 200, 800,225))
        if self.show_confirmation:
            confirm_button_rect, cancel_button_rect = self.draw_confirmation_dialog()
            if confirm_button_rect.collidepoint(mouse_pos) and mouse_click[0]:
                if self.idd > 0:
                    if self.user_text[0] == "":
                        self.user_text[0] = self.titulo
                    if self.user_text[1] == "":
                        self.user_text[1] = self.data
                    if self.user_text[2] == "":
                        self.user_text[2] = self.horario
                    if self.user_text[3] == "":
                        self.user_text[3] = self.descrição
                    formatted_date = self.format_date(self.user_text[1])
                    self.alterar_evento(user_id, self.user_text[0], self.user_text[3], formatted_date, self.user_text[2],self.idd)
                    self.show_confirmation = False
                    print("Evento alterado com sucesso!")
                    self.user_text[0] = ""
                    self.user_text[1] = ""
                    self.user_text[2] = ""
                    self.user_text[3] = ""
                    self.selected_frame = None
                    self.gameStateManager.set_state('AlterarTarefas')
                    print("Indo para Alterar Tarefa")
                else:
                    formatted_date = self.format_date(self.user_text[1])
                    self.criar_evento(user_id, self.user_text[0], self.user_text[3], formatted_date, self.user_text[2])
                    self.show_confirmation = False
                    print("Evento criado com sucesso!")
                    self.user_text[0] = ""
                    self.user_text[1] = ""
                    self.user_text[2] = ""
                    self.user_text[3] = ""
                    self.selected_frame = None
            elif cancel_button_rect.collidepoint(mouse_pos) and mouse_click[0]:
                self.show_confirmation = False 

        else:
            for index, rect in enumerate(self.frame_rects):
                if rect.collidepoint(mouse_pos):
                    if mouse_click[0]:  
                        self.selected_frame = index
                        print(f"Moldura {index + 1} selecionada.")

            self.draw_text_boxes()
            if self.back_button.collidepoint(mouse_pos) and mouse_click[0]:
                self.gameStateManager.set_state('Agenda')
                self.user_text[0] = ""
                self.user_text[1] = ""
                self.user_text[2] = ""
                self.user_text[3] = ""
                self.selected_frame = None
                print("Indo para agenda")
                
            if self.concluir_button.collidepoint(mouse_pos) and mouse_click[0]:
                self.show_confirmation = True
                print("Tela de confirmação aberta.")
            self.draw_concluir_button()
        self.draw_back_button()



class VerTarefas:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        self.back_button = pygame.Rect(150 - 64, 600, 175, 75)
        self.next_button = pygame.Rect(780 - 64, 600, 175, 75)
        self.previous_button = pygame.Rect(465 - 64, 600, 175, 75)
        self.concluir_button = pygame.Rect(1100 - 64, 600, 175, 75)  
        self.font = pygame.font.Font('PublicPixel.ttf', 18)
        self.font2 = pygame.font.Font('PublicPixel.ttf', 36)
        self.background = pygame.image.load('sprites/agenda2.png')
        self.previous_button_image = pygame.image.load('sprites/seta0.png').convert_alpha()
        self.next_button_image = pygame.image.load('sprites/seta1.png').convert_alpha()
        
        self.eventos = []  
        self.event_index = 0
        self.next_button_pressed = False
        self.previous_button_pressed = False
        self.confirm_button_pressed = False  
        self.show_confirmation = False  
        self.confirmed_event_id = None  

    def fetch_eventos(self):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, titulo, descricao, data_evento, horario FROM eventos WHERE usuario_id = %s ORDER BY data_evento, horario",
            (user_id,))
        eventos = cursor.fetchall()
        cursor.close()
        connection.close()
        return eventos

    def exibir_evento(self, evento):
        evento_id, titulo, descricao, data_evento, horario = evento

        data_formatada = data_evento.strftime('%d/%m/%Y')
        dia = data_evento.strftime('%A')
        
        if dia == "Sunday":
            dia_da_semana = "Domingo"
        elif dia == "Monday":
            dia_da_semana = "Segunda-feira"
        elif dia == "Tuesday":
            dia_da_semana = "Terça-feira"
        elif dia == "Wednesday":
            dia_da_semana = "Quarta-feira"
        elif dia == "Thursday":
            dia_da_semana = "Quinta-feira"
        elif dia == "Friday":
            dia_da_semana = "Sexta-feira"
        elif dia == "Saturday":
            dia_da_semana = "Sábado"

        if horario:
            horas = horario.seconds // 3600
            minutos = (horario.seconds // 60) % 60
            horario_formatado = f"{horas:02}:{minutos:02}"
        else:
            horario_formatado = "Sem horário"

        titulo_font = pygame.font.Font('PublicPixel.ttf', 24)
        horario_font = pygame.font.Font('PublicPixel.ttf', 28)
        data_font = pygame.font.Font('PublicPixel.ttf', 20)
        descricao_font = pygame.font.Font('PublicPixel.ttf', 20)

        titulo_text = titulo_font.render(f"{titulo}", True, BLACK)
        horario_text = horario_font.render(f"{horario_formatado}", True, BLACK)
        data_text = data_font.render(f"{dia_da_semana}, {data_formatada}", True, BLACK)

        y_offset = 150
        frame_width, frame_height = 800, 150
        frame_x = (self.display.get_width() - frame_width) // 2
        frame_y = y_offset - 20

        pygame.draw.rect(self.display, GRAY, (frame_x, frame_y, frame_width, frame_height))

        self.display.blit(titulo_text, (frame_x + 10, y_offset))
        self.display.blit(horario_text, (frame_x + 10, y_offset + 40))
        self.display.blit(data_text, (frame_x + 10, y_offset + 80))

        descricao_text = descricao if descricao else "Adicione uma anotação"
        descricao_rendered = self.wrap_text(descricao_text, descricao_font, frame_width)

        descricao_y_offset = y_offset + 130
        pygame.draw.rect(self.display, WHITE, (frame_x, descricao_y_offset, frame_width, 300))
        for idx, line in enumerate(descricao_rendered):
            self.display.blit(line, (frame_x + 10, descricao_y_offset + 10 + idx * 20))

    def wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = ""

        for word in words:
            if font.size(current_line + word)[0] < max_width:
                current_line += word + ' '
            else:
                lines.append(font.render(current_line, True, BLACK))
                current_line = word + ' '
        if current_line:
            lines.append(font.render(current_line, True, BLACK))
        
        return lines

    def draw_buttons(self):
        pygame.draw.rect(self.display, DARK_GRAY, self.back_button)
        back_text = self.font.render("Voltar", True, WHITE)
        back_text_rect = back_text.get_rect(center=self.back_button.center)
        self.display.blit(back_text, back_text_rect)
        

        self.display.blit(self.previous_button_image, self.previous_button.topleft)
        previous_text = self.font.render("Anterior", True, WHITE)
        previous_text_rect = previous_text.get_rect(center=(self.previous_button.centerx, self.previous_button.centery))
        self.display.blit(previous_text, previous_text_rect)
        

        self.display.blit(self.next_button_image, self.next_button.topleft)
        next_text = self.font.render("Próximo", True, WHITE)
        next_text_rect = next_text.get_rect(center=(self.next_button.centerx, self.next_button.centery))
        self.display.blit(next_text, next_text_rect)

        pygame.draw.rect(self.display, GREEN, self.concluir_button)
        concluir_text = self.font.render("Concluir", True, WHITE)
        concluir_text_rect = concluir_text.get_rect(center=self.concluir_button.center)
        self.display.blit(concluir_text, concluir_text_rect)

        pygame.draw.rect(self.display, BLACK, pygame.Rect(150 -69, 600-5, 185, 85), 5)
        pygame.draw.rect(self.display, BLACK, pygame.Rect(465 -69, 600-5, 185, 85), 5)
        pygame.draw.rect(self.display, BLACK, pygame.Rect(780 -69, 600-5, 185, 85), 5)
        pygame.draw.rect(self.display, BLACK, pygame.Rect(1100 -69, 600-5, 185, 85), 5)

    def draw_confirmation_dialog(self):
        if self.show_confirmation:
            dialog_width, dialog_height = 400, 200
            dialog_x = (self.display.get_width() - dialog_width) // 2
            dialog_y = (self.display.get_height() - dialog_height) // 2

            pygame.draw.rect(self.display, GRAY, (dialog_x, dialog_y, dialog_width, dialog_height))
            pygame.draw.rect(self.display, BLACK, (dialog_x, dialog_y, dialog_width, dialog_height), 3)

            confirmation_text = self.font.render("Concluir tarefa?", True, BLACK)
            confirm_text = self.font.render("Sim", True, GREEN)
            cancel_text = self.font.render("Não", True, RED)

            confirmation_rect = confirmation_text.get_rect(center=(dialog_x + dialog_width // 2, dialog_y + 50))
            self.display.blit(confirmation_text, confirmation_rect)

            confirm_button_rect = pygame.Rect(dialog_x + 50, dialog_y + 150, 100, 40)
            cancel_button_rect = pygame.Rect(dialog_x + 250, dialog_y + 150, 100, 40)

            self.display.blit(confirm_text, (confirm_button_rect.centerx - confirm_text.get_width() // 2, confirm_button_rect.centery - confirm_text.get_height() // 2))
            self.display.blit(cancel_text, (cancel_button_rect.centerx - cancel_text.get_width() // 2, cancel_button_rect.centery - cancel_text.get_height() // 2))

            return confirm_button_rect, cancel_button_rect
        return None, None

    def concluir_evento(self, evento_id):
        self.event_index = 0
        connection = get_db_connection()
        cursor = connection.cursor()
        
        cursor.execute("UPDATE usuarios SET pontuação = pontuação + 1 WHERE id = %s", (user_id,))
        
        cursor.execute("DELETE FROM eventos WHERE id = %s", (evento_id,))
        
        connection.commit()
        cursor.close()
        connection.close()

    def run(self):
        pygame.display.set_caption("Ver Tarefas")
        self.eventos = self.fetch_eventos()  
        self.display.blit(self.background, (0, 0))
        
        self.draw_buttons()

        if self.eventos:
            pygame.draw.rect(self.display, BLACK, pygame.Rect(235, 125, 810,460))
            evento = self.eventos[self.event_index]
            self.exibir_evento(evento)  
            pygame.draw.rect(self.display, BLACK, pygame.Rect(235, 125, 810,160), 5)
            
        else:
            no_event_text = self.font2.render("Nenhuma tarefa disponível.", True, BLACK)
            self.display.blit(no_event_text, (190, 320))

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        if self.back_button.collidepoint(mouse_pos) and mouse_click[0]:
            self.gameStateManager.set_state('Agenda')
            print("Indo para agenda")

        if self.eventos:  
            if self.next_button.collidepoint(mouse_pos):
                if mouse_click[0] and not self.next_button_pressed:
                    self.next_button_pressed = True
                    self.event_index = (self.event_index + 1) % len(self.eventos)
                    print("Próximo evento")
                elif not mouse_click[0]:
                    self.next_button_pressed = False

            if self.previous_button.collidepoint(mouse_pos):
                if mouse_click[0] and not self.previous_button_pressed:
                    self.previous_button_pressed = True
                    self.event_index = (self.event_index - 1) % len(self.eventos)
                    print("Evento anterior")
                elif not mouse_click[0]:
                    self.previous_button_pressed = False

            if self.concluir_button.collidepoint(mouse_pos) and mouse_click[0]:
                if not self.confirm_button_pressed:  
                    self.show_confirmation = True
                    self.confirmed_event_id = evento[0]  
                    self.confirm_button_pressed = True  
                    print("Solicitação de confirmação para concluir evento")
            elif not mouse_click[0]:  
                self.confirm_button_pressed = False

        if self.show_confirmation:
            confirm_button, cancel_button = self.draw_confirmation_dialog()

            if confirm_button.collidepoint(mouse_pos) and mouse_click[0]:
                self.concluir_evento(self.confirmed_event_id)  
                self.show_confirmation = False  
                print("Evento concluído e pontuação do usuário aumentada.")
            elif cancel_button.collidepoint(mouse_pos) and mouse_click[0]:
                self.show_confirmation = False  
                print("Cancelando a conclusão do evento.")


class DeletarTarefas:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        self.back_button = pygame.Rect(150 - 64, 600, 175, 75)
        self.next_button = pygame.Rect(780 - 64, 600, 175, 75)
        self.previous_button = pygame.Rect(465 - 64, 600, 175, 75)
        self.concluir_button = pygame.Rect(1100 - 64, 600, 175, 75)  
        self.font = pygame.font.Font('PublicPixel.ttf', 18)
        self.font2 = pygame.font.Font('PublicPixel.ttf', 36)
        self.background = pygame.image.load('sprites/agenda3.png')
        self.previous_button_image = pygame.image.load('sprites/seta0.png').convert_alpha()
        self.next_button_image = pygame.image.load('sprites/seta1.png').convert_alpha()
        
        self.eventos = []  
        self.event_index = 0
        self.next_button_pressed = False
        self.previous_button_pressed = False
        self.confirm_button_pressed = False  
        self.show_confirmation = False 
        self.confirmed_event_id = None  

    def fetch_eventos(self):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, titulo, descricao, data_evento, horario FROM eventos WHERE usuario_id = %s ORDER BY data_evento, horario",
            (user_id,))
        eventos = cursor.fetchall()
        cursor.close()
        connection.close()
        return eventos

    def exibir_evento(self, evento):
        evento_id, titulo, descricao, data_evento, horario = evento

        data_formatada = data_evento.strftime('%d/%m/%Y')
        dia = data_evento.strftime('%A')
        
        if dia == "Sunday":
            dia_da_semana = "Domingo"
        elif dia == "Monday":
            dia_da_semana = "Segunda-feira"
        elif dia == "Tuesday":
            dia_da_semana = "Terça-feira"
        elif dia == "Wednesday":
            dia_da_semana = "Quarta-feira"
        elif dia == "Thursday":
            dia_da_semana = "Quinta-feira"
        elif dia == "Friday":
            dia_da_semana = "Sexta-feira"
        elif dia == "Saturday":
            dia_da_semana = "Sábado"

        if horario:
            horas = horario.seconds // 3600
            minutos = (horario.seconds // 60) % 60
            horario_formatado = f"{horas:02}:{minutos:02}"
        else:
            horario_formatado = "Sem horário"

        titulo_font = pygame.font.Font('PublicPixel.ttf', 24)
        horario_font = pygame.font.Font('PublicPixel.ttf', 28)
        data_font = pygame.font.Font('PublicPixel.ttf', 20)
        descricao_font = pygame.font.Font('PublicPixel.ttf', 20)

        titulo_text = titulo_font.render(f"{titulo}", True, BLACK)
        horario_text = horario_font.render(f"{horario_formatado}", True, BLACK)
        data_text = data_font.render(f"{dia_da_semana}, {data_formatada}", True, BLACK)

        y_offset = 150
        frame_width, frame_height = 800, 150
        frame_x = (self.display.get_width() - frame_width) // 2
        frame_y = y_offset - 20

        pygame.draw.rect(self.display, GRAY, (frame_x, frame_y, frame_width, frame_height))

        self.display.blit(titulo_text, (frame_x + 10, y_offset))
        self.display.blit(horario_text, (frame_x + 10, y_offset + 40))
        self.display.blit(data_text, (frame_x + 10, y_offset + 80))

        descricao_text = descricao if descricao else "Adicione uma anotação em Alterar tarefas"
        descricao_rendered = self.wrap_text(descricao_text, descricao_font, frame_width)

        descricao_y_offset = y_offset + 130
        pygame.draw.rect(self.display, WHITE, (frame_x, descricao_y_offset, frame_width, 300))
        for idx, line in enumerate(descricao_rendered):
            self.display.blit(line, (frame_x + 10, descricao_y_offset + 10 + idx * 20))

    def wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = ""

        for word in words:
            if font.size(current_line + word)[0] < max_width:
                current_line += word + ' '
            else:
                lines.append(font.render(current_line, True, BLACK))
                current_line = word + ' '
        if current_line:
            lines.append(font.render(current_line, True, BLACK))
        
        return lines

    def draw_buttons(self):
        # Botão "Voltar"
        pygame.draw.rect(self.display, DARK_GRAY, self.back_button)
        back_text = self.font.render("Voltar", True, WHITE)
        back_text_rect = back_text.get_rect(center=self.back_button.center)
        self.display.blit(back_text, back_text_rect)

        self.display.blit(self.previous_button_image, self.previous_button.topleft)
        previous_text = self.font.render("Anterior", True, WHITE)
        previous_text_rect = previous_text.get_rect(center=(self.previous_button.centerx, self.previous_button.centery))
        self.display.blit(previous_text, previous_text_rect)

        self.display.blit(self.next_button_image, self.next_button.topleft)
        next_text = self.font.render("Próximo", True, WHITE)
        next_text_rect = next_text.get_rect(center=(self.next_button.centerx, self.next_button.centery))
        self.display.blit(next_text, next_text_rect)

        pygame.draw.rect(self.display, RED, self.concluir_button)
        concluir_text = self.font.render("Deletar", True, WHITE)
        concluir_text_rect = concluir_text.get_rect(center=self.concluir_button.center)
        self.display.blit(concluir_text, concluir_text_rect)

        pygame.draw.rect(self.display, BLACK, pygame.Rect(150 -69, 600-5, 185, 85), 5)
        pygame.draw.rect(self.display, BLACK, pygame.Rect(465 -69, 600-5, 185, 85), 5)
        pygame.draw.rect(self.display, BLACK, pygame.Rect(780 -69, 600-5, 185, 85), 5)
        pygame.draw.rect(self.display, BLACK, pygame.Rect(1100 -69, 600-5, 185, 85), 5)

    def draw_confirmation_dialog(self):
        if self.show_confirmation:
            dialog_width, dialog_height = 400, 200
            dialog_x = (self.display.get_width() - dialog_width) // 2
            dialog_y = (self.display.get_height() - dialog_height) // 2

            pygame.draw.rect(self.display, GRAY, (dialog_x, dialog_y, dialog_width, dialog_height))
            pygame.draw.rect(self.display, BLACK, (dialog_x, dialog_y, dialog_width, dialog_height), 3)

            confirmation_text = self.font.render("Deletar tarefa?", True, BLACK)
            confirm_text = self.font.render("Sim", True, GREEN)
            cancel_text = self.font.render("Não", True, RED)

            confirmation_rect = confirmation_text.get_rect(center=(dialog_x + dialog_width // 2, dialog_y + 50))
            self.display.blit(confirmation_text, confirmation_rect)

            confirm_button_rect = pygame.Rect(dialog_x + 50, dialog_y + 150, 100, 40)
            cancel_button_rect = pygame.Rect(dialog_x + 250, dialog_y + 150, 100, 40)

            self.display.blit(confirm_text, (confirm_button_rect.centerx - confirm_text.get_width() // 2, confirm_button_rect.centery - confirm_text.get_height() // 2))
            self.display.blit(cancel_text, (cancel_button_rect.centerx - cancel_text.get_width() // 2, cancel_button_rect.centery - cancel_text.get_height() // 2))

            return confirm_button_rect, cancel_button_rect
        return None, None

    def concluir_evento(self, evento_id):
        self.event_index = 0
        connection = get_db_connection()
        cursor = connection.cursor()
        
        cursor.execute("DELETE FROM eventos WHERE id = %s", (evento_id,))
        
        connection.commit()
        cursor.close()
        connection.close()

    def run(self):
        pygame.display.set_caption("Deletar Tarefa")
        self.display.blit(self.background, (0, 0))
        self.eventos = self.fetch_eventos()
        
        self.draw_buttons()

        if self.eventos:
            evento = self.eventos[self.event_index]
            pygame.draw.rect(self.display, BLACK, pygame.Rect(235, 125, 810,460))
            self.exibir_evento(evento)  
            pygame.draw.rect(self.display, BLACK, pygame.Rect(235, 125, 810,160), 5)
        else:
            no_event_text = self.font2.render("Nenhuma tarefa disponível.", True, BLACK)
            self.display.blit(no_event_text, (190, 320))

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        if self.back_button.collidepoint(mouse_pos) and mouse_click[0]:
            self.gameStateManager.set_state('Agenda')
            print("Indo para agenda")

        if self.eventos:  
            if self.next_button.collidepoint(mouse_pos):
                if mouse_click[0] and not self.next_button_pressed:
                    self.next_button_pressed = True
                    self.event_index = (self.event_index + 1) % len(self.eventos)
                    print("Próximo evento")
                elif not mouse_click[0]:
                    self.next_button_pressed = False

            if self.previous_button.collidepoint(mouse_pos):
                if mouse_click[0] and not self.previous_button_pressed:
                    self.previous_button_pressed = True
                    self.event_index = (self.event_index - 1) % len(self.eventos)
                    print("Evento anterior")
                elif not mouse_click[0]:
                    self.previous_button_pressed = False

            if self.concluir_button.collidepoint(mouse_pos) and mouse_click[0]:
                if not self.confirm_button_pressed:  
                    self.show_confirmation = True
                    self.confirmed_event_id = evento[0] 
                    self.confirm_button_pressed = True 
                    print("Solicitação de confirmação para deletar evento")
            elif not mouse_click[0]:
                self.confirm_button_pressed = False

        if self.show_confirmation:
            confirm_button, cancel_button = self.draw_confirmation_dialog()

            if confirm_button.collidepoint(mouse_pos) and mouse_click[0]:
                self.concluir_evento(self.confirmed_event_id) 
                self.show_confirmation = False
                self.event_index = 0
                print("Evento excluído.")
            elif cancel_button.collidepoint(mouse_pos) and mouse_click[0]:
                self.show_confirmation = False 
                print("Cancelando a exclusão do evento.")

class AlterarTarefas:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        self.back_button = pygame.Rect(150 - 64, 600, 175, 75)
        self.next_button = pygame.Rect(780 - 64, 600, 175, 75)
        self.previous_button = pygame.Rect(465 - 64, 600, 175, 75)
        self.concluir_button = pygame.Rect(1100 - 64, 600, 175, 75)  
        self.font = pygame.font.Font('PublicPixel.ttf', 18)
        self.font2 = pygame.font.Font('PublicPixel.ttf', 36)
        self.background = pygame.image.load('sprites/agenda4.png')
        self.previous_button_image = pygame.image.load('sprites/seta0.png').convert_alpha()
        self.next_button_image = pygame.image.load('sprites/seta1.png').convert_alpha()
        
        self.eventos = []  
        self.event_index = 0
        self.next_button_pressed = False
        self.previous_button_pressed = False
        self.confirm_button_pressed = False  
        self.show_confirmation = False  
        self.confirmed_event_id = None  

    def fetch_eventos(self):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, titulo, descricao, data_evento, horario FROM eventos WHERE usuario_id = %s ORDER BY data_evento, horario",
            (user_id,))
        eventos = cursor.fetchall()
        cursor.close()
        connection.close()
        return eventos

    def exibir_evento(self, evento):
        evento_id, titulo, descricao, data_evento, horario = evento

        data_formatada = data_evento.strftime('%d/%m/%Y')
        dia = data_evento.strftime('%A')
        
        if dia == "Sunday":
            dia_da_semana = "Domingo"
        elif dia == "Monday":
            dia_da_semana = "Segunda-feira"
        elif dia == "Tuesday":
            dia_da_semana = "Terça-feira"
        elif dia == "Wednesday":
            dia_da_semana = "Quarta-feira"
        elif dia == "Thursday":
            dia_da_semana = "Quinta-feira"
        elif dia == "Friday":
            dia_da_semana = "Sexta-feira"
        elif dia == "Saturday":
            dia_da_semana = "Sábado"

        if horario:
            horas = horario.seconds // 3600
            minutos = (horario.seconds // 60) % 60
            horario_formatado = f"{horas:02}:{minutos:02}"
        else:
            horario_formatado = "Sem horário"

        titulo_font = pygame.font.Font('PublicPixel.ttf', 24)
        horario_font = pygame.font.Font('PublicPixel.ttf', 28)
        data_font = pygame.font.Font('PublicPixel.ttf', 20)
        descricao_font = pygame.font.Font('PublicPixel.ttf', 20)

        titulo_text = titulo_font.render(f"{titulo}", True, BLACK)
        horario_text = horario_font.render(f"{horario_formatado}", True, BLACK)
        data_text = data_font.render(f"{dia_da_semana}, {data_formatada}", True, BLACK)

        y_offset = 150
        frame_width, frame_height = 800, 150
        frame_x = (self.display.get_width() - frame_width) // 2
        frame_y = y_offset - 20

        pygame.draw.rect(self.display, GRAY, (frame_x, frame_y, frame_width, frame_height))

        self.display.blit(titulo_text, (frame_x + 10, y_offset))
        self.display.blit(horario_text, (frame_x + 10, y_offset + 40))
        self.display.blit(data_text, (frame_x + 10, y_offset + 80))

        descricao_text = descricao if descricao else "Adicione uma anotação"
        descricao_rendered = self.wrap_text(descricao_text, descricao_font, frame_width)

        descricao_y_offset = y_offset + 130
        pygame.draw.rect(self.display, WHITE, (frame_x, descricao_y_offset, frame_width, 300))
        for idx, line in enumerate(descricao_rendered):
            self.display.blit(line, (frame_x + 10, descricao_y_offset + 10 + idx * 20))

    def wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = ""

        for word in words:
            if font.size(current_line + word)[0] < max_width:
                current_line += word + ' '
            else:
                lines.append(font.render(current_line, True, BLACK))
                current_line = word + ' '
        if current_line:
            lines.append(font.render(current_line, True, BLACK))
        
        return lines

    def draw_buttons(self):
        pygame.draw.rect(self.display, DARK_GRAY, self.back_button)
        back_text = self.font.render("Voltar", True, WHITE)
        back_text_rect = back_text.get_rect(center=self.back_button.center)
        self.display.blit(back_text, back_text_rect)
        

        self.display.blit(self.previous_button_image, self.previous_button.topleft)
        previous_text = self.font.render("Anterior", True, WHITE)
        previous_text_rect = previous_text.get_rect(center=(self.previous_button.centerx, self.previous_button.centery))
        self.display.blit(previous_text, previous_text_rect)
        

        self.display.blit(self.next_button_image, self.next_button.topleft)
        next_text = self.font.render("Próximo", True, WHITE)
        next_text_rect = next_text.get_rect(center=(self.next_button.centerx, self.next_button.centery))
        self.display.blit(next_text, next_text_rect)

        pygame.draw.rect(self.display, DARK_BLUE, self.concluir_button)
        concluir_text = self.font.render("Editar", True, WHITE)
        concluir_text_rect = concluir_text.get_rect(center=self.concluir_button.center)
        self.display.blit(concluir_text, concluir_text_rect)

        pygame.draw.rect(self.display, BLACK, pygame.Rect(150 -69, 600-5, 185, 85), 5)
        pygame.draw.rect(self.display, BLACK, pygame.Rect(465 -69, 600-5, 185, 85), 5)
        pygame.draw.rect(self.display, BLACK, pygame.Rect(780 -69, 600-5, 185, 85), 5)
        pygame.draw.rect(self.display, BLACK, pygame.Rect(1100 -69, 600-5, 185, 85), 5)

    def draw_confirmation_dialog(self):
        if self.show_confirmation:
            dialog_width, dialog_height = 400, 200
            dialog_x = (self.display.get_width() - dialog_width) // 2
            dialog_y = (self.display.get_height() - dialog_height) // 2

            pygame.draw.rect(self.display, GRAY, (dialog_x, dialog_y, dialog_width, dialog_height))
            pygame.draw.rect(self.display, BLACK, (dialog_x, dialog_y, dialog_width, dialog_height), 3)

            confirmation_text = self.font.render("Editar tarefa?", True, BLACK)
            confirm_text = self.font.render("Sim", True, GREEN)
            cancel_text = self.font.render("Não", True, RED)

            confirmation_rect = confirmation_text.get_rect(center=(dialog_x + dialog_width // 2, dialog_y + 50))
            self.display.blit(confirmation_text, confirmation_rect)

            confirm_button_rect = pygame.Rect(dialog_x + 50, dialog_y + 150, 100, 40)
            cancel_button_rect = pygame.Rect(dialog_x + 250, dialog_y + 150, 100, 40)

            self.display.blit(confirm_text, (confirm_button_rect.centerx - confirm_text.get_width() // 2, confirm_button_rect.centery - confirm_text.get_height() // 2))
            self.display.blit(cancel_text, (cancel_button_rect.centerx - cancel_text.get_width() // 2, cancel_button_rect.centery - cancel_text.get_height() // 2))

            return confirm_button_rect, cancel_button_rect
        return None, None

    def concluir_evento(self, evento_id,title, date, hour, desc):
        if hour:
            horas = hour.seconds // 3600
            minutos = (hour.seconds // 60) % 60
            horario = f"{horas:02}:{minutos:02}"
        else:
            horario = "Sem horário"
        if date:
            data = date.strftime('%d/%m/%Y')
        self.gameStateManager.set_state_criar('CriarTarefa',idd = evento_id, titulo = title, data = data, horario = horario, descrição = desc)
        print("Indo para criar tarefa")

    def run(self):
        pygame.display.set_caption("Editar Tarefas")
        self.eventos = self.fetch_eventos()  
        self.display.blit(self.background, (0, 0))
        
        self.draw_buttons()

        if self.eventos:
            pygame.draw.rect(self.display, BLACK, pygame.Rect(235, 125, 810,460))
            evento = self.eventos[self.event_index]
            self.exibir_evento(evento)  
            pygame.draw.rect(self.display, BLACK, pygame.Rect(235, 125, 810,160), 5)
        else:
            no_event_text = self.font2.render("Nenhuma tarefa disponível.", True, BLACK)
            self.display.blit(no_event_text, (190, 320))

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        if self.back_button.collidepoint(mouse_pos) and mouse_click[0]:
            self.gameStateManager.set_state('Agenda')
            print("Indo para agenda")

        if self.eventos:  
            if self.next_button.collidepoint(mouse_pos):
                if mouse_click[0] and not self.next_button_pressed:
                    self.next_button_pressed = True
                    self.event_index = (self.event_index + 1) % len(self.eventos)
                    print("Próximo evento")
                elif not mouse_click[0]:
                    self.next_button_pressed = False

            if self.previous_button.collidepoint(mouse_pos):
                if mouse_click[0] and not self.previous_button_pressed:
                    self.previous_button_pressed = True
                    self.event_index = (self.event_index - 1) % len(self.eventos)
                    print("Evento anterior")
                elif not mouse_click[0]:
                    self.previous_button_pressed = False

            if self.concluir_button.collidepoint(mouse_pos) and mouse_click[0]:
                if not self.confirm_button_pressed:  
                    self.show_confirmation = True
                    self.confirmed_event_id = evento[0]  
                    self.confirmed_title_id = evento[1]
                    self.confirmed_descr_id = evento[2]
                    self.confirmed_hour_id = evento[4]
                    self.confirmed_date_id = evento[3]
                    self.confirm_button_pressed = True  
                    print("Solicitação de confirmação para concluir evento")
            elif not mouse_click[0]:  
                self.confirm_button_pressed = False

        if self.show_confirmation:
            confirm_button, cancel_button = self.draw_confirmation_dialog()

            if confirm_button.collidepoint(mouse_pos) and mouse_click[0]:
                self.concluir_evento(self.confirmed_event_id,self.confirmed_title_id,self.confirmed_date_id,self.confirmed_hour_id,self.confirmed_descr_id)  
                self.show_confirmation = False  
                print("Evento concluído e pontuação do usuário aumentada.")
            elif cancel_button.collidepoint(mouse_pos) and mouse_click[0]:
                self.show_confirmation = False  
                print("Cancelando a conclusão do evento.")


class Agenda:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        
        self.background = pygame.image.load('sprites/agenda0.png')
        self.icons = [
            pygame.image.load('sprites/icon0.png'),
            pygame.image.load('sprites/icon1.png'),
            pygame.image.load('sprites/icon2.png'),
            pygame.image.load('sprites/icon3.png')
        ]
        
        self.icon_positions = [
            (200-75, 475),
            (500-75, 475),
            (800-75, 475),
            (1100-75, 475)
            
        ]
        
        self.button_labels = ["Criar Tarefa", "Ver Tarefas", "Editar Tarefa","Deletar Tarefa"]
        self.font = pygame.font.Font('PublicPixel.ttf', 14)

    def draw_buttons(self):
        for i, (icon, position) in enumerate(zip(self.icons, self.icon_positions)):
            self.display.blit(icon, position)
            if i == 0:
                color = (230,230,230)
            if i == 1:
                color = (230,230,230)
            if i == 2:
                color = (230,230,230)
            if i == 3:
                color = (230,230,230)
            text = self.font.render(self.button_labels[i], True, color)
            text_rect = text.get_rect(center=(position[0] + icon.get_width() // 2, position[1] + icon.get_height() // 0.9))
            self.display.blit(text, text_rect)

    def run(self):
        pygame.display.set_caption("Agenda")
        self.display.blit(self.background, (0, 0))

        self.draw_buttons()
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.gameStateManager.set_state('Tela_inicial')
            print("Indo para tela inicial")

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        for i, (icon, position) in enumerate(zip(self.icons, self.icon_positions)):
            icon_rect = icon.get_rect(topleft=position)
            if icon_rect.collidepoint(mouse_pos) and mouse_click[0]: 
                if i == 0:
                    self.gameStateManager.set_state_criar('CriarTarefa',idd = 0,titulo="",data="",horario="",descrição="")
                    print("Indo para criar tarefa")
                elif i == 1:
                    self.gameStateManager.set_state('VerTarefas')
                    print("Indo para ver tarefas")
                elif i == 3:
                    self.gameStateManager.set_state('DeletarTarefas')
                    print("Indo para deletar tarefas")
                elif i == 2:
                    self.gameStateManager.set_state('AlterarTarefas')
                    print("Indo para alterar tarefas")


class Minigame: 
    def __init__(self, display, gameStateManager, player_sprite):
        self.display = display
        self.gameStateManager = gameStateManager
        x = random.randint(1,2)
        if x == 1:
            self.color = WHITE
        elif x == 2:
            self.color = DARK_GREEN
        elif x == 3:
            self.color = DARK_BLUE
        self.background_image = pygame.image.load(f'sprites/backmini{x}.png').convert()  
        self.bird_x = 100
        self.bird_y = HEIGHT // 2
        self.bird_velocity = 0
        self.gravity = 0.4
        self.flap_strength = -10
        
        self.pipes = []
        self.pipe_gap = 300
        self.pipe_frequency = 1900
        self.last_pipe = pygame.time.get_ticks()
        self.score = 0
        self.high_score = self.load_high_score()  
        self.font = pygame.font.Font('PublicPixel.ttf', 30)
        self.game_started = False 
        self.can_flap = True  

    def load_high_score(self):
        try:
            with open('high_score.txt', 'r') as file:
                return int(file.read().strip())
        except (FileNotFoundError, ValueError):
            return 0 

    def save_high_score(self):
        with open('high_score.txt', 'w') as file:
            file.write(str(self.high_score))

    def draw_bird(self):
        self.display.blit(self.player_sprite, (self.bird_x, self.bird_y))

    def draw_pipes(self):
        for pipe in self.pipes:
            pygame.draw.rect(self.display, self.color, (pipe['x'], 0, 75, pipe['top']))  
            pygame.draw.rect(self.display, self.color, (pipe['x'], pipe['bottom'], 75, HEIGHT))  

    def check_collisions(self):
        bird_rect = pygame.Rect(self.bird_x, self.bird_y, 75, 125)
        for pipe in self.pipes:
            top_pipe_rect = pygame.Rect(pipe['x'], 0, 50, pipe['top'])
            bottom_pipe_rect = pygame.Rect(pipe['x'], pipe['bottom'], 50, HEIGHT)
            if bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect):
                return True
        return False

    def update_pipes(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_pipe > self.pipe_frequency:
            pipe_height = random.randint(50, HEIGHT - self.pipe_gap - 50)
            self.pipes.append({
                'x': WIDTH,
                'top': pipe_height,
                'bottom': pipe_height + self.pipe_gap,
                'passed': False  
            })
            self.last_pipe = current_time

        for pipe in self.pipes:
            pipe['x'] -= 5  
            if not pipe['passed'] and pipe['x'] + 75 < self.bird_x:
                self.score += 1
                pipe['passed'] = True  

        self.pipes = [pipe for pipe in self.pipes if pipe['x'] > -50]

    def reset_game(self):
        if self.score > self.high_score:  # Atualiza o recorde se necessário
            self.high_score = self.score
            self.save_high_score()  # Salva o novo recorde

        self.bird_y = HEIGHT // 2
        self.bird_velocity = 0
        self.pipes = []
        self.score = 0
        self.last_pipe = pygame.time.get_ticks()
        self.game_started = False  
        self.can_flap = True
        
    def run(self):
        pygame.display.set_caption("Joguinho")
        self.display.blit(self.background_image, (0, 0)) 
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if not self.game_started:
                self.game_started = True  
            elif self.can_flap:  
                self.bird_velocity = self.flap_strength  
                self.can_flap = False
        if keys[pygame.K_SPACE] == 0:  
            self.can_flap = True

        if self.game_started:
            self.bird_velocity += self.gravity
            self.bird_y += self.bird_velocity
            
            if self.bird_y > HEIGHT - 50 or self.check_collisions():
                self.reset_game()
                self.gameStateManager.set_state('Minigame')

            self.update_pipes()
            self.draw_bird()
            self.draw_pipes()

            score_text = self.font.render(f"Pontos: {self.score}", True, BLACK)
            self.display.blit(score_text, (10, 10))
        else:
            start_text = self.font.render("Pressione Espaço para Começar", True, BLACK)
            start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.display.blit(start_text, start_rect)

            high_score_text = self.font.render(f"Recorde: {self.high_score}", True, WHITE)
            high_score_rect = high_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40)) 
            self.display.blit(high_score_text, high_score_rect)

            back_text = self.font.render("ESC para voltar", True, BLACK)
            back_rect = back_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
            self.display.blit(back_text, back_rect)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                self.gameStateManager.set_state('Tela_inicial')
                print("Indo para tela inicial")

        pygame.display.update()


class Personalizacao:
    def __init__(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
        self.selected_index = 0 
        self.font = pygame.font.Font('PublicPixel.ttf', 36) 
    def draw_title(self):
        titulo = "Selecione seu personagem!"
        rendered_text = self.font.render(titulo, True, BLACK)  
        text_rect = rendered_text.get_rect(center=(WIDTH // 2, 200)) 
        self.display.blit(rendered_text, text_rect)
    def get_pontuacao(self):
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            query = "SELECT pontuação FROM usuarios WHERE id = %s"
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return 0
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return 0
        finally:
            cursor.close()
            connection.close()
    def get_selected_index(self):
        print(self.selected_index)
        return self.selected_index
    
    def run(self):
        pygame.display.set_caption("Customização")
        self.display.fill(WHITE)
        self.draw_title()
        pontuacao = self.get_pontuacao()

        square_size = 150
        small_square_size = 50
        square_positions = [
            (240 - 75, 300),
            (440 - 75, 300),
            (640 - 75, 300),
            (840 - 75, 300),
            (1040 - 75, 300),
        ]
        colors = [BLACK] * 5
        unlock_colors = [LIGHT_BLUE] * 5
        small_square_colors = [pygame.image.load(f'sprites/sprite{i}.png') for i in range(5)] 

        if pontuacao >= 0:
            colors[0] = unlock_colors[0]
        if pontuacao >= 3:
            colors[1] = unlock_colors[1]
        if pontuacao >= 6:
            colors[2] = unlock_colors[2]
        if pontuacao >= 9:
            colors[3] = unlock_colors[3]
        if pontuacao >= 12:
            colors[4] = unlock_colors[4]

        for index, pos in enumerate(square_positions):
            pygame.draw.rect(self.display, colors[index], (pos[0], pos[1], square_size, square_size))

            if self.selected_index == index:
                pygame.draw.rect(self.display, (255, 255, 0), (pos[0], pos[1], square_size, square_size), 5)

            small_square_pos = (pos[0] + (square_size - small_square_size) // 2, pos[1] + (square_size - small_square_size) // 2)
            small_square_color = small_square_colors[index]
            self.display.blit(small_square_color, small_square_pos) 

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        for index, pos in enumerate(square_positions):
            if colors[index] == unlock_colors[index] and (pos[0] <= mouse_pos[0] <= pos[0] + square_size) and (pos[1] <= mouse_pos[1] <= pos[1] + square_size):
                if mouse_click[0]:
                    self.selected_index = index
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.gameStateManager.set_state('Tela_inicial')
            print("Indo para tela inicial")


class Tela_inicial:
    def __init__(self, display, gameStateManager, player_sprite):
        self.display = display
        self.gameStateManager = gameStateManager
        self.player_width = 100  
        self.player_height = 150 
        self.player_x = 100
        self.player_y = HEIGHT - self.player_height - 50
        self.player_speed = 5

        self.door_width = 150 
        self.door_height = 250 
        self.doors = [
            pygame.Rect(300, HEIGHT - self.door_height - 100, self.door_width, self.door_height), 
            pygame.Rect(600, HEIGHT - self.door_height - 100, self.door_width, self.door_height), 
            pygame.Rect(900, HEIGHT - self.door_height - 100, self.door_width, self.door_height)
        ]

        self.ground_height = 100
        self.ground_rect = pygame.Rect(0, HEIGHT - self.ground_height, WIDTH, self.ground_height)

        self.background_image = pygame.image.load('sprites/backg1.png').convert()  # Use convert() para otimizar
        
        self.door_images = [
            pygame.image.load('sprites/porta0.png').convert_alpha(),
            pygame.image.load('sprites/porta1.png').convert_alpha(),
            pygame.image.load('sprites/porta2.png').convert_alpha()
        ]

        self.door_images = [pygame.transform.scale(image, (self.door_width, self.door_height)) for image in self.door_images]

    def draw_player_and_doors(self):
        for i, door in enumerate(self.doors):
            self.display.blit(self.door_images[i], door.topleft)


        player_sprite_scaled = pygame.transform.scale(self.player_sprite, (self.player_width, self.player_height))
        self.display.blit(player_sprite_scaled, (self.player_x, self.player_y))

        return pygame.Rect(self.player_x, self.player_y, self.player_width, self.player_height)

    def run(self):
        pygame.display.set_caption("Tela inicial")
        self.display.blit(self.background_image, (0, 0))  # Posiciona a imagem no canto superior esquerdo
        pygame.draw.rect(self.display, GRAY, self.ground_rect)
        player_rect = self.draw_player_and_doors()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player_x -= self.player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player_x += self.player_speed

        self.player_x = max(0, min(self.player_x, WIDTH - self.player_width))

        for i, door in enumerate(self.doors):
            if player_rect.colliderect(door) and (keys[pygame.K_w] or keys[pygame.K_UP]):
                if i == 0:
                    self.gameStateManager.set_state('Agenda')
                    print("Indo para agenda")
                elif i == 1:
                    self.gameStateManager.set_state('Minigame')
                    print("Indo para minigame")
                elif i == 2:
                    self.gameStateManager.set_state('Personalizacao')
                    print("Indo para personalização")
        pygame.display.update()






class GameStateManager:
    def __init__(self, initial_state):
        self.state = initial_state

    def set_state(self, new_state):
        self.state = new_state

    def set_state_criar(self, new_state, idd,titulo,data,horario,descrição):
        self.state = new_state
        CriarTarefa.idd = idd
        CriarTarefa.titulo = titulo
        CriarTarefa.data = data
        CriarTarefa.horario = horario
        CriarTarefa.descrição = descrição

    def get_state(self):
        return self.state

if __name__ == "__main__":
    game = Game()
    game.run()
