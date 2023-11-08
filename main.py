import math
import pygame
import random


pygame.init()
myfont = pygame.font.SysFont("monospace", 20, bold=True)


screen = pygame.display.set_mode((800, 800))

clock = pygame.time.Clock()

run = True

class Ship():
    def __init__(self, startx, starty) -> None:
        self.x = startx
        self.y = starty
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        if self.x < 0:
            self.x = 0
        elif self.x > 800:
            self.x = 800
        if self.y < 0:
            self.y = 0
        elif self.y > 800:
            self.y = 800

class Bullet():
    def __init__(self, startx, starty) -> None:
        self.x = startx
        self.y = starty
    def move(self):
        self.y -= 20

class Asteroid():
    def __init__(self, startx, starty, speed, size) -> None:
        self.x = startx
        self.y = starty
        self.speed = speed
        self.size = size
    def move(self):
        self.y += self.speed
        if self.y > 840:
            self.y = -40

ship = Ship (400, 400)
bullets = []
asteroids = []
score = 0

def generate_random_asteroid():
    rand_startx = random.randint(0, 800)
    rand_starty = random.randint(0, 200)
    rand_speed = random.randint(1, 4)
    rand_size = random.randint(8, 40)

    asteroid = Asteroid(rand_startx, rand_starty, rand_speed, rand_size)
    return asteroid

for i in range(30):
    asteroid = generate_random_asteroid()
    asteroids.append(asteroid)


def distance (ax, ay, bx, by) -> float:
    return math.sqrt((ax-bx)**2 + (ay - by)**2)

while run:
        
    screen.fill("BLUE")
    events = pygame.event.get()
    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]: ship.move(0, -10)
    if keys[pygame.K_DOWN]: ship.move(0, 10)
    if keys[pygame.K_LEFT]: ship.move(-10, 0)
    if keys[pygame.K_RIGHT]: ship.move(10, 0)
        
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
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            run = False
        
    
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
    label = myfont.render(f"Score: {score}", 1, (255,0,0))
    screen.blit(label, (0, 0))

    pygame.display.update()

    clock.tick(30)
pygame.quit()
