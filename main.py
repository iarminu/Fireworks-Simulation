import pygame
import random
import math

# تنظیمات اولیه
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fireworks Simulation")

clock = pygame.time.Clock()
gravity = 0.05

# کلاس ذره
class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1, 4)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.alpha = 255
        self.color = (
            random.randint(100, 255),
            random.randint(100, 255),
            random.randint(100, 255)
        )

    def update(self):
        self.vy += gravity
        self.x += self.vx
        self.y += self.vy
        self.alpha -= 3

    def draw(self, surface):
        if self.alpha > 0:
            s = pygame.Surface((4, 4), pygame.SRCALPHA)
            pygame.draw.circle(s, (*self.color, self.alpha), (2, 2), 2)
            surface.blit(s, (self.x, self.y))

# کلاس موشک
class Firework:
    def __init__(self):
        self.x = random.randint(100, WIDTH - 100)
        self.y = HEIGHT
        self.vy = random.uniform(-5, -8)
        self.exploded = False
        self.particles = []

    def update(self):
        if not self.exploded:
            self.y += self.vy
            self.vy += gravity
            if self.vy >= 0:
                self.explode()
        else:
            for p in self.particles[:]:
                p.update()
                if p.alpha <= 0:
                    self.particles.remove(p)

    def explode(self):
        self.exploded = True
        for _ in range(100):
            self.particles.append(Particle(self.x, self.y))

    def draw(self, surface):
        if not self.exploded:
            pygame.draw.circle(surface, (255, 255, 255), (int(self.x), int(self.y)), 3)
        else:
            for p in self.particles:
                p.draw(surface)

# حلقه اصلی
fireworks = []
running = True

while running:
    clock.tick(60)
    screen.fill((0, 0, 20))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            fireworks.append(Firework())

    if random.random() < 0.02:
        fireworks.append(Firework())

    for fw in fireworks[:]:
        fw.update()
        fw.draw(screen)
        if fw.exploded and len(fw.particles) == 0:
            fireworks.remove(fw)

    pygame.display.flip()

pygame.quit()
