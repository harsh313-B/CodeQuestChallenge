import pygame
from ui.button import Button
from ui.input_box import InputBox
from assets.styles import Colors, Fonts
from levels.level_manager import LevelManager

class GameState:
    def __init__(self, game):
        self.game = game

    def handle_event(self, event):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass

class HomeScreen(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.buttons = [
            Button("Start Game", 300, 250, 200, 50),
            Button("Login", 300, 320, 200, 50),
            Button("Register", 300, 390, 200, 50)
        ]

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                if button.is_clicked(event.pos):
                    self.game.sounds['click'].play()
                    if button.text == "Start Game":
                        if self.game.current_user:
                            self.game.change_state(LevelScreen(self.game, 1))
                    elif button.text == "Login":
                        self.game.change_state(AuthScreen(self.game, is_login=True))
                    elif button.text == "Register":
                        self.game.change_state(AuthScreen(self.game, is_login=False))

    def draw(self, screen):
        # Draw title
        title = Fonts.LARGE.render("Code Quest", True, Colors.TEXT)
        screen.blit(title, (250, 100))

        # Draw buttons
        for button in self.buttons:
            button.draw(screen)

        # Draw user info if logged in
        if self.game.current_user:
            user_text = Fonts.SMALL.render(f"Logged in as: {self.game.current_user}",
                                         True, Colors.TEXT)
            screen.blit(user_text, (10, 10))

class AuthScreen(GameState):
    def __init__(self, game, is_login=True):
        super().__init__(game)
        self.is_login = is_login
        self.username_box = InputBox(250, 200, 300, 40, "Username")
        self.password_box = InputBox(250, 260, 300, 40, "Password")
        self.message = ""
        self.submit_button = Button("Submit", 300, 320, 200, 50)
        self.back_button = Button("Back", 300, 380, 200, 50)

    def handle_event(self, event):
        self.username_box.handle_event(event)
        self.password_box.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.submit_button.is_clicked(event.pos):
                self.game.sounds['click'].play()
                self.process_auth()
            elif self.back_button.is_clicked(event.pos):
                self.game.sounds['click'].play()
                self.game.change_state(HomeScreen(self.game))

    def process_auth(self):
        username = self.username_box.text
        password = self.password_box.text

        if self.is_login:
            user_id = self.game.db.login_user(username, password)
            if user_id:
                self.game.current_user = username
                self.game.change_state(HomeScreen(self.game))
            else:
                self.message = "Invalid credentials"
        else:
            if self.game.db.register_user(username, password):
                self.game.current_user = username
                self.game.change_state(HomeScreen(self.game))
            else:
                self.message = "Username already exists"

    def draw(self, screen):
        title = Fonts.LARGE.render("Login" if self.is_login else "Register",
                                 True, Colors.TEXT)
        screen.blit(title, (320, 100))

        self.username_box.draw(screen)
        self.password_box.draw(screen)
        self.submit_button.draw(screen)
        self.back_button.draw(screen)

        if self.message:
            msg_text = Fonts.SMALL.render(self.message, True, Colors.ERROR)
            screen.blit(msg_text, (250, 450))

class LevelScreen(GameState):
    def __init__(self, game, level_num):
        super().__init__(game)
        self.level_manager = LevelManager()
        self.current_level = self.level_manager.levels[level_num - 1]
        self.answer_box = InputBox(250, 350, 300, 40, "Your Answer")
        self.show_answer = False
        self.start_time = pygame.time.get_ticks()

        # Initialize buttons
        self.submit_button = Button("Submit Answer", 300, 410, 200, 50)
        self.show_answer_button = Button("Show Answer", 300, 470, 200, 50)
        self.back_button = Button("Back to Menu", 300, 530, 200, 50)

    def handle_event(self, event):
        self.answer_box.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.submit_button.is_clicked(event.pos):
                self.game.sounds['click'].play()
                self.check_answer()
            elif self.show_answer_button.is_clicked(event.pos):
                self.game.sounds['click'].play()
                self.show_answer = True
            elif self.back_button.is_clicked(event.pos):
                self.game.sounds['click'].play()
                self.game.change_state(HomeScreen(self.game))

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
        screen.blit(level_text, (320, 50))

        # Draw puzzle description (handle multiple lines)
        desc_lines = self.current_level.description.split('\n')
        y_offset = 120
        for line in desc_lines:
            desc_text = Fonts.MEDIUM.render(line, True, Colors.TEXT)
            screen.blit(desc_text, (50, y_offset))
            y_offset += 40

        # Draw puzzle-specific elements
        if 'pattern' in self.current_level.puzzle_data:
            pattern = self.current_level.puzzle_data['pattern']
            for i, line in enumerate(pattern):
                pattern_text = Fonts.MEDIUM.render(line, True, Colors.TEXT)
                screen.blit(pattern_text, (350, 200 + i * 30))

        # Draw answer box and buttons
        self.answer_box.draw(screen)
        self.submit_button.draw(screen)
        self.show_answer_button.draw(screen)
        self.back_button.draw(screen)

        # Draw correct answer if requested
        if self.show_answer:
            answer_lines = self.current_level.correct_answer.split('\n')
            y_offset = 580
            for line in answer_lines:
                answer_text = Fonts.SMALL.render(line, True, Colors.TEXT)
                screen.blit(answer_text, (50, y_offset))
                y_offset += 20