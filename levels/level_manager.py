import pygame
from assets.styles import Colors, Fonts
from ui.button import Button

class Level:
    def __init__(self, number, description, puzzle_data, answer, correct_answer):
        self.number = number
        self.description = description
        self.puzzle_data = puzzle_data
        self.answer = answer
        self.correct_answer = correct_answer
        self.start_time = None

class LevelManager:
    def __init__(self):
        self.levels = [
            Level(1, 
                "Debug the Code!\nFind and fix the error in this Python code:\n\ndef greet(name)\nprint('Hello, ' + name)",
                {"code": "def greet(name)\nprint('Hello, ' + name)",
                 "expected_output": "Hello, Alice"},
                ":", 
                "Correct answer: Add ':' after function definition\ndef greet(name):\nprint('Hello, ' + name)"),

            Level(2,
                "Complete the Pattern!\nWhat symbol completes this pattern?\n\n# * * *\n# * _ *\n# * * *",
                {"pattern": ["* * *", "* _ *", "* * *"]},
                "*",
                "Correct answer: '*' completes the symmetrical pattern\n* * *\n* * *\n* * *"),

            Level(3,
                "Decode the Message!\nEach number represents a letter position (A=1, B=2, etc):\n\n16 25 20 8 15 14",
                {"encoded": "16 25 20 8 15 14",
                 "cipher": "position"},
                "python",
                "Correct answer: PYTHON\n16=P, 25=Y, 20=T, 8=H, 15=O, 14=N"),

            Level(4,
                "Fix the Logic!\nWhat operator fixes this code?\n\nif age [] 18:\n    print('Adult')\nelse:\n    print('Minor')",
                {"code": "if age [] 18:",
                 "options": [">=", "<=", "==", "!="]},
                ">=",
                "Correct answer: '>='\nif age >= 18:\n    print('Adult')\nelse:\n    print('Minor')"),

            Level(5,
                "Complete the Sequence!\nWhat's the missing operator?\n\nresult = 10 [] 2 [] 3\nprint(result)  # Output: 5",
                {"sequence": "10 [] 2 [] 3",
                 "target": 5},
                "/ +",
                "Correct answer: '/ +'\nresult = 10 / 2 + 3\nprint(result)  # Output: 5")
        ]

class InputBox:
    def __init__(self, x, y, w, h, text=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = Colors.INPUT_BOX
        self.text = text
        self.txt_surface = Fonts.MEDIUM.render(text, True, Colors.TEXT)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = Fonts.MEDIUM.render(self.text, True, Colors.TEXT)

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

class HomeScreen:
    def __init__(self, game):
        pass

    def handle_event(self, event):
        pass

    def draw(self, screen):
        pass