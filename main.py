import pygame
import random
import string

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fruit Slicer")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class GameState:
    def __init__(self):
        self.artist_mode = False
        self.load_assets("classic_mode")  # Start in classic mode
        self.game_active = False
        self.score = 0
        self.lives = 3
        self.fruits = []
        self.bombs = []
        self.ices = []
        self.letters_active = {}
        self.available_letters = set(string.ascii_uppercase)
        self.ice_effect = False
        self.ice_effect_duration = 0
        self.game_speed = 30
        self.next_spawn_time = random.randint(20, 60)
        self.next_bomb_spawn_time = random.randint(100, 200)
        self.next_ice_spawn_time = random.randint(500, 1000)

    def load_assets(self, mode):
        if mode == "artist_mode":
            # Artist mode assets
            self.fruits_images = {
                "apple": pygame.image.load("assets/apple.png"),
                "banana": pygame.image.load("assets/banana.png"),
                "cherry": pygame.image.load("assets/cherry.png"),
                "watermelon": pygame.image.load("assets/watermelon.png"),
                "purple_fruit": pygame.image.load("assets/Purple_fruit.png"),
            }
            self.bomb_image = pygame.image.load("assets/bomb.png")
            self.ice_image = pygame.image.load("assets/ice.png")
            self.background_image = pygame.image.load("assets/background.png")
            self.icon_image = pygame.image.load("assets/icon.png")
            self.button_image = pygame.image.load("assets/log.png")  # Log to change with artist asset

            # Artist mode audio (keep existing paths)
            self.sword_sound = pygame.mixer.Sound("assets/sword.mp3")
            self.bomb_sound = pygame.mixer.Sound("assets/bomb.mp3")
            self.ice_sound = pygame.mixer.Sound("assets/ice.mp3")
            self.fruit_sound = pygame.mixer.Sound("assets/fruits.mp3")
        else:  # Classic mode
            # Classic mode assets
            self.fruits_images = {
                "apple": pygame.image.load("assets/classic_mode/classic_lemon.png"),
                "banana": pygame.image.load("assets/classic_mode/classic_strawberry.png"),
                "cherry": pygame.image.load("assets/classic_mode/classic_apple.png"),
                "watermelon": pygame.image.load("assets/classic_mode/classic_watermelon.png"),
                "purple_fruit": pygame.image.load("assets/classic_mode/classic_grapefruit.png"),
            }
            self.bomb_image = pygame.image.load("assets/classic_mode/classic_bomb.png")
            self.ice_image = pygame.image.load("assets/classic_mode/classic_ice_cube.png")
            self.background_image = pygame.image.load("assets/classic_mode/classic_background.jpg")
            self.icon_image = pygame.image.load("assets/classic_mode/classic_icon.png")
            self.button_image = pygame.image.load("assets/classic_mode/classic_log.png")

            # Classic mode audio (placeholders for now)
            self.sword_sound = pygame.mixer.Sound("assets/sword.mp3")  # Replace with classic mode sword sound
            self.bomb_sound = pygame.mixer.Sound("assets/bomb.mp3")  # Replace with classic mode bomb sound
            self.ice_sound = pygame.mixer.Sound("assets/ice.mp3")  # Replace with classic mode ice sound
            self.fruit_sound = pygame.mixer.Sound("assets/fruits.mp3")  # Replace with classic mode fruit sound

        # Scale images
        for key in self.fruits_images:
            self.fruits_images[key] = pygame.transform.scale(self.fruits_images[key], (60, 60))
        self.bomb_image = pygame.transform.scale(self.bomb_image, (60, 60))
        self.ice_image = pygame.transform.scale(self.ice_image, (60, 60))
        self.background_image = pygame.transform.scale(self.background_image, (WIDTH, HEIGHT))
        pygame.display.set_icon(self.icon_image)
        self.button_image = pygame.transform.scale(self.button_image, (400, 50))

    def trigger(self):
        self.artist_mode = not self.artist_mode
        mode = "artist_mode" if self.artist_mode else "classic_mode"
        self.load_assets(mode)
        # Update all button images
        for button in buttons:
            button.image = pygame.transform.scale(self.button_image, (button.rect.width, button.rect.height))

    def start_game(self):
        self.score = 0
        self.lives = 3
        self.fruits = []
        self.bombs = []
        self.ices = []
        self.letters_active = {}
        self.available_letters = set(string.ascii_uppercase)
        self.ice_effect = False
        self.ice_effect_duration = 0
        self.game_speed = 30
        self.next_spawn_time = random.randint(20, 60)
        self.next_bomb_spawn_time = random.randint(100, 200)
        self.next_ice_spawn_time = random.randint(500, 1000)
        self.game_active = True

    def return_to_menu(self):
        self.game_active = False
        self.fruits = []
        self.bombs = []
        self.ices = []
        self.letters_active = {}
        self.available_letters = set(string.ascii_uppercase)
        self.ice_effect = False
        self.ice_effect_duration = 0
        self.game_speed = 30
        self.next_spawn_time = random.randint(20, 60)
        self.next_bomb_spawn_time = random.randint(100, 200)
        self.next_ice_spawn_time = random.randint(500, 1000)

    def spawn_object(self, is_bomb=False, is_ice=False):
        if not self.available_letters:
            return
        
        x = random.randint(100, WIDTH - 100)
        letter = random.choice(list(self.available_letters))
        self.available_letters.remove(letter)
        
        if is_bomb:
            obj = Bomb(x, self.bomb_image, letter)
            self.bombs.append(obj)
        elif is_ice:
            obj = Ice(x, self.ice_image, letter)
            self.ices.append(obj)
        else:
            image = random.choice(list(self.fruits_images.values()))
            obj = Fruit(x, image, letter)
            self.fruits.append(obj)
        self.letters_active[letter] = obj

# Initialize game state
game_state = GameState()

font = pygame.font.Font("assets/classic_mode/font.ttf", 26)

def quit_game():
    pygame.quit()
    exit()

def scores():
    print("Scores !")

def language():
    print("Bonjour ! Hello ! Hola !")

class Fruit:
    def __init__(self, x, image, letter):
        self.x = x
        self.y = HEIGHT
        self.image = image
        self.letter = letter
        self.speed = random.randint(7, 12)
        self.vy = -random.randint(15, 20)
        self.vx = random.choice([-3, -2, -1, 1, 2, 3])
        self.gravity = 0.3
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

class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action 
        self.image = pygame.transform.scale(game_state.button_image, (width, height))

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        text_surf = font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.action()

class Bomb(Fruit):
    pass

class Ice(Fruit):
    pass

new_game_button = Button(200, 50, 400, 50, "New game", game_state.start_game)
scores_button = Button(200, 125, 400, 50, "Leaderboards", scores)
render_button = Button(200, 200, 400, 50, "Trigger mode", game_state.trigger)
language_button = Button(200, 275, 400, 50, "Language", language)
quit_button = Button(200, 350, 400, 50, "Quit", quit_game)
buttons = [new_game_button, scores_button, render_button, language_button, quit_button]

clock = pygame.time.Clock()
running = True

while running:
    screen.blit(game_state.background_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_state.game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Check for ESC key press
                    game_state.return_to_menu()
                key = event.unicode.upper()
                if key in game_state.letters_active:
                    if isinstance(game_state.letters_active[key], Bomb):
                        game_state.sword_sound.play()
                        game_state.bomb_sound.play()
                        game_state.lives = 0
                    elif isinstance(game_state.letters_active[key], Ice):
                        game_state.sword_sound.play()
                        game_state.ice_sound.play()
                        game_state.ice_effect = True
                        game_state.ice_effect_duration = pygame.time.get_ticks() + random.randint(2000, 3000)
                    else:
                        game_state.sword_sound.play()
                        game_state.fruit_sound.play()
                        game_state.score += 1
                        if game_state.score % 10 == 0:
                            game_state.game_speed += 5
                    game_state.letters_active[key].active = False
                    del game_state.letters_active[key]
                    game_state.available_letters.add(key)
        else:
            for button in buttons:
                if button.handle_event(event):
                    if button == render_button:
                        # The trigger method now updates all button images
                        pass

    if game_state.game_active:
        if game_state.ice_effect and pygame.time.get_ticks() > game_state.ice_effect_duration:
            game_state.ice_effect = False
        
        game_state.next_spawn_time -= 1
        if game_state.next_spawn_time <= 0:
            game_state.spawn_object()
            game_state.next_spawn_time = random.randint(20, 60)
        
        game_state.next_bomb_spawn_time -= 1
        if game_state.next_bomb_spawn_time <= 0:
            game_state.spawn_object(is_bomb=True)
            game_state.next_bomb_spawn_time = random.randint(100, 200)
        
        if game_state.score >= 50:
            game_state.next_ice_spawn_time -= 1
            if game_state.next_ice_spawn_time <= 0:
                game_state.spawn_object(is_ice=True)
                game_state.next_ice_spawn_time = random.randint(300, 400)
        
        for obj_list in [game_state.fruits, game_state.bombs, game_state.ices]:
            for obj in obj_list:
                obj.move()
        
        for obj_list in [game_state.fruits, game_state.bombs, game_state.ices]:
            for obj in obj_list[:]:
                if obj.y > HEIGHT and obj.active:
                    if obj_list != game_state.bombs and obj_list != game_state.ices:
                        game_state.lives -= 1
                    obj_list.remove(obj)
                    if obj.letter in game_state.letters_active:
                        del game_state.letters_active[obj.letter]
                        game_state.available_letters.add(obj.letter)
        
        if game_state.lives <= 0:
            screen.blit(game_state.background_image, (0, 0))
            game_over_text = font.render("GAME OVER", True, RED)
            screen.blit(game_over_text, (WIDTH//2 - 80, HEIGHT//2))
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

    if game_state.game_active:
        for fruit in game_state.fruits:
            fruit.draw(screen)
        for bomb in game_state.bombs:
            bomb.draw(screen)
        for ice in game_state.ices:
            ice.draw(screen)
        
        score_text = font.render(f"Score: {game_state.score}", True, RED)
        lives_text = font.render(f"Lives: {game_state.lives}", True, RED)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 50))
    else:
        for button in buttons:
            button.draw(screen)

    pygame.display.update()
    clock.tick(game_state.game_speed if not game_state.ice_effect else 0)

pygame.quit()