import pygame
import random
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import time

pygame.init()
width, height = 1280, 720
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("JB Games")
clock = pygame.time.Clock()
fps = 30

font_path = 'C:/Users/Jina/Downloads/Resources/Resources/Marcellus-Regular.ttf'
bg_image = pygame.image.load('C:/Users/Jina/Downloads/Resources/Resources/BackgroundBlue.jpg')
bg_image = pygame.transform.scale(bg_image, (width, height))
balloon_image = pygame.image.load('C:/Users/Jina/Downloads/Resources/Resources/BalloonRed.png').convert_alpha()


button = pygame.Rect(500, 400, 280, 80)

def show_welcome():
    running = True
    while running:
        window.blit(bg_image, (0, 0))

        
        font = pygame.font.Font(font_path, 80)
        text = font.render("Welcome to JB Games", True, (255, 255, 255))
        window.blit(text, (180, 200))

        # Draw button
        pygame.draw.rect(window, (0, 100, 255), button, border_radius=10)
        font_btn = pygame.font.Font(font_path, 40)
        start_text = font_btn.render("START", True, (255, 255, 255))
        window.blit(start_text, (button.x + 80, button.y + 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button.collidepoint(event.pos):
                    run_game()
                    return

        pygame.display.update()
        clock.tick(fps)

def run_game():
    
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)
    detector = HandDetector(detectionCon=0.8, maxHands=1)
    rect = balloon_image.get_rect(center=(640, 600))
    speed = 8
    score = 0
    start_time = time.time()
    total_time = 30

    def reset_balloon():
        rect.x = random.randint(100, 1100)
        rect.y = 720 + 50

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return

        time_left = int(total_time - (time.time() - start_time))

        if time_left <= 0:
            window.fill((255, 255, 255))
            font = pygame.font.Font(font_path, 50)
            text = font.render(f"Time's Up! Score: {score}", True, (0, 0, 255))
            window.blit(text, (400, 320))
        else:
            success, img = cap.read()
            img = cv2.flip(img, 1)
            hands, img = detector.findHands(img, flipType=False)

            rect.y -= speed
            if rect.y < 0:
                reset_balloon()
                speed += 1

            if hands:
                x, y, _ = hands[0]['lmList'][8]
                if rect.collidepoint(x, y):
                    reset_balloon()
                    score += 10


            # Show webcam and balloon
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img_rgb = np.rot90(img_rgb)
            frame = pygame.surfarray.make_surface(img_rgb)
            frame = pygame.transform.flip(frame, True, False)
            window.blit(frame, (0, 0))
            window.blit(balloon_image, rect)

            # Show score and time
            font = pygame.font.Font(font_path, 40)
            score_text = font.render(f"Score: {score}", True, (0, 0, 255))
            time_text = font.render(f"Time: {time_left}", True, (0, 0, 255))
            window.blit(score_text, (30, 30))
            window.blit(time_text, (1100, 30))

        pygame.display.update()
        clock.tick(fps)

show_welcome()
