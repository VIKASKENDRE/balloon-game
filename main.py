import pygame
from config import WIDTH, HEIGHT
from menu import main_menu
from utils import calibrate_distance, load_highscore
from game import run_game

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Balloon Burst Game")

# Calibration
calibrated_distance = calibrate_distance()

# Load high score
high_score = load_highscore()

# Main loop
selected_difficulty = 'Medium'
while True:
    selected_difficulty = main_menu(screen, WIDTH, HEIGHT, high_score, selected_difficulty)
    run_game(screen, selected_difficulty)
