import pygame
import random
import threading
import time
import cv2
import mediapipe as mp

from config import WIDTH, HEIGHT, FONT, DIFFICULTY_SETTINGS, GAME_DURATION, CAMERA_INDEX
from utils import save_highscore
from utils import load_highscore

# Mediapipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Global palm positions
palm_positions = []
calibrated_distance = 150
palm_radius = 30

class Balloon:
    def __init__(self, selected_difficulty, balloon_img, burst_img):
        self.x = random.randint(50, WIDTH - 50)
        self.y = HEIGHT
        self.radius = 30
        speed_min, speed_max = DIFFICULTY_SETTINGS[selected_difficulty]['speed_range']
        self.speed = random.uniform(speed_min, speed_max)
        self.burst = False
        self.burst_timer = 0
        self.balloon_img = balloon_img
        self.burst_img = burst_img

    def move(self):
        self.y -= self.speed

    def draw(self, screen):
        img = self.burst_img if self.burst else self.balloon_img
        img_resized = pygame.transform.scale(img, (self.radius*2, self.radius*2))
        screen.blit(img_resized, (int(self.x - self.radius), int(self.y - self.radius)))

def camera_thread_func():
    global palm_positions, palm_radius
    cap = cv2.VideoCapture(CAMERA_INDEX)

    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        palm_positions = []

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                cx, cy = int(hand_landmarks.landmark[9].x * WIDTH), int(hand_landmarks.landmark[9].y * HEIGHT)
                palm_positions.append((cx, cy))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def run_game(screen, selected_difficulty):
    global palm_positions
    balloons = []
    score = 0

    # Load assets
    balloon_img = pygame.image.load('assets/balloon.png').convert_alpha()
    burst_img = pygame.image.load('assets/burst.png').convert_alpha()
    pop_sound = pygame.mixer.Sound('assets/pop.wav')

    # Start background music
    pygame.mixer.music.load('assets/bg_music.wav')
    pygame.mixer.music.play(-1)

    # Start camera thread
    threading.Thread(target=camera_thread_func, daemon=True).start()

    start_time = time.time()
    running = True

    while running:
        elapsed_time = time.time() - start_time
        if elapsed_time >= GAME_DURATION:
            running = False

        screen.fill((135, 206, 250))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Add new balloons based on difficulty
        if random.randint(1, DIFFICULTY_SETTINGS[selected_difficulty]['spawn_chance']) == 1:
            balloons.append(Balloon(selected_difficulty, balloon_img, burst_img))

        # Update and draw balloons
        for balloon in balloons[:]:
            balloon.move()
            balloon.draw(screen)

            for pos in palm_positions:
                dx = balloon.x - pos[0]
                dy = balloon.y - pos[1]
                distance = (dx**2 + dy**2)**0.5
                if distance < balloon.radius + 10:
                    if not balloon.burst:
                        balloon.burst = True
                        balloon.burst_timer = pygame.time.get_ticks()
                        pop_sound.play()
                        score += 1

            if balloon.burst and pygame.time.get_ticks() - balloon.burst_timer > 200:
                balloons.remove(balloon)

            if balloon.y < -50:
                balloons.remove(balloon)

        # Draw palm dots
        for pos in palm_positions:
            pygame.draw.circle(screen, (0, 0, 255), pos, 10)

        # Draw score and timer
        score_text = FONT.render(f"Score: {score}", True, (0, 0, 0))
        timer_text = FONT.render(f"Time: {int(GAME_DURATION - elapsed_time)}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))
        screen.blit(timer_text, (10, 60))

        pygame.display.flip()
        pygame.time.Clock().tick(30)

    # Check and save high score
    high_score = load_highscore()
    if score > high_score:
        save_highscore(score)
        high_score = score

    # Game over screen
    screen.fill((255, 255, 255))
    over_text = FONT.render("Game Over!", True, (0, 0, 0))
    final_score = FONT.render(f"Score: {score}", True, (0, 0, 0))
    highscore_text = FONT.render(f"High Score: {high_score}", True, (0, 0, 0))

    screen.blit(over_text, (WIDTH//2 - over_text.get_width()//2, HEIGHT//2 - 80))
    screen.blit(final_score, (WIDTH//2 - final_score.get_width()//2, HEIGHT//2 - 30))
    screen.blit(highscore_text, (WIDTH//2 - highscore_text.get_width()//2, HEIGHT//2 + 20))
    pygame.display.flip()
    pygame.time.wait(5000)
