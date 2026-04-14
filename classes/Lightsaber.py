import pygame
from config import *

class Lightsaber(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y):
        super().__init__()
        # Load lightsaber image from assets
        import os
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        lightsaber_path = os.path.join(BASE_DIR, 'assets', 'Lightsaber.png.jpg')
        
        try:
            self.image = pygame.image.load(lightsaber_path).convert_alpha()
            # Scale lightsaber image to be skinnier
            self.image = pygame.transform.scale(self.image, (100, 6))  # Skinnier width
        except Exception as e:
            print(f"Could not load lightsaber image at {lightsaber_path}: {e}")
            # Fallback to programmatically drawn lightsaber
            self.image = pygame.Surface((100, 6), pygame.SRCALPHA)
            # Draw the lightsaber blade
            pygame.draw.rect(self.image, (0, 255, 0), (0, 1, 100, 4))  # Green blade
            pygame.draw.rect(self.image, (150, 255, 150), (0, 0, 100, 1))  # Glow effect top
            pygame.draw.rect(self.image, (150, 255, 150), (0, 5, 100, 1))  # Glow effect bottom
        
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
