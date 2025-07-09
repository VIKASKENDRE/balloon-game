import pygame
from config import FONT, DIFFICULTY_SETTINGS

def main_menu(screen, width, height, high_score, selected_difficulty):
    menu_running = True
    while menu_running:
        screen.fill((255,255,255))
        title = FONT.render("Balloon Burst Game", True, (0,0,0))
        start_text = FONT.render("Press S to Start", True, (0,0,0))
        quit_text = FONT.render("Press Q to Quit", True, (0,0,0))
        difficulty_text = FONT.render(f"Difficulty: {selected_difficulty} (Press D to Change)", True, (0,0,0))
        highscore_text = FONT.render(f"High Score: {high_score}", True, (0,0,0))

        screen.blit(title, (width//2 - title.get_width()//2, height//2 - 150))
        screen.blit(start_text, (width//2 - start_text.get_width()//2, height//2 - 50))
        screen.blit(quit_text, (width//2 - quit_text.get_width()//2, height//2))
        screen.blit(difficulty_text, (width//2 - difficulty_text.get_width()//2, height//2 + 50))
        screen.blit(highscore_text, (width//2 - highscore_text.get_width()//2, height//2 + 100))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    menu_running = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()
                if event.key == pygame.K_d:
                    levels = list(DIFFICULTY_SETTINGS.keys())
                    curr_index = levels.index(selected_difficulty)
                    selected_difficulty = levels[(curr_index + 1) % len(levels)]
    return selected_difficulty
