# Player class
import pygame
from classes.Bullet import Bullet
from config import *
from sprites_manager import all_sprites, bullets
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Try to load the player image from assets, fall back to a colored rect
        try:
            BASE_DIR = __file__
            # construct path relative to project root
            import os
            base = os.path.dirname(os.path.abspath(__file__))
            img_path = os.path.join(base, '..', 'assets', 'player.png')
            self.image = pygame.image.load(img_path).convert_alpha()
            # scale to be slightly taller (width 120, height 110)
            self.image = pygame.transform.scale(self.image, (120, 110))
        except Exception:
            self.image = pygame.Surface((50, 40))
            self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)