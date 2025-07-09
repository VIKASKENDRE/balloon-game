import pygame

# Screen settings
WIDTH = 1280
HEIGHT = 720

# Initialize pygame fonts globally
pygame.font.init()
FONT = pygame.font.SysFont(None, 48)

# Difficulty settings
DIFFICULTY_SETTINGS = {
    'Easy': {'speed_range': (1,2), 'spawn_chance': 40},
    'Medium': {'speed_range': (1,3), 'spawn_chance': 30},
    'Hard': {'speed_range': (2,4), 'spawn_chance': 20}
}

# High score file
HIGHSCORE_FILE = 'highscore.txt'

# Camera index (0 = inbuilt, 1 = USB cam)
CAMERA_INDEX = 0

# Game duration (seconds)
GAME_DURATION = 60
