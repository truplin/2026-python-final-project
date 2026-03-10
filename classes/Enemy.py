import pygame
import random
from config import *
# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(2, 5)

    def update(self):
        self.rect.y += self.speed
        # Remove if off screen
        if self.rect.top > SCREEN_HEIGHT:
            # Notify the game that an enemy reached the ground so score can be adjusted
            try:
                evt = pygame.event.Event(pygame.USEREVENT + 1, {'points': -5})
                pygame.event.post(evt)
            except Exception:
                pass
            self.kill()