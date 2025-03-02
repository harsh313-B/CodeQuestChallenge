import pygame

class Colors:
    BACKGROUND = (20, 20, 40)
    TEXT = (255, 255, 255)
    BUTTON = (60, 60, 100)
    BUTTON_HOVER = (80, 80, 120)
    ERROR = (255, 0, 0)
    INPUT_BOX = (40, 40, 60)
    INPUT_TEXT = (200, 200, 200)

class Fonts:
    pygame.font.init()
    LARGE = pygame.font.Font(None, 64)
    MEDIUM = pygame.font.Font(None, 32)
    SMALL = pygame.font.Font(None, 24)
