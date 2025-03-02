import pygame
from assets.styles import Colors, Fonts

class Button:
    def __init__(self, text, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.is_hovered = False
        
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
        
    def draw(self, screen):
        color = Colors.BUTTON_HOVER if self.is_hovered else Colors.BUTTON
        pygame.draw.rect(screen, color, self.rect)
        
        text_surface = Fonts.MEDIUM.render(self.text, True, Colors.TEXT)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
        # Update hover state
        self.is_hovered = self.rect.collidepoint(pygame.mouse.get_pos())
