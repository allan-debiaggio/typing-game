import pygame
import random
import string
import os

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fruit Slicer")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
BLUE  = (0, 0, 255)

LANGUAGES = {
    "English": {
        "new_game": "New Game",
        "leaderboards": "Leaderboards",
        "trigger_mode": "Trigger Mode",
        "language": "Language",
        "quit": "Quit",
        "game_over": "GAME OVER",
        "score": "Score",
        "lives": "Lives",
        "difficulty_title": "Select Difficulty",
        "easy": "Easy",
        "medium": "Medium",
        "hard": "Hard",
        "back": "Back",
        "lb_title": "Select Leaderboard"
    },
    "French": {
        "new_game": "Nouvelle partie",
        "leaderboards": "Scores",
        "trigger_mode": "Changer de mode",
        "language": "Langue",
        "quit": "Quitter",
        "game_over": "FIN DE PARTIE",
        "score": "Points",
        "lives": "Vies",
        "difficulty_title": "Sélectionnez la difficulté",
        "easy": "Facile",
        "medium": "Moyen",
        "hard": "Difficile",
        "back": "Retour",
        "lb_title": "Sélectionnez le leaderboard"
    },
    "Spanish": {
        "new_game": "Nueva partida",
        "leaderboards": "Puntaje",
        "trigger_mode": "Cambiar el modo de juego",
        "language": "Idioma",
        "quit": "Salir",
        "game_over": "JUEGO TERMINADO",
        "score": "Puntos",
        "lives": "Vidas",
        "difficulty_title": "Selecciona la dificultad",
        "easy": "Fácil",
        "medium": "Medio",
        "hard": "Difícil",
        "back": "Atrás",
        "lb_title": "Selecciona el leaderboard"
    }
}

def language():
    languages = list(LANGUAGES.keys())
    current_index = languages.index(language.current_language)
    next_index = (current_index + 1) % len(languages)
    language.current_language = languages[next_index]
    update_texts()

language.current_language = "English"

def update_texts():
    new_game_button.text = LANGUAGES[language.current_language]["new_game"]
    scores_button.text = LANGUAGES[language.current_language]["leaderboards"]
    render_button.text = LANGUAGES[language.current_language]["trigger_mode"]
    language_button.text = LANGUAGES[language.current_language]["language"]
    quit_button.text = LANGUAGES[language.current_language]["quit"]
    for button, key in zip(difficulty_buttons, ["easy", "medium", "hard", "back"]):
        button.text = LANGUAGES[language.current_language][key]
    for button, key in zip(leaderboard_buttons, ["easy", "medium", "hard", "back"]):
        button.text = LANGUAGES[language.current_language][key]

def update_leaderboard(name, score, difficulty):
    filename = f"leaderboard_{difficulty}.txt"
    entries = []
    if os.path.exists(filename):
        with open(filename, "r") as f:
            for line in f:
                parts = line.strip().split(";")
                if len(parts) == 2:
                    try:
                        old_score = int(parts[0])
                        old_name = parts[1]
                        entries.append((old_score, old_name))
                    except ValueError:
                        pass
    entries.append((score, name))
    entries.sort(key=lambda x: x[0], reverse=True)
    with open(filename, "w") as f:
        for s, n in entries:
            f.write(f"{s};{n}\n")

def get_player_name(screen, font):
    name = ""
    active = True
    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode
        screen.fill(BLACK)
        prompt = font.render("Entrez votre nom: " + name, True, WHITE)
        instruction = font.render("Appuyez sur Entrée pour valider", True, WHITE)
        screen.blit(prompt, (WIDTH//2 - prompt.get_width()//2, HEIGHT//2))
        screen.blit(instruction, (WIDTH//2 - instruction.get_width()//2, HEIGHT//2 + 40))
        pygame.display.flip()
        pygame.time.Clock().tick(30)
    return name

def display_leaderboard(difficulty):
    filename = f"leaderboard_{difficulty}.txt"
    entries = []
    if os.path.exists(filename):
        with open(filename, "r") as f:
            for line in f:
                parts = line.strip().split(";")
                if len(parts) == 2:
                    try:
                        s = int(parts[0])
                        n = parts[1]
                        entries.append((s, n))
                    except ValueError:
                        pass
    entries.sort(key=lambda x: x[0], reverse=True)
    leaderboard_active = True
    while leaderboard_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                    leaderboard_active = False
        screen.fill(BLACK)
        title_text = font.render(f"Leaderboard {difficulty}", True, WHITE)
        screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 20))
        y_offset = 80
        for s, n in entries:
            entry_text = font.render(f"{n}: {s}", True, WHITE)
            screen.blit(entry_text, (WIDTH//2 - entry_text.get_width()//2, y_offset))
            y_offset += 40
        pygame.display.flip()
        clock.tick(30)

class SlicedFruit:
    def __init__(self, x, y, image, vx, vy, rotation_speed=0, gravity=0.3):
        self.x = x
        self.y = y
        self.image = image
        self.vx = vx
        self.vy = vy
        self.gravity = gravity
        self.rotation = 0
        self.rotation_speed = rotation_speed
        self.active = True

    def move(self):
        if game_state.ice_effect:
            return
        self.vy += self.gravity
        self.x += self.vx
        self.y += self.vy
        self.rotation += self.rotation_speed

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.image, self.rotation)
        rect = rotated_image.get_rect(center=(self.x, self.y))
        screen.blit(rotated_image, rect)

class GameState:
    def __init__(self):
        self.artist_mode = False
        self.load_assets("classic_mode")
        self.game_active = False
        self.score = 0
        self.lives = 3
        self.fruits = []
        self.bombs = []
        self.ices = []
        self.sliced_fruits = []
        self.letters_active = {}
        self.available_letters = set(string.ascii_uppercase)
        self.ice_effect = False
        self.ice_effect_duration = 0
        self.game_speed = 30
        self.next_spawn_time = random.randint(20, 60)
        self.next_bomb_spawn_time = random.randint(100, 200)
        self.next_ice_spawn_time = random.randint(500, 1000)
        self.speed_factor = 1.0
        self.combo_texts = []
        self.menu = "main"
        self.difficulty = "Medium"

    def load_assets(self, mode):
        if mode == "artist_mode":
            self.fruits_images = {
                "apple": pygame.image.load("assets/apple.png"),
                "banana": pygame.image.load("assets/banana.png"),
                "cherry": pygame.image.load("assets/cherry.png"),
                "watermelon": pygame.image.load("assets/watermelon.png"),
                "purple_fruit": pygame.image.load("assets/Purple_fruit.png"),
            }
            self.fruits_sliced_left = {
                "apple": pygame.image.load("assets/apple_sliced_left.png"),
                "banana": pygame.image.load("assets/banana_sliced_left.png"),
                "cherry": pygame.image.load("assets/cherry_sliced_left.png"),
                "watermelon": pygame.image.load("assets/watermelon_sliced_left.png"),
                "purple_fruit": pygame.image.load("assets/Purple_fruit_sliced_left.png"),
            }
            self.fruits_sliced_right = {
                "apple": pygame.image.load("assets/apple_sliced_right.png"),
                "banana": pygame.image.load("assets/banana_sliced_right.png"),
                "cherry": pygame.image.load("assets/cherry_sliced_right.png"),
                "watermelon": pygame.image.load("assets/watermelon_sliced_right.png"),
                "purple_fruit": pygame.image.load("assets/Purple_fruit_sliced_right.png"),
            }
            self.bomb_image = pygame.image.load("assets/bomb.png")
            self.ice_image = pygame.image.load("assets/ice.png")
            self.background_image = pygame.image.load("assets/background.png")
            self.icon_image = pygame.image.load("assets/icon.png")
            self.button_image = pygame.image.load("assets/log.png")
            self.sword_sound = pygame.mixer.Sound("assets/sounds/sword.mp3")
            self.bomb_sound = pygame.mixer.Sound("assets/sounds/bomb.mp3")
            self.ice_sound = pygame.mixer.Sound("assets/sounds/ice.mp3")
            self.fruit_sound = pygame.mixer.Sound("assets/sounds/fruits.mp3")
            self.music = "assets/sounds/music.mp3"
            self.button_sound = pygame.mixer.Sound("assets/sounds/button.mp3")
        else:
            self.fruits_images = {
                "apple": pygame.image.load("assets/classic_mode/classic_lemon.png"),
                "banana": pygame.image.load("assets/classic_mode/classic_strawberry.png"),
                "cherry": pygame.image.load("assets/classic_mode/classic_apple.png"),
                "watermelon": pygame.image.load("assets/classic_mode/classic_watermelon.png"),
                "purple_fruit": pygame.image.load("assets/classic_mode/classic_grapefruit.png"),
            }
            self.fruits_sliced_left = {
                "apple": pygame.image.load("assets/classic_mode/classic_apple_sliced_left.png"),
                "banana": pygame.image.load("assets/classic_mode/classic_strawberry_sliced_left.png"),
                "cherry": pygame.image.load("assets/classic_mode/classic_apple_sliced_left.png"),
                "watermelon": pygame.image.load("assets/classic_mode/classic_watermelon_sliced_left.png"),
                "purple_fruit": pygame.image.load("assets/classic_mode/classic_grapefruit_sliced_left.png"),
            }
            self.fruits_sliced_right = {
                "apple": pygame.image.load("assets/classic_mode/classic_apple_sliced_right.png"),
                "banana": pygame.image.load("assets/classic_mode/classic_strawberry_sliced_right.png"),
                "cherry": pygame.image.load("assets/classic_mode/classic_apple_sliced_right.png"),
                "watermelon": pygame.image.load("assets/classic_mode/classic_watermelon_sliced_right.png"),
                "purple_fruit": pygame.image.load("assets/classic_mode/classic_grapefruit_sliced_right.png"),
            }
            self.bomb_image = pygame.image.load("assets/classic_mode/classic_bomb.png")
            self.ice_image = pygame.image.load("assets/classic_mode/classic_ice_cube.png")
            self.background_image = pygame.image.load("assets/classic_mode/classic_background.jpg")
            self.icon_image = pygame.image.load("assets/classic_mode/classic_icon.png")
            self.button_image = pygame.image.load("assets/classic_mode/classic_log.png")
            self.sword_sound = pygame.mixer.Sound("assets/classic_mode/sounds_classic/sword_classic.mp3")
            self.bomb_sound = pygame.mixer.Sound("assets/classic_mode/sounds_classic/bomb_classic.mp3")
            self.ice_sound = pygame.mixer.Sound("assets/classic_mode/sounds_classic/ice_classic.mp3")
            self.fruit_sound = pygame.mixer.Sound("assets/classic_mode/sounds_classic/fruits_classic.mp3")
            self.music = "assets/classic_mode/sounds_classic/music_classic.mp3"
            self.button_sound = pygame.mixer.Sound("assets/classic_mode/sounds_classic/button_classic.mp3")
        for key in self.fruits_images:
            self.fruits_images[key] = pygame.transform.scale(self.fruits_images[key], (60, 60))
        for key in self.fruits_sliced_left:
            self.fruits_sliced_left[key] = pygame.transform.scale(self.fruits_sliced_left[key], (60, 60))
        for key in self.fruits_sliced_right:
            self.fruits_sliced_right[key] = pygame.transform.scale(self.fruits_sliced_right[key], (60, 60))
        self.bomb_image = pygame.transform.scale(self.bomb_image, (60, 60))
        self.ice_image = pygame.transform.scale(self.ice_image, (60, 60))
        self.background_image = pygame.transform.scale(self.background_image, (WIDTH, HEIGHT))
        pygame.display.set_icon(self.icon_image)
        self.button_image = pygame.transform.scale(self.button_image, (400, 50))

    def trigger(self):
        self.artist_mode = not self.artist_mode
        mode = "artist_mode" if self.artist_mode else "classic_mode"
        self.load_assets(mode)
        pygame.mixer.music.stop()
        pygame.mixer.music.load(self.music)
        for button in buttons:
            button.image = pygame.transform.scale(self.button_image, (button.rect.width, button.rect.height))
        for button in difficulty_buttons:
            button.image = pygame.transform.scale(self.button_image, (button.rect.width, button.rect.height))
        for button in leaderboard_buttons:
            button.image = pygame.transform.scale(self.button_image, (button.rect.width, button.rect.height))

    def start_game(self, difficulty):
        self.difficulty = difficulty
        if difficulty == "Easy":
            self.lives = 5
            self.game_speed = 25
            self.speed_factor = 0.8
            self.next_spawn_time = random.randint(40, 80)
            self.next_bomb_spawn_time = random.randint(150, 300)
            self.next_ice_spawn_time = random.randint(600, 1200)
        elif difficulty == "Medium":
            self.lives = 3
            self.game_speed = 30
            self.speed_factor = 1.0
            self.next_spawn_time = random.randint(20, 60)
            self.next_bomb_spawn_time = random.randint(100, 200)
            self.next_ice_spawn_time = random.randint(500, 1000)
        elif difficulty == "Hard":
            self.lives = 2
            self.game_speed = 40
            self.speed_factor = 1.2
            self.next_spawn_time = random.randint(10, 30)
            self.next_bomb_spawn_time = random.randint(50, 150)
            self.next_ice_spawn_time = random.randint(300, 600)
        self.score = 0
        self.fruits = []
        self.bombs = []
        self.ices = []
        self.sliced_fruits = []
        self.letters_active = {}
        self.available_letters = set(string.ascii_uppercase)
        self.ice_effect = False
        self.ice_effect_duration = 0
        self.combo_texts = []
        self.game_active = True
        pygame.mixer.music.load(self.music)
        pygame.mixer.music.play(-1)
        self.menu = None

    def return_to_menu(self):
        self.game_active = False
        self.fruits = []
        self.bombs = []
        self.ices = []
        self.sliced_fruits = []
        self.letters_active = {}
        self.available_letters = set(string.ascii_uppercase)
        self.ice_effect = False
        self.ice_effect_duration = 0
        self.game_speed = 30
        self.next_spawn_time = random.randint(20, 60)
        self.next_bomb_spawn_time = random.randint(100, 200)
        self.next_ice_spawn_time = random.randint(500, 1000)
        pygame.mixer.music.stop()
        self.menu = "main"

    def spawn_object(self, is_bomb=False, is_ice=False):
        x = random.randint(100, WIDTH - 100)
        if is_bomb or is_ice:
            if not self.available_letters:
                return
            letter = random.choice(list(self.available_letters))
            self.available_letters.remove(letter)
            if is_bomb:
                obj = Bomb(x, self.bomb_image, letter, speed_factor=self.speed_factor)
                self.bombs.append(obj)
            else:
                obj = Ice(x, self.ice_image, letter, speed_factor=self.speed_factor)
                self.ices.append(obj)
            self.letters_active[letter] = [obj]
        else:
            duplicate_possible = False
            active_fruit_letters = [fruit.letter for fruit in self.fruits]
            if active_fruit_letters and random.random() < 0.1:
                letter = random.choice(active_fruit_letters)
                duplicate_possible = True
            if not duplicate_possible:
                if self.available_letters:
                    letter = random.choice(list(self.available_letters))
                    self.available_letters.remove(letter)
                else:
                    letter = random.choice(list(string.ascii_uppercase))
            fruit_type = random.choice(list(self.fruits_images.keys()))
            image = self.fruits_images[fruit_type]
            obj = Fruit(x, image, letter, fruit_type, speed_factor=self.speed_factor)
            self.fruits.append(obj)
            if letter in self.letters_active:
                self.letters_active[letter].append(obj)
            else:
                self.letters_active[letter] = [obj]

class Fruit:
    def __init__(self, x, image, letter, fruit_type, speed_factor=1.0):
        self.x = x
        self.y = HEIGHT
        self.image = image
        self.letter = letter
        self.fruit_type = fruit_type
        self.speed_factor = speed_factor
        self.speed = int(random.randint(7, 12) * speed_factor)
        self.vy = -int(random.randint(15, 20) * speed_factor)
        self.vx = random.choice([-3, -2, -1, 1, 2, 3])
        self.gravity = 0.3 * speed_factor
        self.active = True

    def move(self):
        if not game_state.ice_effect:
            self.vy += self.gravity
            self.y += self.vy
            self.x += self.vx

    def draw(self, screen):
        if self.active:
            screen.blit(self.image, (self.x, self.y))
            text = font.render(self.letter, True, RED)
            screen.blit(text, (self.x + 20, self.y - 30))

class Bomb(Fruit):
    def __init__(self, x, image, letter, speed_factor=1.0):
        super().__init__(x, image, letter, "bomb", speed_factor=speed_factor)

class Ice(Fruit):
    def __init__(self, x, image, letter, speed_factor=1.0):
        super().__init__(x, image, letter, "ice", speed_factor=speed_factor)

class Button:
    def __init__(self, x, y, width, height, text, action, game_state):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.image = pygame.transform.scale(game_state.button_image, (width, height))
        self.game_state = game_state

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        text_surf = font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.game_state.button_sound.play()
                self.action()

game_state = GameState()
font = pygame.font.Font("assets/classic_mode/font.ttf", 26)

new_game_button = Button(200, 50, 400, 50, LANGUAGES[language.current_language]["new_game"], lambda: setattr(game_state, "menu", "difficulty"), game_state)
scores_button = Button(200, 125, 400, 50, LANGUAGES[language.current_language]["leaderboards"], lambda: setattr(game_state, "menu", "leaderboard"), game_state)
render_button = Button(200, 200, 400, 50, LANGUAGES[language.current_language]["trigger_mode"], game_state.trigger, game_state)
language_button = Button(200, 275, 400, 50, LANGUAGES[language.current_language]["language"], language, game_state)
quit_button = Button(200, 350, 400, 50, LANGUAGES[language.current_language]["quit"], lambda: (pygame.quit(), exit()), game_state)
buttons = [new_game_button, scores_button, render_button, language_button, quit_button]

easy_button = Button(200, 100, 400, 50, LANGUAGES[language.current_language]["easy"], lambda: game_state.start_game("Easy"), game_state)
medium_button = Button(200, 175, 400, 50, LANGUAGES[language.current_language]["medium"], lambda: game_state.start_game("Medium"), game_state)
hard_button = Button(200, 250, 400, 50, LANGUAGES[language.current_language]["hard"], lambda: game_state.start_game("Hard"), game_state)
back_button = Button(200, 325, 400, 50, LANGUAGES[language.current_language]["back"], lambda: setattr(game_state, "menu", "main"), game_state)
difficulty_buttons = [easy_button, medium_button, hard_button, back_button]

lb_easy_button = Button(200, 100, 400, 50, LANGUAGES[language.current_language]["easy"], lambda: display_leaderboard("Easy"), game_state)
lb_medium_button = Button(200, 175, 400, 50, LANGUAGES[language.current_language]["medium"], lambda: display_leaderboard("Medium"), game_state)
lb_hard_button = Button(200, 250, 400, 50, LANGUAGES[language.current_language]["hard"], lambda: display_leaderboard("Hard"), game_state)
lb_back_button = Button(200, 325, 400, 50, LANGUAGES[language.current_language]["back"], lambda: setattr(game_state, "menu", "main"), game_state)
leaderboard_buttons = [lb_easy_button, lb_medium_button, lb_hard_button, lb_back_button]

clock = pygame.time.Clock()
running = True

while running:
    screen.blit(game_state.background_image, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_state.game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state.return_to_menu()
                key = event.unicode.upper()
                if key in game_state.letters_active:
                    objs = game_state.letters_active[key]
                    if any(isinstance(obj, Bomb) for obj in objs):
                        game_state.sword_sound.play()
                        game_state.bomb_sound.play()
                        game_state.lives = 0
                    elif any(isinstance(obj, Ice) for obj in objs):
                        game_state.sword_sound.play()
                        game_state.ice_sound.play()
                        game_state.ice_effect = True
                        game_state.ice_effect_duration = pygame.time.get_ticks() + random.randint(2000, 3000)
                        for obj in objs:
                            if isinstance(obj, Ice):
                                obj.active = False
                    else:
                        game_state.sword_sound.play()
                        game_state.fruit_sound.play()
                        count = len(objs)
                        base_points = count
                        combo_bonus = 0
                        if count == 2:
                            combo_bonus = 5
                        elif count == 3:
                            combo_bonus = 10
                        elif count >= 4:
                            combo_bonus = 20
                        points = base_points + combo_bonus
                        game_state.score += points
                        if count > 1:
                            avg_x = sum(obj.x for obj in objs) / count
                            min_y = min(obj.y for obj in objs)
                            combo_text_surface = font.render(f"COMBO +{points}", True, BLUE)
                            game_state.combo_texts.append((combo_text_surface, (avg_x, min_y - 40), pygame.time.get_ticks() + 1000))
                        for obj in objs:
                            if isinstance(obj, Fruit):
                                fruit_type = obj.fruit_type
                                left_image = game_state.fruits_sliced_left[fruit_type]
                                right_image = game_state.fruits_sliced_right[fruit_type]
                                lf = SlicedFruit(obj.x, obj.y, left_image, vx=-abs(obj.vx)-1, vy=obj.vy, rotation_speed=-5, gravity=obj.gravity)
                                rf = SlicedFruit(obj.x, obj.y, right_image, vx=abs(obj.vx)+1, vy=obj.vy, rotation_speed=5, gravity=obj.gravity)
                                game_state.sliced_fruits.append(lf)
                                game_state.sliced_fruits.append(rf)
                            obj.active = False
                    del game_state.letters_active[key]
                    game_state.available_letters.add(key)
        else:
            if game_state.menu == "difficulty":
                for button in difficulty_buttons:
                    button.handle_event(event)
            elif game_state.menu == "leaderboard":
                for button in leaderboard_buttons:
                    button.handle_event(event)
            else:
                for button in buttons:
                    button.handle_event(event)
    if game_state.game_active:
        if game_state.ice_effect and pygame.time.get_ticks() > game_state.ice_effect_duration:
            game_state.ice_effect = False
        if not game_state.ice_effect:
            game_state.next_spawn_time -= 1
            if game_state.next_spawn_time <= 0:
                game_state.spawn_object()
                game_state.next_spawn_time = random.randint(20, 60)
            game_state.next_bomb_spawn_time -= 1
            if game_state.next_bomb_spawn_time <= 0:
                game_state.spawn_object(is_bomb=True)
                game_state.next_bomb_spawn_time = random.randint(100, 200)
            if game_state.score >= 10:
                game_state.next_ice_spawn_time -= 1
                if game_state.next_ice_spawn_time <= 0:
                    game_state.spawn_object(is_ice=True)
                    game_state.next_ice_spawn_time = random.randint(300, 400)
        for obj_list in [game_state.fruits, game_state.bombs, game_state.ices]:
            for obj in obj_list:
                obj.move()
        for obj_list in [game_state.fruits, game_state.bombs, game_state.ices]:
            for obj in obj_list[:]:
                if (obj.y > HEIGHT and obj.active) or (not obj.active):
                    if obj in game_state.fruits and obj.active:
                        game_state.lives -= 1
                    obj_list.remove(obj)
                    if obj.letter in game_state.letters_active:
                        try:
                            game_state.letters_active[obj.letter].remove(obj)
                        except ValueError:
                            pass
                        if not game_state.letters_active[obj.letter]:
                            del game_state.letters_active[obj.letter]
                            game_state.available_letters.add(obj.letter)
        for sliced in game_state.sliced_fruits:
            sliced.move()
        for sliced in game_state.sliced_fruits[:]:
            if sliced.y > HEIGHT or sliced.x < -50 or sliced.x > WIDTH + 50:
                game_state.sliced_fruits.remove(sliced)
        for fruit in game_state.fruits:
            fruit.draw(screen)
        for bomb in game_state.bombs:
            bomb.draw(screen)
        for ice in game_state.ices:
            ice.draw(screen)
        for sliced in game_state.sliced_fruits:
            sliced.draw(screen)
        for combo in game_state.combo_texts[:]:
            text_surface, pos, expire_time = combo
            if pygame.time.get_ticks() < expire_time:
                screen.blit(text_surface, pos)
            else:
                game_state.combo_texts.remove(combo)
        score_text = font.render(f"{LANGUAGES[language.current_language]['score']}: {game_state.score}", True, RED)
        lives_text = font.render(f"{LANGUAGES[language.current_language]['lives']}: {game_state.lives}", True, RED)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 50))
        if game_state.lives <= 0:
            screen.blit(game_state.background_image, (0, 0))
            game_over_text = font.render(LANGUAGES[language.current_language]["game_over"], True, RED)
            screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2))
            pygame.mixer.music.stop()
            pygame.display.update()
            start_time = pygame.time.get_ticks()
            while pygame.time.get_ticks() - start_time < 2000:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        pygame.quit()
                        exit()
                pygame.time.delay(10)
            game_state.game_active = False
            player_name = get_player_name(screen, font)
            update_leaderboard(player_name, game_state.score, game_state.difficulty)
            game_state.menu = "main"
    else:
        if game_state.menu == "difficulty":
            diff_title = font.render(LANGUAGES[language.current_language]["difficulty_title"], True, WHITE)
            screen.blit(diff_title, (WIDTH//2 - diff_title.get_width()//2, 20))
            for button in difficulty_buttons:
                button.draw(screen)
        elif game_state.menu == "leaderboard":
            lb_title = font.render(LANGUAGES[language.current_language]["lb_title"], True, WHITE)
            screen.blit(lb_title, (WIDTH//2 - lb_title.get_width()//2, 20))
            for button in leaderboard_buttons:
                button.draw(screen)
        else:
            for button in buttons:
                button.draw(screen)
    pygame.display.update()
    clock.tick(game_state.game_speed if not game_state.ice_effect else 0)

pygame.quit()
