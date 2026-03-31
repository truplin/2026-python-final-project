import pygame
import random
from config import *
from classes.Lightsaber import Lightsaber
from sprites_manager import all_sprites, lightsabers

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load boss image from assets
        import os
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        boss_path = os.path.join(BASE_DIR, 'assets', 'Boss.png.jpg')
        
        try:
            self.image = pygame.image.load(boss_path).convert_alpha()
            # Scale the boss image to appropriate size
            self.image = pygame.transform.scale(self.image, (80, 80))
        except Exception as e:
            print(f"Could not load boss image at {boss_path}: {e}")
            # Fallback to programmatically drawn boss
            self.image = pygame.Surface((80, 80), pygame.SRCALPHA)
            # Draw boss as a dark lord figure
            pygame.draw.rect(self.image, (50, 0, 50), (20, 10, 40, 50))  # Body
            pygame.draw.circle(self.image, (100, 0, 100), (40, 25), 15)  # Head
            # Draw red lightsaber hilt
            pygame.draw.rect(self.image, (150, 150, 150), (35, 55, 10, 15))
        
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.y = 50
        
        # Boss properties - moderate difficulty
        self.max_lives = 15  # Reduced from 25 to 15
        self.lives = self.max_lives
        self.speed = 4  # Reduced from 6 to 4
        self.direction = 1  # 1 for right, -1 for left
        self.shoot_cooldown = 0
        self.shoot_delay = 30  # Increased from 20 to 30 (still faster than original 60)
        self.rage_mode = False  # Rage mode when health is low
        
        # Create mask for pixel-perfect collision
        try:
            self.mask = pygame.mask.from_surface(self.image)
        except Exception:
            self.mask = None

    def update(self, player_x, player_y):
        # Move boss left and right
        self.rect.x += self.speed * self.direction
        
        # Change direction when hitting screen edges
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.direction *= -1
            
        # Check for rage mode (when health is below 40%)
        if self.lives < self.max_lives * 0.4 and not self.rage_mode:
            self.rage_mode = True
            self.speed = 5  # Slightly faster in rage mode
            self.shoot_delay = 20  # Faster shooting in rage mode
            
        # Handle shooting
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
            
        if self.shoot_cooldown <= 0:
            # In rage mode, occasionally shoot double lightsabers
            if self.rage_mode and random.random() < 0.3:  # 30% chance for double shot
                self.shoot_lightsaber(player_x - 30, player_y)
                self.shoot_lightsaber(player_x + 30, player_y)
            else:
                self.shoot_lightsaber(player_x, player_y)
            self.shoot_cooldown = self.shoot_delay

    def shoot_lightsaber(self, target_x, target_y):
        """Shoot a lightsaber towards the player"""
        lightsaber = Lightsaber(self.rect.centerx, self.rect.bottom, target_x, target_y)
        all_sprites.add(lightsaber)
        lightsabers.add(lightsaber)
        return lightsaber

    def take_damage(self):
        """Reduce boss lives when hit"""
        self.lives -= 1
        return self.lives <= 0  # Return True if boss is defeated

    def draw_health_bar(self, screen):
        """Draw boss health bar above the boss"""
        bar_width = 200
        bar_height = 10
        bar_x = SCREEN_WIDTH // 2 - bar_width // 2
        bar_y = 20
        
        # Draw background (red)
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
        
        # Draw current health (green)
        health_percentage = self.lives / self.max_lives
        health_width = int(bar_width * health_percentage)
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, health_width, bar_height))
        
        # Draw border
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)
