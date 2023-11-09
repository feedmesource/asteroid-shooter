import math
import pygame
import random

pygame.init()
my_font = pygame.font.SysFont("monospace", 20, bold=True)

display_width = 1000
display_height = 800
screen = pygame.display.set_mode((display_width, display_height))

clock = pygame.time.Clock()

run = True

class Ship():
    def __init__(self, start_x, start_y) -> None:
        self.x = start_x
        self.y = start_y
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        if self.x < 0:
            self.x = 0
        elif self.x > display_width:
            self.x = display_width
        if self.y < 0:
            self.y = 0
        elif self.y > display_height:
            self.y = display_height

class Bullet():
    def __init__(self, start_x, start_y) -> None:
        self.x = start_x
        self.y = start_y
    def move(self):
        self.y -= 10

class Asteroid():
    biggest_size = 55
    
    def __init__(self, start_x, start_y, speed, size) -> None:
        self.x = start_x
        self.y = start_y
        self.speed = speed
        self.size = size
    def move(self):
        self.y += self.speed
        if self.y > display_height + self.biggest_size:
            self.y = -self.biggest_size

ship = Ship (display_width / 2, display_height / 2)
bullets = []
asteroids = []
score = 0

def generate_random_asteroid():
    rand_start_x = random.randint(0, display_width)
    rand_start_y = random.randint(-2 * Asteroid.biggest_size, display_height / 4)
    rand_speed = random.randint(1, 2)
    rand_size = random.randint(7, Asteroid.biggest_size)

    asteroid = Asteroid(rand_start_x, rand_start_y, rand_speed, rand_size)
    return asteroid

count_of_asteroids = 25

for i in range(count_of_asteroids):
    asteroid = generate_random_asteroid()
    asteroids.append(asteroid)


def distance (ax, ay, bx, by) -> float:
    return math.sqrt((ax-bx)**2 + (ay - by)**2)

exit = False

while run:    
    background_color = pygame.Color(66,37,4,204)
    screen.fill(background_color)
    
    events = pygame.event.get()
    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]: ship.move(0, -5)
    if keys[pygame.K_DOWN]: ship.move(0, 5)
    if keys[pygame.K_LEFT]: ship.move(-5, 0)
    if keys[pygame.K_RIGHT]: ship.move(5, 0)
        
    pygame.draw.polygon(screen, "#FFFFFF", [[ship.x, ship.y], [ship.x - 10, ship.y + 30],  [ship.x + 10, ship.y + 30]], 2)

    for asteroid in asteroids:
        dist = distance(asteroid.x, asteroid.y, ship.x, ship.y)
        if dist <= asteroid.size:
            run = False

        asteroid.move()
        pygame.draw.circle(screen, "#FFFFFF", [asteroid.x, asteroid.y], asteroid.size, 2)
    
    for event in events:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bullet = Bullet(ship.x, ship.y)
            bullets.append(bullet)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE or event.type == pygame.QUIT:
            run = False
            exit = True
        
    
    for bullet in bullets:
        bullet.move()
        pygame.draw.circle(screen, "#FFFFFF", [bullet.x, bullet.y], 5, 2)
        if bullet.y < -5:
            bullets.remove(bullet)
            continue
        for asteroid in asteroids:
            dist = distance(bullet.x, bullet.y, asteroid.x, asteroid.y)
            if dist - 5 - asteroid.size <= 0:
                score += round(asteroid.size, -1)
                asteroids.remove(asteroid)
                bullets.remove(bullet)
                new_asteroid = generate_random_asteroid()
                asteroids.append(new_asteroid)
                break

    # render text
    label = my_font.render(f"Score: {score}", 1, (200,0,150), background_color.normalize())
    screen.blit(label, (0, 0))

    pygame.display.update()

    clock.tick(60)


if not exit:
    game_over_font = pygame.font.SysFont("monospace", 80, True)
    game_over_text = game_over_font.render("You lost!", 1, "RED")
    text_rect = game_over_text.get_rect(center=(display_width / 2, display_height / 2))
    screen.blit(game_over_text, text_rect)
    pygame.display.update()

while(not exit):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE) or event.type == pygame.QUIT:
            run = False
            exit = True

pygame.quit()
