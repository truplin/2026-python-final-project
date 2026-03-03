import pygame
import random
from enum import Enum
from classes.Player import Player
from classes.Enemy import Enemy
from config import *
from sprites_manager import all_sprites, enemies, bullets
# Initialize Pygame
pygame.init()



# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders - Starter")
clock = pygame.time.Clock()

# Bullet class


# Sprite groups


# Create player
player = Player()
all_sprites.add(player)

# Game variables
score = 0
font = pygame.font.Font(None, 36)
running = True

# Main game loop
while running:
    clock.tick(60)  # 60 FPS
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    
    # Update
    all_sprites.update()
    
    # Spawn enemies randomly
    if random.random() < 0.02:  # 2% chance each frame
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)
    
    # Check for bullet-enemy collisions
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        score += 10
        # Spawn a new enemy when one is destroyed
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)
    
    # Check if enemy hit player
    if pygame.sprite.spritecollide(player, enemies, True):
        running = False  # Game Over
    
    # Draw
    screen.fill(BLACK)
    all_sprites.draw(screen)
    
    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    pygame.display.flip()

# Game Over screen
game_over = True
while game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = False
    
    screen.fill(BLACK)
    game_over_text = font.render(f"Game Over! Final Score: {score}", True, RED)
    restart_text = font.render("Close window to exit", True, WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
    pygame.display.flip()
    clock.tick(30)

pygame.quit()