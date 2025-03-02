import pygame
from assets.styles import Colors, Fonts

class InputBox:
    def __init__(self, x, y, width, height, placeholder=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""
        self.placeholder = placeholder
        self.active = False
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
                
    def draw(self, screen):
        pygame.draw.rect(screen, Colors.INPUT_BOX, self.rect, 2)
        
        if self.text:
            text_surface = Fonts.MEDIUM.render(self.text, True, Colors.INPUT_TEXT)
        else:
            text_surface = Fonts.MEDIUM.render(self.placeholder, True,
                                             Colors.INPUT_TEXT)
            
        text_rect = text_surface.get_rect(x=self.rect.x + 5,
                                        centery=self.rect.centery)
        screen.blit(text_surface, text_rect)
