from .SceneBase import SceneBase
from widgets import Picker, Button
from models.game import Board, Player
from models.game.bots import BotLoader
from services import ImageService, FontService, SceneManager, SettingsService as Settings


class SetupGame(SceneBase):
    """
    This scene shows a graphical representation of a game between two players
    If one or both of the players are human, then it allows that player to make moves with a mouse
    """
    def __init__(self):
        SceneBase.__init__(self)
        # calculate constants used for drawing later
        # (these are all done in the fixed transform space, so we can safely use constants)
        self.CENTER_X = 1920*0.5
        self.QUARTER_X = int(1920*0.25)
        self.THREE_QUARTER_X = int(1920*0.75)
        self.CENTER_Y = 1080*0.5
        self.HEIGHT = 1080
        self.WIDTH = 1920

        self.TITLE_SIZE = 56
        self.LABEL_SIZE = 48
        self.PICKER_HEIGHT = 120
        self.PICKER_WIDTH = 800

        # setup labels and scene title
        font_color = Settings.theme['font']

        self.title = FontService.get_regular_font(self.TITLE_SIZE)
        self.title_surface = self.title.render("Setup New Game", False, font_color)
        self.title_size = self.title.size("Setup New Game")
        self.title_location = (self.CENTER_X - 0.5 * self.title_size[0], 72)

        self.p1_label = FontService.get_regular_font(self.LABEL_SIZE)
        self.p1_label_surface = self.p1_label.render("Player 1", False, font_color)
        self.p1_label_size = self.p1_label.size("Player 1")
        self.p1_label_location = (self.QUARTER_X - 0.5 * self.p1_label_size[0], 170)

        self.p2_label = FontService.get_regular_font(self.LABEL_SIZE)
        self.p2_label_surface = self.p2_label.render("Player 2", False, font_color)
        self.p2_label_size = self.p2_label.size("Player 2")
        self.p2_label_location = (self.THREE_QUARTER_X - 0.5 * self.p2_label_size[0], 170)

        self.p1_time_label = FontService.get_regular_font(self.LABEL_SIZE)
        self.p1_time_label_surface = self.p1_time_label.render("Move Timer", False, font_color)
        self.p1_time_label_size = self.p1_time_label.size("Move Timer")
        self.p1_time_label_location = (self.QUARTER_X - 0.5 * self.p1_time_label_size[0], 470)

        self.p2_time_label = FontService.get_regular_font(self.LABEL_SIZE)
        self.p2_time_label_surface = self.p2_time_label.render("Move Timer", False, font_color)
        self.p2_time_label_size = self.p2_time_label.size("Move Timer")
        self.p2_time_label_location = (self.THREE_QUARTER_X - 0.5 * self.p2_time_label_size[0], 470)

        # these are the selectable options for time limits
        human_time_limit_options = [
            {"title": "Unlimited", "data": -1}
        ]
        bot_time_limit_options = [
            {"title": "0:01", "data": 1},
            {"title": "0:02", "data": 2},
            {"title": "0:03", "data": 3},
            {"title": "0:04", "data": 4},
            {"title": "0:05", "data": 5},
            {"title": "0:10", "data": 10},
            {"title": "0:20", "data": 20},
            {"title": "0:30", "data": 30},
            {"title": "0:45", "data": 45},
            {"title": "1:00", "data": 60},
            {"title": "1:30", "data": 90},
            {"title": "2:00", "data": 120},
            {"title": "2:30", "data": 150},
            {"title": "5:00", "data": 300},
            {"title": "Seriously? More?", "data": 600}
        ]

        def p1_time_callback(value):
            self.player1_time_limit = value['data']

        def p2_time_callback(value):
            self.player2_time_limit = value['data']

        player1_time_picker = Picker(self.QUARTER_X - 0.5 * self.PICKER_WIDTH, 550, self.PICKER_WIDTH,
                                     self.PICKER_HEIGHT, human_time_limit_options, p1_time_callback,
                                     wrap_values=False, selected_index=len(human_time_limit_options)-1)
        player2_time_picker = Picker(self.THREE_QUARTER_X - 0.5 * self.PICKER_WIDTH, 550, self.PICKER_WIDTH,
                                     self.PICKER_HEIGHT, human_time_limit_options, p2_time_callback,
                                     wrap_values=False, selected_index=len(human_time_limit_options)-1)
        self.widgets.append(player1_time_picker)
        self.widgets.append(player2_time_picker)

        # these are the choosable options for player 1 and player 2
        player_options = [{
            "title": "Human Player",
            "description": "Moves controlled by a human player using the mouse.",
            "difficulty": 5,
            "data": Player
        }]
        bots = BotLoader.get_bots()
        player_options.extend(bots)

        def p1_picker_callback(value):
            self.player1_type = value['data']
            # if the player is no longer human, remove the "Unlimited" time option
            if self.player1_type != Player:
                player1_time_picker.set_values(bot_time_limit_options)
            else:
                player1_time_picker.set_values(human_time_limit_options)

        def p2_picker_callback(value):
            self.player2_type = value['data']
            # if the player is no longer human, remove the "Unlimited" time option
            if self.player2_type != Player:
                player2_time_picker.set_values(bot_time_limit_options)
            else:
                player2_time_picker.set_values(human_time_limit_options)

        player1_picker = Picker(self.QUARTER_X - 0.5*self.PICKER_WIDTH, 250, self.PICKER_WIDTH, self.PICKER_HEIGHT, player_options, p1_picker_callback)
        player2_picker = Picker(self.THREE_QUARTER_X - 0.5*self.PICKER_WIDTH, 250, self.PICKER_WIDTH, self.PICKER_HEIGHT, player_options, p2_picker_callback)
        self.widgets.append(player1_picker)
        self.widgets.append(player2_picker)

        # Data that will be set by page controls:
        self.player1_type = player_options[0]['data']
        self.player1_time_limit = human_time_limit_options[-1]['data']
        self.player2_type = player_options[0]['data']
        self.player2_time_limit = human_time_limit_options[-1]['data']

        # button to start the game
        def start_game():
            p1 = self.player1_type(Board.X, self.player1_time_limit)
            p2 = self.player2_type(Board.O, self.player2_time_limit)
            SceneManager.go_to_play_game(self, p1, p2)

        start_game_btn = Button(self.CENTER_X - self.PICKER_WIDTH*0.5, 750,
                                   self.PICKER_WIDTH, self.PICKER_HEIGHT, "Start Game", start_game)
        self.widgets.append(start_game_btn)

    def process_input(self, events, pressed_keys):
        for widget in self.widgets:
            widget.process_input(events, pressed_keys)

    def update(self):
        pass

    def render(self, screen):
        bg = ImageService.get_game_bg()
        screen.blit(bg, (0, 0))

        screen.blit(self.title_surface, self.title_location)
        screen.blit(self.p1_label_surface, self.p1_label_location)
        screen.blit(self.p2_label_surface, self.p2_label_location)
        screen.blit(self.p1_time_label_surface, self.p1_time_label_location)
        screen.blit(self.p2_time_label_surface, self.p2_time_label_location)

        for widget in self.widgets:
            widget.render(screen)
