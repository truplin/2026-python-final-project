import pygame
import random
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

# Helper: draw centered text
def draw_text(surface, text, size, color, x, y):
    font = pygame.font.Font(None, size)
    txt = font.render(text, True, color)
    rect = txt.get_rect()
    rect.center = (x, y)
    surface.blit(txt, rect)


def run_game():
    """Run one playthrough. Returns True if player chose to restart, False to quit."""
    # Clear any existing sprites from previous runs
    all_sprites.empty()
    enemies.empty()
    bullets.empty()

    # Create player and initial state
    player = Player()
    all_sprites.add(player)
    score = 0
    won = False

    running = True

    font = pygame.font.Font(None, 36)

    # Main game loop
    while running:
        clock.tick(60)  # 60 FPS

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()
            # Enemy reached ground -> subtract points
            if event.type == pygame.USEREVENT + 1:
                # event contains {'points': -5}
                pts = event.__dict__.get('points', -5)
                score = max(0, score + pts)

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
            # Win condition: reach 300 points
            if score >= 300:
                won = True
                running = False
                break
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

    # Game Over / Win UI with Restart button
    button_w, button_h = 200, 50
    button_rect = pygame.Rect((SCREEN_WIDTH - button_w) // 2, SCREEN_HEIGHT // 2 + 10, button_w, button_h)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_rect.collidepoint(event.pos):
                    return True

        screen.fill(BLACK)
        if won:
            draw_text(screen, f"Congratulations! You reached {score} points!", 36, (0,200,0), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40)
        else:
            draw_text(screen, f"Game Over! Final Score: {score}", 36, RED, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40)

        # Draw restart button
        pygame.draw.rect(screen, WHITE, button_rect)
        draw_text(screen, "Restart (R)", 30, BLACK, button_rect.centerx, button_rect.centery)

        # Instruction
        draw_text(screen, "Click Restart or press R. Close window to exit.", 20, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 90)

        pygame.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    # Loop game runs until player chooses to quit
    while True:
        restart = run_game()
        if not restart:
            break

    pygame.quit()