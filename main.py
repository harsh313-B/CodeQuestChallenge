import pygame
import sys
from database import Database
from game_states import GameState, HomeScreen, LevelScreen, AuthScreen
from assets.styles import Colors, Fonts
from assets.sounds import load_sounds

class CodeQuest:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Set up display with error handling
        try:
            # Try hardware-accelerated mode first
            self.screen = pygame.display.set_mode((800, 600))
        except pygame.error:
            # Fallback to software rendering if hardware acceleration fails
            pygame.display.quit()
            pygame.init()
            self.screen = pygame.display.set_mode((800, 600), pygame.SWSURFACE)

        pygame.display.set_caption("Code Quest")

        # Initialize other components
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

            try:
                pygame.display.flip()
            except pygame.error:
                print("Error updating display")
                continue

if __name__ == "__main__":
    game = CodeQuest()
    game.run()