import pygame
import random
from classes.Player import Player
from classes.Enemy import Enemy
from config import *
from sprites_manager import all_sprites, enemies, bullets
import os

# Import level configs
import level_1
import level_2

# Initialize Pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders - Starter")
clock = pygame.time.Clock()

# Load background image (safe: prints error and falls back to solid fill)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
bg_path = os.path.join(BASE_DIR, 'assets', 'Backround.png')
background = None
try:
    background = pygame.image.load(bg_path)
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT)).convert()
except Exception as e:
    print(f"Could not load background image at {bg_path}: {e}")

# Load and play background music (safe: prints error and continues without music)
music_path = os.path.join(BASE_DIR, 'assets', 'YTDown.com_YouTube_Star-Wars-Main-Theme-Full_Media_D0ZQPqeJkk_007_128k.mp3')
try:
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.set_volume(0.3)  # Set volume to 30%
    pygame.mixer.music.play(-1)  # Loop indefinitely
    print(f"Playing background music from {music_path}")
except Exception as e:
    print(f"Could not load background music at {music_path}: {e}")
    print("To add music, place a file named 'background_music.mp3' in the assets folder")

# Helper: draw centered text
def draw_text(surface, text, size, color, x, y):
    font = pygame.font.Font(None, size)
    txt = font.render(text, True, color)
    rect = txt.get_rect()
    rect.center = (x, y)
    surface.blit(txt, rect)


def show_start_screen():
    """Display the start screen with title and start button"""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    return 'start'
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Check if start button was clicked
                start_button_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 50, 200, 50)
                credits_button_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 120, 200, 50)
                if start_button_rect.collidepoint(event.pos):
                    return 'start'
                if credits_button_rect.collidepoint(event.pos):
                    return 'credits'

        # Draw background
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill(BLACK)
        
        # Draw title
        draw_text(screen, "Galactic Adventures", 72, (100, 200, 255), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)
        
        # Draw start button
        start_button_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 50, 200, 50)
        pygame.draw.rect(screen, (100, 200, 255), start_button_rect)
        draw_text(screen, "START", 36, BLACK, start_button_rect.centerx, start_button_rect.centery)
        
        # Draw credits button
        credits_button_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 120, 200, 50)
        pygame.draw.rect(screen, (150, 150, 255), credits_button_rect)
        draw_text(screen, "CREDITS", 36, BLACK, credits_button_rect.centerx, credits_button_rect.centery)
        
        # Draw instructions
        draw_text(screen, "Press SPACE or ENTER to start", 24, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200)
        draw_text(screen, "Click START button or close window to quit", 20, (150, 150, 150), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 230)

        pygame.display.flip()
        clock.tick(30)


def show_credits_screen():
    """Display the credits screen"""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    return 'back'
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Check if back button was clicked
                back_button_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 150, 200, 50)
                if back_button_rect.collidepoint(event.pos):
                    return 'back'

        # Draw background
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill(BLACK)
        
        # Draw title
        draw_text(screen, "CREDITS", 72, (100, 200, 255), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 150)
        
        # Draw credits information
        draw_text(screen, "Writer: Tate Ruplin", 36, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30)
        draw_text(screen, "Co Writer: AI", 36, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)
        draw_text(screen, "Song Writer: John Williams", 36, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70)
        
        # Draw back button
        back_button_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 150, 200, 50)
        pygame.draw.rect(screen, (200, 100, 100), back_button_rect)
        draw_text(screen, "BACK", 36, BLACK, back_button_rect.centerx, back_button_rect.centery)
        
        # Draw instructions
        draw_text(screen, "Press ESC, SPACE, or ENTER to go back", 20, (150, 150, 150), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 220)

        pygame.display.flip()
        clock.tick(30)


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
            # Enemy reached ground -> subtract points (1 point in level 1, 3 points in level 2, 5 points in other levels)
            if event.type == pygame.USEREVENT + 1:
                if level_num == 1:
                    pts = -1  # Level 1: deduct 1 point
                elif level_num == 2:
                    pts = -3  # Level 2: deduct 3 points
                else:
                    pts = event.__dict__.get('points', -5)  # Other levels: deduct 5 points
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

        # Check for bullet-enemy collisions (pixel-perfect using masks)
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True, pygame.sprite.collide_mask)
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

        # Check if enemy hit player (pixel-perfect)
        if pygame.sprite.spritecollide(player, enemies, True, pygame.sprite.collide_mask):
            running = False  # Level failed / Game Over

        # Draw background (use image when available, otherwise solid fill)
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill(BLACK)
        # Draw sprites on top
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
    # Show start screen first
    while True:
        start_result = show_start_screen()
        if start_result == 'quit':
            break
        if start_result == 'credits':
            credits_result = show_credits_screen()
            if credits_result == 'quit':
                break
            # If back was pressed, continue the loop to show start screen again
            continue
        if start_result == 'start':
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
                            draw_text(screen, "Press R to return to start screen or close window to quit.", 20, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)
                            pygame.display.flip()
                            clock.tick(30)
                        break  # Return to start screen
            # After completing or quitting levels, loop back to start screen

    pygame.quit()