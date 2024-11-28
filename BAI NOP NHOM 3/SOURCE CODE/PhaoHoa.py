
import pygame
import random
import math
class Firework:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.explosion_particles = []
        self.exploded = False
        self.color = random.choice([(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 165, 0)])
        self.timer = random.randint(30, 60)  # Random delay before exploding

    def update(self):
        if not self.exploded:
            self.y -= 2  # Firework moves upward
            self.timer -= 1
            if self.timer <= 0:
                self.explode()
        else:
            for particle in self.explosion_particles:
                particle.update()

    def explode(self):
        self.exploded = True
        for _ in range(50):  
            angle = random.uniform(0, 2 * math.pi)  
            speed = random.uniform(1, 4)  
            self.explosion_particles.append(Particle(self.x, self.y, angle, speed, self.color))

    def draw(self, surface):
        if not self.exploded:
            pygame.draw.circle(surface, self.color, (self.x, self.y), 3)
        else:
            for particle in self.explosion_particles:
                particle.draw(surface)

class Particle:
    def __init__(self, x, y, angle, speed, color):
        self.x = x
        self.y = y
        self.vx = speed * math.cos(angle)
        self.vy = speed * math.sin(angle)
        self.lifetime = random.randint(20, 50)
        self.color = color

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.1  # Gravity effect
        self.lifetime -= 1

    def draw(self, surface):
        if self.lifetime > 0:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), 2)