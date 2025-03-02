import pygame
import sys
from database import Database
from game_states import GameState, HomeScreen, LevelScreen, AuthScreen
from assets.styles import Colors, Fonts
from assets.sounds import load_sounds

class CodeQuest:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Code Quest")
        
        self.clock = pygame.time.Clock()
        self.db = Database()
        self.sounds = load_sounds()
        
        self.current_user = None
        self.state = HomeScreen(self)
        
    def change_state(self, new_state):
        self.state = new_state
        
    def run(self):
        while True:
            self.clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                self.state.handle_event(event)
            
            self.screen.fill(Colors.BACKGROUND)
            self.state.update()
            self.state.draw(self.screen)
            
            pygame.display.flip()

if __name__ == "__main__":
    game = CodeQuest()
    game.run()
