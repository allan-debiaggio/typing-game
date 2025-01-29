import pygame
import random
import string

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fruit Slicer")
fruits_images = {
    "apple": pygame.image.load("assets/apple.png"),
    "banana": pygame.image.load("assets/banana.png"),
    "cherry": pygame.image.load("assets/cherry.png"),
    "watermelon": pygame.image.load("assets/watermelon.png"),
    "purple_fruit": pygame.image.load("assets/Purple_fruit.png"),
}
bomb_image = pygame.image.load("assets/bomb.png")
ice_image = pygame.image.load("assets/ice.png")

for key in fruits_images:
    fruits_images[key] = pygame.transform.scale(fruits_images[key], (60, 60))
bomb_image = pygame.transform.scale(bomb_image, (60, 60))
ice_image = pygame.transform.scale(ice_image, (60, 60))

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
font = pygame.font.Font(None, 40)

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
        if not ice_effect:
            self.vy += self.gravity
            self.y += self.vy
            self.x += self.vx

    def draw(self, screen):
        if self.active:
            screen.blit(self.image, (self.x, self.y))
            text = font.render(self.letter, True, RED)
            screen.blit(text, (self.x + 20, self.y - 30))

class Bomb(Fruit):
    pass

class Ice(Fruit):
    pass

clock = pygame.time.Clock()
running = True
score = 0
lives = 3
fruits = []
bombs = []
ices = []
letters_active = {}
game_speed = 30
available_letters = set(string.ascii_uppercase)

ice_effect = False
ice_effect_duration = 0
def spawn_object(is_bomb=False, is_ice=False):
    global available_letters
    if not available_letters:
        return
    
    x = random.randint(100, WIDTH - 100)
    letter = random.choice(list(available_letters))
    available_letters.remove(letter)
    
    if is_bomb:
        obj = Bomb(x, bomb_image, letter)
        bombs.append(obj)
    elif is_ice:
        obj = Ice(x, ice_image, letter)
        ices.append(obj)
    else:
        image = random.choice(list(fruits_images.values()))
        obj = Fruit(x, image, letter)
        fruits.append(obj)
    letters_active[letter] = obj

next_spawn_time = random.randint(20, 60)
next_bomb_spawn_time = random.randint(100, 200)
next_ice_spawn_time = random.randint(500, 1000)

while running:
    screen.fill(WHITE if not ice_effect else BLUE)
    pygame.mixer.init()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            key = event.unicode.upper()
            if key in letters_active:
                if isinstance(letters_active[key], Bomb):
                    pygame.mixer.Sound("assets/sword.mp3").play()
                    pygame.mixer.Sound("assets/bomb.mp3").play()
                    lives = 0
                elif isinstance(letters_active[key], Ice):
                    pygame.mixer.Sound("assets/sword.mp3").play()
                    pygame.mixer.Sound("assets/ice.mp3").play()
                    pygame.mixer.Sound("assets/sword.mp3").play()
                    ice_effect = True
                    ice_effect_duration = pygame.time.get_ticks() + random.randint(2000, 3000)
                else:
                    pygame.mixer.Sound("assets/sword.mp3").play()
                    pygame.mixer.Sound("assets/fruits.mp3").play()
                    score += 1
                    if score % 10 == 0:
                        game_speed += 5
                letters_active[key].active = False
                del letters_active[key]
                available_letters.add(key)
    
    if ice_effect and pygame.time.get_ticks() > ice_effect_duration:
        ice_effect = False
    
    if not ice_effect:
        next_spawn_time -= 1
        if next_spawn_time <= 0:
            spawn_object()
            next_spawn_time = random.randint(20, 60)
        
        next_bomb_spawn_time -= 1
        if next_bomb_spawn_time <= 0:
            spawn_object(is_bomb=True)
            next_bomb_spawn_time = random.randint(100, 200)
        
        if score >= 50:
            next_ice_spawn_time -= 1
            if next_ice_spawn_time <= 0:
                spawn_object(is_ice=True)
                next_ice_spawn_time = random.randint(300, 400)
    
    for obj_list in [fruits, ices]:
        for obj in obj_list[:]:
            obj.move()
            obj.draw(screen)
            if obj.y > HEIGHT and obj.active and not isinstance(obj, Ice):
                lives -= 1
                obj_list.remove(obj)
                if obj.letter in letters_active:
                    del letters_active[obj.letter]
                    available_letters.add(obj.letter)
    
    for obj in bombs[:]:
        obj.move()
        obj.draw(screen)
        if obj.y > HEIGHT and obj.active:
            bombs.remove(obj)
            if obj.letter in letters_active:
                del letters_active[obj.letter]
                available_letters.add(obj.letter)
    
    score_text = font.render(f"Score: {score}", True, RED)
    lives_text = font.render(f"Vies: {lives}", True, RED)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 50))
    
    if lives <= 0:
        game_over_text = font.render("GAME OVER", True, RED)
        screen.blit(game_over_text, (WIDTH//2 - 80, HEIGHT//2))
        pygame.display.update()
        pygame.time.delay(2000)
        running = False
    
    pygame.display.update()
    clock.tick(game_speed if not ice_effect else 0)

pygame.quit()
