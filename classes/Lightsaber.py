import pygame
from config import *

class Lightsaber(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y):
        super().__init__()
        # Create a lightsaber visual (rectangular with glow effect)
        self.image = pygame.Surface((60, 8), pygame.SRCALPHA)
        # Draw the lightsaber blade
        pygame.draw.rect(self.image, (0, 255, 0), (0, 2, 60, 4))  # Green blade
        pygame.draw.rect(self.image, (150, 255, 150), (0, 1, 60, 2))  # Glow effect top
        pygame.draw.rect(self.image, (150, 255, 150), (0, 5, 60, 2))  # Glow effect bottom
        
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        
        # Calculate direction towards player
        dx = target_x - x
        dy = target_y - y
        distance = (dx**2 + dy**2)**0.5
        if distance > 0:
            self.vel_x = (dx / distance) * 10  # Reduced from 12 to 10
            self.vel_y = (dy / distance) * 10
        else:
            self.vel_x = 0
            self.vel_y = 10
            
        # Create mask for pixel-perfect collision
        try:
            self.mask = pygame.mask.from_surface(self.image)
        except Exception:
            self.mask = None

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        
        # Remove if off screen
        if (self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or 
            self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT):
            self.kill()
