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

    def handle_event(self, event):
        self.username_box.handle_event(event)
        self.password_box.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos[0] > 300 and event.pos[0] < 500:
                if event.pos[1] > 320 and event.pos[1] < 370:
                    self.game.sounds['click'].play()
                    self.process_auth()

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

        if self.message:
            msg_text = Fonts.SMALL.render(self.message, True, Colors.ERROR)
            screen.blit(msg_text, (250, 400))

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