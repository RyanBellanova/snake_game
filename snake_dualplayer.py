import pygame
import sys
import random
import json
import os
from datetime import datetime

CELL_SIZE = 20
GRID_WIDTH = 40
GRID_HEIGHT = 40
WINDOW_WIDTH = CELL_SIZE * GRID_WIDTH
WINDOW_HEIGHT = CELL_SIZE * GRID_HEIGHT

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
GRAY = (128, 128, 128)
ORANGE = (255, 165, 0)

pygame.init()
font = pygame.font.SysFont(None, 28)
big_font = pygame.font.SysFont(None, 50)
small_font = pygame.font.SysFont(None, 20)
clock = pygame.time.Clock()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Snake Dual Player - Login System")

# Dateipfade
USERS_FILE = "users.json"
HIGHSCORES_FILE = "highscores.json"

# Sprachdaten (erweitert)
languages = {
    "de": {
        "select_language": "Sprache wählen",
        "german": "1: Deutsch",
        "italian": "2: Italienisch",
        "english": "3: Englisch",
        "login_screen": "LOGIN",
        "username_prompt": "Benutzername eingeben:",
        "password_prompt": "Passwort eingeben:",
        "login_button": "ENTER: Einloggen",
        "register_button": "R: Registrieren",
        "quit_button": "ESC: Beenden",
        "highscore_button": "H: Highscores",
        "login_success": "Erfolgreich eingeloggt!",
        "login_failed": "Falscher Benutzername oder Passwort!",
        "register_success": "Erfolgreich registriert!",
        "user_exists": "Benutzername bereits vergeben!",
        "player_mode": "Spielmodus wählen",
        "single": "3: Einzelspieler",
        "dual": "4: Zweispieler",
        "timer_prompt": "Timer aktivieren?",
        "with_timer": "5: Mit Timer",
        "without_timer": "6: Ohne Timer",
        "speed_select": "Geschwindigkeit wählen",
        "slow": "1: Langsam",
        "medium": "2: Mittel",
        "fast": "3: Schnell",
        "set_timer": "Timer: {} Sekunden",
        "timer_instructions": "Benutze PFEIL-OBEN/PFEIL-UNTEN zum Einstellen, Enter zum Bestätigen",
        "score_single": "Punkte: {}",
        "score_dual": "P1: {}   P2: {}",
        "time_left": "   Zeit: {}s",
        "speed_indicator": "Geschwindigkeit: {}",
        "collision_dual": "Beide Spieler verloren! Kollision!",
        "collision_single": "Spiel verloren! Kollision!",
        "time_up_single": "Zeit abgelaufen!",
        "time_up_dual_win1": "Spieler 1 gewinnt!",
        "time_up_dual_win2": "Spieler 2 gewinnt!",
        "time_up_dual_draw": "Unentschieden!",
        "made_by": "Gemacht von Ryan Bellanova ©",
        "wall_penalty": "Wand berührt! -1 Punkt",
        "highscores": "HIGHSCORES",
        "no_scores": "Keine Highscores vorhanden",
        "logged_in_as": "Angemeldet als: {}",
        "final_score": "Endpunktestand: {}",
        "new_highscore": "NEUER HIGHSCORE!",
        "press_space": "LEERTASTE: Neues Spiel",
        "press_esc": "ESC: Zum Hauptmenü",
        "rank": "Rang",
        "player": "Spieler",
        "score": "Punkte",
        "date": "Datum",
        "mode": "Modus",
        "back_to_menu": "LEERTASTE: Zurück zum Menü"
    },
    "it": {
        "select_language": "Seleziona lingua",
        "german": "1: Tedesco",
        "italian": "2: Italiano",
        "english": "3: Inglese",
        "login_screen": "LOGIN",
        "username_prompt": "Inserisci nome utente:",
        "password_prompt": "Inserisci password:",
        "login_button": "ENTER: Accedi",
        "register_button": "R: Registrati",
        "quit_button": "ESC: Esci",
        "highscore_button": "H: Punteggi",
        "login_success": "Accesso riuscito!",
        "login_failed": "Nome utente o password errati!",
        "register_success": "Registrazione riuscita!",
        "user_exists": "Nome utente già esistente!",
        "player_mode": "Seleziona modalità",
        "single": "3: Giocatore singolo",
        "dual": "4: Due giocatori",
        "timer_prompt": "Attivare timer?",
        "with_timer": "5: Con timer",
        "without_timer": "6: Senza timer",
        "speed_select": "Seleziona velocità",
        "slow": "1: Lento",
        "medium": "2: Medio",
        "fast": "3: Veloce",
        "set_timer": "Timer: {} secondi",
        "timer_instructions": "Usa FRECCIA-SU/FRECCIA-GIU per impostare, Invio per confermare",
        "score_single": "Punteggio: {}",
        "score_dual": "P1: {}   P2: {}",
        "time_left": "   Tempo: {}s",
        "speed_indicator": "Velocità: {}",
        "collision_dual": "Entrambi i giocatori persi! Collisione!",
        "collision_single": "Gioco perso! Collisione!",
        "time_up_single": "Tempo scaduto!",
        "time_up_dual_win1": "Giocatore 1 vince!",
        "time_up_dual_win2": "Giocatore 2 vince!",
        "time_up_dual_draw": "Pareggio!",
        "made_by": "Realizzato da Ryan Bellanova ©",
        "wall_penalty": "Muro toccato! -1 punto",
        "highscores": "PUNTEGGI",
        "no_scores": "Nessun punteggio disponibile",
        "logged_in_as": "Connesso come: {}",
        "final_score": "Punteggio finale: {}",
        "new_highscore": "NUOVO RECORD!",
        "press_space": "SPAZIO: Nuova partita",
        "press_esc": "ESC: Menu principale",
        "rank": "Pos.",
        "player": "Giocatore",
        "score": "Punti",
        "date": "Data",
        "mode": "Modalità",
        "back_to_menu": "SPAZIO: Torna al menu"
    },
    "en": {
        "select_language": "Select Language",
        "german": "1: German",
        "italian": "2: Italian",
        "english": "3: English",
        "login_screen": "LOGIN",
        "username_prompt": "Enter username:",
        "password_prompt": "Enter password:",
        "login_button": "ENTER: Login",
        "register_button": "R: Register",
        "quit_button": "ESC: Quit",
        "highscore_button": "H: Highscores",
        "login_success": "Login successful!",
        "login_failed": "Wrong username or password!",
        "register_success": "Registration successful!",
        "user_exists": "Username already exists!",
        "player_mode": "Select Player Mode",
        "single": "3: Single Player",
        "dual": "4: Two Players",
        "timer_prompt": "Enable Timer?",
        "with_timer": "5: With Timer",
        "without_timer": "6: Without Timer",
        "speed_select": "Select Game Speed",
        "slow": "1: Slow",
        "medium": "2: Medium",
        "fast": "3: Fast",
        "set_timer": "Timer: {} seconds",
        "timer_instructions": "Use UP/DOWN ARROW to set, Enter to confirm",
        "score_single": "Score: {}",
        "score_dual": "P1: {}   P2: {}",
        "time_left": "   Time: {}s",
        "speed_indicator": "Speed: {}",
        "collision_dual": "Both players lost! Collision!",
        "collision_single": "Game over! Collision!",
        "time_up_single": "Time's up!",
        "time_up_dual_win1": "Player 1 wins!",
        "time_up_dual_win2": "Player 2 wins!",
        "time_up_dual_draw": "It's a draw!",
        "made_by": "Made by Ryan Bellanova ©",
        "wall_penalty": "Wall hit! -1 point",
        "highscores": "HIGHSCORES",
        "no_scores": "No highscores available",
        "logged_in_as": "Logged in as: {}",
        "final_score": "Final Score: {}",
        "new_highscore": "NEW HIGHSCORE!",
        "press_space": "SPACE: New Game",
        "press_esc": "ESC: Main Menu",
        "rank": "Rank",
        "player": "Player",
        "score": "Score",
        "date": "Date",
        "mode": "Mode",
        "back_to_menu": "SPACE: Back to Menu"
    }
}

class UserManager:
    def __init__(self):
        self.users = self.load_users()
        
    def load_users(self):
        try:
            if os.path.exists(USERS_FILE):
                with open(USERS_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except:
            return {}
    
    def save_users(self):
        try:
            with open(USERS_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.users, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def register_user(self, username, password):
        if username in self.users:
            return False
        self.users[username] = password
        self.save_users()
        return True
    
    def login_user(self, username, password):
        return username in self.users and self.users[username] == password

class HighscoreManager:
    def __init__(self):
        self.highscores = self.load_highscores()
    
    def load_highscores(self):
        try:
            if os.path.exists(HIGHSCORES_FILE):
                with open(HIGHSCORES_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except:
            return []
    
    def save_highscores(self):
        try:
            with open(HIGHSCORES_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.highscores, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def add_score(self, username, score, mode, speed):
        entry = {
            "username": username,
            "score": score,
            "mode": mode,
            "speed": speed,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        self.highscores.append(entry)
        self.highscores.sort(key=lambda x: x["score"], reverse=True)
        self.highscores = self.highscores[:20]  # Top 20 behalten
        self.save_highscores()
    
    def is_highscore(self, score):
        return len(self.highscores) < 20 or score > self.highscores[-1]["score"]
    
    def get_user_rank(self, username):
        for i, entry in enumerate(self.highscores):
            if entry["username"] == username:
                return i + 1
        return None

class Snake:
    def __init__(self, color, pos, direction):
        self.color = color
        self.body = [pos]
        self.direction = direction
        self.score = 0
        self.start_pos = pos
        self.start_direction = direction

    def move(self):
        x, y = self.body[0]
        dx, dy = self.direction
        new_pos = (x + dx, y + dy)
        self.body.insert(0, new_pos)
        self.body.pop()

    def grow(self):
        self.body.append(self.body[-1])
        self.score += 1
        
    def reset(self):
        self.body = [self.start_pos]
        self.direction = self.start_direction
        self.score = max(0, self.score - 1)

def draw_text_centered(lines, lang_data, y_offset=0):
    window.fill(BLACK)
    y = WINDOW_HEIGHT // 2 - len(lines) * 20 + y_offset
    for line in lines:
        text = font.render(line, True, WHITE)
        window.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, y))
        y += 40
    copyright = small_font.render(lang_data["made_by"], True, GRAY)
    window.blit(copyright, (10, WINDOW_HEIGHT - 25))
    pygame.display.flip()

def get_text_input(prompt, lang_data, is_password=False):
    input_text = ""
    cursor_visible = True
    cursor_timer = 0
    
    while True:
        clock.tick(60)
        cursor_timer += 1
        if cursor_timer >= 30:
            cursor_visible = not cursor_visible
            cursor_timer = 0
        
        window.fill(BLACK)
        
        # Titel
        title = big_font.render(lang_data["login_screen"], True, WHITE)
        window.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 150))
        
        # Prompt
        prompt_text = font.render(prompt, True, WHITE)
        window.blit(prompt_text, (WINDOW_WIDTH // 2 - prompt_text.get_width() // 2, 250))
        
        # Input field
        display_text = "*" * len(input_text) if is_password else input_text
        input_surface = font.render(display_text, True, YELLOW)
        
        # Input box
        input_rect = pygame.Rect(WINDOW_WIDTH // 2 - 150, 300, 300, 40)
        pygame.draw.rect(window, WHITE, input_rect, 2)
        window.blit(input_surface, (input_rect.x + 5, input_rect.y + 8))
        
        # Cursor
        if cursor_visible:
            cursor_x = input_rect.x + 5 + input_surface.get_width()
            pygame.draw.line(window, YELLOW, (cursor_x, input_rect.y + 5), (cursor_x, input_rect.y + 35), 2)
        
        # Copyright
        copyright = small_font.render(lang_data["made_by"], True, GRAY)
        window.blit(copyright, (10, WINDOW_HEIGHT - 25))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return input_text
                elif event.key == pygame.K_ESCAPE:
                    return None
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if len(input_text) < 20 and event.unicode.isprintable():
                        input_text += event.unicode

def login_screen(lang_data, user_manager):
    message = ""
    message_color = WHITE
    message_timer = 0
    
    while True:
        clock.tick(60)
        
        if message_timer > 0:
            message_timer -= 1
        else:
            message = ""
        
        window.fill(BLACK)
        
        # Titel
        title = big_font.render(lang_data["login_screen"], True, WHITE)
        window.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 150))
        
        # Menü-Optionen
        options = [
            lang_data["login_button"],
            lang_data["register_button"],
            lang_data["highscore_button"],
            lang_data["quit_button"]
        ]
        
        y = 250
        for option in options:
            text = font.render(option, True, WHITE)
            window.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, y))
            y += 40
        
        # Nachricht anzeigen
        if message:
            msg_text = font.render(message, True, message_color)
            window.blit(msg_text, (WINDOW_WIDTH // 2 - msg_text.get_width() // 2, 450))
        
        # Copyright
        copyright = small_font.render(lang_data["made_by"], True, GRAY)
        window.blit(copyright, (10, WINDOW_HEIGHT - 25))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Login
                    username = get_text_input(lang_data["username_prompt"], lang_data)
                    if username:
                        password = get_text_input(lang_data["password_prompt"], lang_data, True)
                        if password:
                            if user_manager.login_user(username, password):
                                message = lang_data["login_success"]
                                message_color = GREEN
                                message_timer = 120
                                return username
                            else:
                                message = lang_data["login_failed"]
                                message_color = RED
                                message_timer = 120
                
                elif event.key == pygame.K_r:
                    # Registrierung
                    username = get_text_input(lang_data["username_prompt"], lang_data)
                    if username:
                        password = get_text_input(lang_data["password_prompt"], lang_data, True)
                        if password:
                            if user_manager.register_user(username, password):
                                message = lang_data["register_success"]
                                message_color = GREEN
                                message_timer = 120
                            else:
                                message = lang_data["user_exists"]
                                message_color = RED
                                message_timer = 120
                
                elif event.key == pygame.K_h:
                    # Highscores anzeigen
                    show_highscores(lang_data, HighscoreManager())
                
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def show_highscores(lang_data, highscore_manager):
    while True:
        window.fill(BLACK)
        
        # Titel
        title = big_font.render(lang_data["highscores"], True, WHITE)
        window.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 50))
        
        if not highscore_manager.highscores:
            no_scores = font.render(lang_data["no_scores"], True, WHITE)
            window.blit(no_scores, (WINDOW_WIDTH // 2 - no_scores.get_width() // 2, 200))
        else:
            # Header
            y = 120
            header_texts = [
                f"{lang_data['rank']:<4} {lang_data['player']:<12} {lang_data['score']:<8} {lang_data['mode']:<8} {lang_data['date']}"
            ]
            header = small_font.render(header_texts[0], True, YELLOW)
            window.blit(header, (50, y))
            y += 30
            
            # Scores
            for i, entry in enumerate(highscore_manager.highscores[:15]):
                rank = f"{i+1}."
                name = entry["username"][:10]
                score = str(entry["score"])
                mode = entry["mode"][:6]
                date = entry["date"]
                
                score_text = f"{rank:<4} {name:<12} {score:<8} {mode:<8} {date}"
                text = small_font.render(score_text, True, WHITE)
                window.blit(text, (50, y))
                y += 25
                
                if y > WINDOW_HEIGHT - 100:
                    break
        
        # Zurück-Button
        back_text = font.render(lang_data["back_to_menu"], True, GRAY)
        window.blit(back_text, (WINDOW_WIDTH // 2 - back_text.get_width() // 2, WINDOW_HEIGHT - 50))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                    return

def wait_for_key(options):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in options:
                    return event.key

def choose_option(title, options_dict, lang_data, y_offset=0):
    while True:
        lines = [title] + list(options_dict.values())
        draw_text_centered(lines, lang_data, y_offset)
        key = wait_for_key(set(options_dict.keys()))
        return key

def set_timer_duration(lang_data):
    seconds = 60
    waiting = True
    
    while waiting:
        window.fill(BLACK)
        msg = big_font.render(lang_data["set_timer"].format(seconds), True, WHITE)
        inst = font.render(lang_data["timer_instructions"], True, WHITE)
        window.blit(msg, (WINDOW_WIDTH // 2 - msg.get_width() // 2, WINDOW_HEIGHT // 2 - 40))
        window.blit(inst, (WINDOW_WIDTH // 2 - inst.get_width() // 2, WINDOW_HEIGHT // 2 + 10))
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    seconds += 10
                elif event.key == pygame.K_DOWN and seconds > 10:
                    seconds -= 10
                elif event.key == pygame.K_RETURN:
                    waiting = False
                    break
    
    return seconds

def set_game_speed(lang_data):
    speeds = {
        pygame.K_1: 8,
        pygame.K_2: 12,
        pygame.K_3: 20
    }
    speed_key = choose_option(lang_data["speed_select"], {
        pygame.K_1: lang_data["slow"],
        pygame.K_2: lang_data["medium"],
        pygame.K_3: lang_data["fast"]
    }, lang_data, -30)
    return speeds[speed_key]

def draw_grid():
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        pygame.draw.line(window, (40, 40, 40), (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
        pygame.draw.line(window, (40, 40, 40), (0, y), (WINDOW_WIDTH, y))

def place_food(snakes, current):
    while True:
        pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if all(pos not in s.body for s in snakes) and pos not in current:
            return pos

def game_loop(player_mode, use_timer, timer_seconds, speed, lang_data, username, user_manager, highscore_manager):
    snake1 = Snake(GREEN, (10, 10), (1, 0))
    snakes = [snake1]

    if player_mode == "dual":
        snake2 = Snake(BLUE, (30, 30), (-1, 0))
        snakes.append(snake2)

    foods = [place_food(snakes, []) for _ in range(2)]
    start_ticks = pygame.time.get_ticks()
    game_over = False
    message = ""
    frame_count = 0
    penalty_message = ""
    penalty_timer = 0
    
    # Speed name für Highscore
    speed_names = {8: "slow", 12: "medium", 20: "fast"}
    speed_name = speed_names[speed]

    while not game_over:
        clock.tick(60)
        frame_count += 1
        time_passed = (pygame.time.get_ticks() - start_ticks) // 1000
        time_left = timer_seconds - time_passed
        
        if penalty_timer > 0:
            penalty_timer -= 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        # Player 1 - Arrows
        if keys[pygame.K_UP] and snake1.direction != (0, 1): snake1.direction = (0, -1)
        if keys[pygame.K_DOWN] and snake1.direction != (0, -1): snake1.direction = (0, 1)
        if keys[pygame.K_LEFT] and snake1.direction != (1, 0): snake1.direction = (-1, 0)
        if keys[pygame.K_RIGHT] and snake1.direction != (-1, 0): snake1.direction = (1, 0)

        # Player 2 - WASD
        if player_mode == "dual":
            if keys[pygame.K_w] and snake2.direction != (0, 1): snake2.direction = (0, -1)
            if keys[pygame.K_s] and snake2.direction != (0, -1): snake2.direction = (0, 1)
            if keys[pygame.K_a] and snake2.direction != (1, 0): snake2.direction = (-1, 0)
            if keys[pygame.K_d] and snake2.direction != (-1, 0): snake2.direction = (1, 0)

        # Move snakes
        if frame_count % speed == 0:
            for snake in snakes:
                snake.move()
                
                head_x, head_y = snake.body[0]
                if (head_x < 0 or head_x >= GRID_WIDTH or 
                    head_y < 0 or head_y >= GRID_HEIGHT):
                    snake.reset()
                    penalty_message = lang_data["wall_penalty"]
                    penalty_timer = 60

            # Collision detection
            collision = False
            for snake in snakes:
                if snake.body[0] in snake.body[1:]:
                    collision = True
                    break
                
                if player_mode == "dual":
                    other = snake2 if snake == snake1 else snake1
                    if snake.body[0] in other.body:
                        collision = True
                        break

            if collision:
                if player_mode == "dual":
                    message = lang_data["collision_dual"]
                else:
                    message = lang_data["collision_single"]
                game_over = True

            # Food collection
            for i in range(len(foods)):
                for snake in snakes:
                    if snake.body[0] == foods[i]:
                        snake.grow()
                        foods[i] = place_food(snakes, foods)

        # Draw everything
        window.fill(BLACK)
        draw_grid()

        for food in foods:
            pygame.draw.rect(window, RED, (food[0]*CELL_SIZE, food[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

        for snake in snakes:
            for segment in snake.body:
                pygame.draw.rect(window, snake.color, (segment[0]*CELL_SIZE, segment[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Score + Time + User
        user_text = font.render(lang_data["logged_in_as"].format(username), True, ORANGE)
        window.blit(user_text, (10, 40))
        
        if len(snakes) == 2:
            score_txt = lang_data["score_dual"].format(snake1.score, snake2.score)
        else:
            score_txt = lang_data["score_single"].format(snake1.score)
            
        if use_timer:
            score_txt += lang_data["time_left"].format(max(0, time_left))

        score = font.render(score_txt, True, WHITE)
        window.blit(score, (10, 10))
        
        # Speed indicator
        speed_display = ""
        if speed == 8: speed_display = lang_data["slow"].split(": ")[1]
        elif speed == 12: speed_display = lang_data["medium"].split(": ")[1]
        else: speed_display = lang_data["fast"].split(": ")[1]
        
        speed_text = font.render(lang_data["speed_indicator"].format(speed_display), True, YELLOW)
        window.blit(speed_text, (WINDOW_WIDTH - speed_text.get_width() - 10, 10))
        
        # Penalty-Meldung anzeigen
        if penalty_timer > 0:
            penalty = font.render(penalty_message, True, RED)
            window.blit(penalty, (WINDOW_WIDTH // 2 - penalty.get_width() // 2, 70))
        
        pygame.display.flip()

        if use_timer and time_left <= 0:
            if len(snakes) == 1:
                message = lang_data["time_up_single"]
            else:
                if snake1.score > snake2.score:
                    message = lang_data["time_up_dual_win1"]
                elif snake2.score > snake1.score:
                    message = lang_data["time_up_dual_win2"]
                else:
                    message = lang_data["time_up_dual_draw"]
            game_over = True

    # Game over screen und Highscore
    final_score = snake1.score if player_mode == "single" else max(snake1.score, snake2.score)
    is_new_highscore = highscore_manager.is_highscore(final_score)
    
    if is_new_highscore and final_score > 0:
        highscore_manager.add_score(username, final_score, player_mode, speed_name)
    
    # Game over screen
    while True:
        window.fill(BLACK)
        
        # Game over message
        end_msg = big_font.render(message, True, WHITE)
        window.blit(end_msg, (WINDOW_WIDTH//2 - end_msg.get_width()//2, WINDOW_HEIGHT//2 - 60))
        
        # Score
        score_msg = font.render(lang_data["final_score"].format(final_score), True, YELLOW)
        window.blit(score_msg, (WINDOW_WIDTH//2 - score_msg.get_width()//2, WINDOW_HEIGHT//2 - 20))
        
        # New Highscore
        if is_new_highscore and final_score > 0:
            highscore_msg = font.render(lang_data["new_highscore"], True, GREEN)
            window.blit(highscore_msg, (WINDOW_WIDTH//2 - highscore_msg.get_width()//2, WINDOW_HEIGHT//2 + 20))
        
        # Controls
        new_game = font.render(lang_data["press_space"], True, WHITE)
        window.blit(new_game, (WINDOW_WIDTH//2 - new_game.get_width()//2, WINDOW_HEIGHT//2 + 80))
        
        menu = font.render(lang_data["press_esc"], True, WHITE)
        window.blit(menu, (WINDOW_WIDTH//2 - menu.get_width()//2, WINDOW_HEIGHT//2 + 110))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Neues Spiel mit gleichen Einstellungen
                    return game_loop(player_mode, use_timer, timer_seconds, speed, lang_data, username, user_manager, highscore_manager)
                elif event.key == pygame.K_ESCAPE:
                    return "menu"

def main():
    user_manager = UserManager()
    highscore_manager = HighscoreManager()
    
    # Sprachauswahl
    lang_data = languages["de"]
    lang_key = choose_option("Select Language / Sprache wählen / Seleziona lingua", {
        pygame.K_1: lang_data["german"],
        pygame.K_2: lang_data["italian"],
        pygame.K_3: lang_data["english"]
    }, lang_data)
    
    if lang_key == pygame.K_1: lang_data = languages["de"]
    elif lang_key == pygame.K_2: lang_data = languages["it"]
    else: lang_data = languages["en"]
    
    while True:
        # Login
        username = login_screen(lang_data, user_manager)
        
        while True:
            # Spielmodus
            mode_key = choose_option(lang_data["player_mode"], {
                pygame.K_3: lang_data["single"],
                pygame.K_4: lang_data["dual"]
            }, lang_data)
            
            mode = "single" if mode_key == pygame.K_3 else "dual"
            
            # Timer-Einstellung
            timer_key = choose_option(lang_data["timer_prompt"], {
                pygame.K_5: lang_data["with_timer"],
                pygame.K_6: lang_data["without_timer"]
            }, lang_data)
            
            use_timer = (timer_key == pygame.K_5)
            seconds = set_timer_duration(lang_data) if use_timer else 999999
            
            # Geschwindigkeit
            speed = set_game_speed(lang_data)
            
            # Spiel starten
            result = game_loop(mode, use_timer, seconds, speed, lang_data, username, user_manager, highscore_manager)
            
            if result == "menu":
                break

if __name__ == "__main__":
    main()