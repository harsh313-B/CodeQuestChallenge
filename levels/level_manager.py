import pygame
from ui.button import Button
from assets.styles import Colors, Fonts

class Level:
    def __init__(self, number, question, answer, hint):
        self.number = number
        self.question = question
        self.answer = answer
        self.hint = hint
        self.start_time = None
        
class LevelManager:
    def __init__(self):
        self.levels = [
            Level(1, "What is the output of: print(2 + '2')?",
                  "TypeError", "Think about data types!"),
            Level(2, "Complete the sequence: for i in _____(5):",
                  "range", "How do we count from 0 to 4?"),
            Level(3, "What method converts 'hello' to 'HELLO'?",
                  "upper", "Look for case transformation"),
            Level(4, "What symbol creates a comment in Python?",
                  "#", "It's not a programming operator"),
            Level(5, "What function returns list length?",
                  "len", "How do we measure collection size?")
        ]

class LevelScreen(GameState):
    def __init__(self, game, level_num):
        super().__init__(game)
        self.level_manager = LevelManager()
        self.current_level = self.level_manager.levels[level_num - 1]
        self.answer_box = InputBox(250, 300, 300, 40, "Answer")
        self.show_hint = False
        self.start_time = pygame.time.get_ticks()
        
    def handle_event(self, event):
        self.answer_box.handle_event(event)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check submit button
            if event.pos[0] > 300 and event.pos[0] < 500:
                if event.pos[1] > 360 and event.pos[1] < 410:
                    self.check_answer()
                    
            # Check hint button
            if event.pos[0] > 300 and event.pos[0] < 500:
                if event.pos[1] > 420 and event.pos[1] < 470:
                    self.show_hint = True
                    
    def check_answer(self):
        if self.answer_box.text.lower() == self.current_level.answer.lower():
            time_taken = (pygame.time.get_ticks() - self.start_time) / 1000
            score = max(100 - int(time_taken), 10)
            
            self.game.db.save_score(
                self.game.current_user,
                self.current_level.number,
                score,
                time_taken
            )
            
            if self.current_level.number < 5:
                self.game.change_state(LevelScreen(self.game,
                                                 self.current_level.number + 1))
            else:
                self.game.change_state(HomeScreen(self.game))
                
    def draw(self, screen):
        # Draw level number
        level_text = Fonts.LARGE.render(f"Level {self.current_level.number}",
                                      True, Colors.TEXT)
        screen.blit(level_text, (320, 100))
        
        # Draw question
        question_text = Fonts.MEDIUM.render(self.current_level.question,
                                          True, Colors.TEXT)
        screen.blit(question_text, (100, 200))
        
        # Draw answer box
        self.answer_box.draw(screen)
        
        # Draw buttons
        submit_btn = Button("Submit", 300, 360, 200, 50)
        hint_btn = Button("Show Hint", 300, 420, 200, 50)
        
        submit_btn.draw(screen)
        hint_btn.draw(screen)
        
        # Draw hint if requested
        if self.show_hint:
            hint_text = Fonts.SMALL.render(f"Hint: {self.current_level.hint}",
                                         True, Colors.TEXT)
            screen.blit(hint_text, (100, 500))
