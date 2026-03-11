import pygame
import random
from classes.Player import Player
from classes.Enemy import Enemy
from config import *
from sprites_manager import all_sprites, enemies, bullets

# Import level configs
import level_1
import level_2

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


def run_level(target_score: int, spawn_chance: float, speed_min: int, speed_max: int, level_num: int = 1):
    """Run a single level with configurable difficulty.

    Returns 'next' if level won, 'restart' if player chose restart, or 'quit'.
    """
    # Clear any existing sprites from previous runs
    all_sprites.empty()
    enemies.empty()
    bullets.empty()

    # Create player and initial state
    player = Player()
    all_sprites.add(player)
    score = 0
    level_won = False

    running = True

    font = pygame.font.Font(None, 36)

    # Main game loop
    while running:
        clock.tick(60)  # 60 FPS

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()
            # Enemy reached ground -> subtract points
            if event.type == pygame.USEREVENT + 1:
                pts = event.__dict__.get('points', -5)
                score = max(0, score + pts)

        # Update
        all_sprites.update()

        # Spawn enemies with configured chance and speed
        if random.random() < spawn_chance:
            enemy = Enemy()
            # override enemy speed for difficulty
            enemy.speed = random.randint(speed_min, speed_max)
            all_sprites.add(enemy)
            enemies.add(enemy)

        # Check for bullet-enemy collisions
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in hits:
            score += 10
            if score >= target_score:
                level_won = True
                running = False
                break
            # Spawn a replacement enemy with configured speed
            enemy = Enemy()
            enemy.speed = random.randint(speed_min, speed_max)
            all_sprites.add(enemy)
            enemies.add(enemy)

        # Check if enemy hit player
        if pygame.sprite.spritecollide(player, enemies, True):
            running = False  # Level failed / Game Over

        # Draw
        screen.fill(BLACK)
        all_sprites.draw(screen)

        # Draw level and score
        header = font.render(f"Level {level_num} - Target: {target_score}", True, WHITE)
        screen.blit(header, (10, 10))
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 40))

        pygame.display.flip()

    # End-of-level UI: Next (if won), Restart, Quit
    button_w, button_h = 200, 50
    center_x = SCREEN_WIDTH // 2
    next_rect = pygame.Rect(center_x - button_w - 10, SCREEN_HEIGHT // 2 + 10, button_w, button_h)
    restart_rect = pygame.Rect(center_x + 10, SCREEN_HEIGHT // 2 + 10, button_w, button_h)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return 'restart'
                if event.key == pygame.K_RETURN and level_won:
                    return 'next'
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if level_won and next_rect.collidepoint(event.pos):
                    return 'next'
                if restart_rect.collidepoint(event.pos):
                    return 'restart'

        screen.fill(BLACK)
        if level_won:
            draw_text(screen, f"Level {level_num} Complete! Score: {score}", 36, (0,200,0), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40)
        else:
            draw_text(screen, f"Game Over! Level {level_num} Score: {score}", 36, RED, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40)

        # Draw buttons
        if level_won:
            pygame.draw.rect(screen, WHITE, next_rect)
            draw_text(screen, "Next Level", 28, BLACK, next_rect.centerx, next_rect.centery)
        else:
            # show disabled next
            pygame.draw.rect(screen, (120,120,120), next_rect)
            draw_text(screen, "Next Level", 22, (60,60,60), next_rect.centerx, next_rect.centery)

        pygame.draw.rect(screen, WHITE, restart_rect)
        draw_text(screen, "Restart (R)", 28, BLACK, restart_rect.centerx, restart_rect.centery)

        draw_text(screen, "Click Next/Restart or press Enter/R. Close window to exit.", 20, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 90)

        pygame.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    # Run Level 1 then Level 2 (harder) when Level 1 is completed
    while True:
        res = run_level(level_1.TARGET, spawn_chance=level_1.SPAWN_CHANCE, speed_min=level_1.SPEED_MIN, speed_max=level_1.SPEED_MAX, level_num=level_1.LEVEL_NUM)
        if res == 'quit':
            break
        if res == 'restart':
            continue
        if res == 'next':
            # Level 2: harder settings, target 500
            res2 = run_level(level_2.TARGET, spawn_chance=level_2.SPAWN_CHANCE, speed_min=level_2.SPEED_MIN, speed_max=level_2.SPEED_MAX, level_num=level_2.LEVEL_NUM)
            if res2 == 'quit':
                break
            if res2 == 'restart':
                continue
            if res2 == 'next':
                # Completed both levels: show final congrats then restart loop
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            raise SystemExit
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                            break
                    screen.fill(BLACK)
                    draw_text(screen, "Congratulations! You beat all levels!", 36, (0,200,0), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40)
                    draw_text(screen, "Press R to restart or close window to quit.", 20, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)
                    pygame.display.flip()
                    clock.tick(30)

    pygame.quit()