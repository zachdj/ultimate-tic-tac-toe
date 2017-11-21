import numpy
from .SceneBase import SceneBase
from widgets import Picker, Button
from models.game import Board
from models.game.bots import BotLoader
from services import ImageService, FontService, SceneManager, SettingsService as Settings


class SetupExperiment(SceneBase):
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

        self.TITLE_SIZE = 48
        self.LABEL_SIZE = 36
        self.PICKER_HEIGHT = 100
        self.PICKER_WIDTH = 650

        # setup labels and scene title
        font_color = Settings.theme['font']

        self.title = FontService.get_regular_font(self.TITLE_SIZE)
        self.title_surface = self.title.render("Setup New Experiment", False, font_color)
        self.title_size = self.title.size("Setup New Experiment")
        self.title_location = (self.CENTER_X - 0.5 * self.title_size[0], 50)

        self.p1_label = FontService.get_regular_font(self.LABEL_SIZE)
        self.p1_label_surface = self.p1_label.render("Player 1", False, font_color)
        self.p1_label_size = self.p1_label.size("Player 1")
        self.p1_label_location = (self.QUARTER_X - 0.5 * self.p1_label_size[0], 120)

        self.p2_label = FontService.get_regular_font(self.LABEL_SIZE)
        self.p2_label_surface = self.p2_label.render("Player 2", False, font_color)
        self.p2_label_size = self.p2_label.size("Player 2")
        self.p2_label_location = (self.THREE_QUARTER_X - 0.5 * self.p2_label_size[0], 120)

        self.p1_time_label = FontService.get_regular_font(self.LABEL_SIZE)
        self.p1_time_label_surface = self.p1_time_label.render("Move Timer", False, font_color)
        self.p1_time_label_size = self.p1_time_label.size("Move Timer")
        self.p1_time_label_location = (self.QUARTER_X - 0.5 * self.p1_time_label_size[0], 350)

        self.p2_time_label = FontService.get_regular_font(self.LABEL_SIZE)
        self.p2_time_label_surface = self.p2_time_label.render("Move Timer", False, font_color)
        self.p2_time_label_size = self.p2_time_label.size("Move Timer")
        self.p2_time_label_location = (self.THREE_QUARTER_X - 0.5 * self.p2_time_label_size[0], 350)

        self.num_games_label = FontService.get_regular_font(self.LABEL_SIZE)
        self.num_games_label_surface = self.num_games_label.render("Number of Trials", False, font_color)
        self.num_games_label_size = self.num_games_label.size("Number of Trials")
        self.num_games_label_location = (self.QUARTER_X - 0.5 * self.num_games_label_size[0], 580)

        self.record_result_label = FontService.get_regular_font(self.LABEL_SIZE)
        self.record_result_label_surface = self.record_result_label.render("Record Result", False, font_color)
        self.record_result_label_size = self.record_result_label.size("Record Result")
        self.record_result_label_location = (self.THREE_QUARTER_X - 0.5 * self.record_result_label_size[0], 580)

        #### SETUP WIDGETS #####

        # pickers for which two bots will play
        bots = BotLoader.get_bots()

        def p1_picker_callback(value):
            self.player1_type = value['data']

        def p2_picker_callback(value):
            self.player2_type = value['data']

        player1_picker = Picker(self.QUARTER_X - 0.5*self.PICKER_WIDTH, 200, self.PICKER_WIDTH, self.PICKER_HEIGHT, bots, p1_picker_callback)
        player2_picker = Picker(self.THREE_QUARTER_X - 0.5*self.PICKER_WIDTH, 200, self.PICKER_WIDTH, self.PICKER_HEIGHT, bots, p2_picker_callback)
        self.widgets.append(player1_picker)
        self.widgets.append(player2_picker)

        # pickers for how long each player has to make a move
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
            {"title": "5:00", "data": 300}
        ]

        def p1_time_callback(value):
            self.player1_time_limit = value['data']

        def p2_time_callback(value):
            self.player2_time_limit = value['data']

        player1_time_picker = Picker(self.QUARTER_X - 0.5 * self.PICKER_WIDTH, 420, self.PICKER_WIDTH,
                                     self.PICKER_HEIGHT, bot_time_limit_options, p1_time_callback,
                                     wrap_values=False, selected_index=0)
        player2_time_picker = Picker(self.THREE_QUARTER_X - 0.5 * self.PICKER_WIDTH, 420, self.PICKER_WIDTH,
                                     self.PICKER_HEIGHT, bot_time_limit_options, p2_time_callback,
                                     wrap_values=False, selected_index=0)
        self.widgets.append(player1_time_picker)
        self.widgets.append(player2_time_picker)

        # picker for number of games to play
        num_games_options = []
        for i in numpy.arange(1, 10, 1):
            num_games_options.append({'title': str(i), 'data': i})
        for i in numpy.arange(10, 110, 10):
            num_games_options.append({'title': str(i), 'data': i})
        for i in numpy.arange(125, 525, 25):
            num_games_options.append({'title': str(i), 'data': i})
        for i in numpy.arange(600, 1600, 100):
            num_games_options.append({'title': str(i), 'data': i})

        def num_games_callback(value):
            self.num_games = value['data']

        num_games_picker = Picker(self.QUARTER_X - 0.5 * self.PICKER_WIDTH, 660, self.PICKER_WIDTH,
                                     self.PICKER_HEIGHT, num_games_options, num_games_callback,
                                     wrap_values=True, selected_index=0)
        self.widgets.append(num_games_picker)

        # binary picker whether to record the result of the experiment or not
        record_result_options = [
            {'title': 'Yes', 'data': True},
            {'title': 'No', 'data': False}
        ]

        def record_result_callback(value):
            self.record_result = value['data']

        record_result_picker = Picker(self.THREE_QUARTER_X - 0.5 * self.PICKER_WIDTH, 660, self.PICKER_WIDTH,
                                     self.PICKER_HEIGHT, record_result_options, record_result_callback,
                                     wrap_values=True, selected_index=0)
        self.widgets.append(record_result_picker)

        # Data that will be set by form controls:
        self.player1_type = bots[0]['data']
        self.player1_time_limit = bot_time_limit_options[0]['data']
        self.player2_type = bots[0]['data']
        self.player2_time_limit = bot_time_limit_options[0]['data']
        self.num_games = num_games_options[0]['data']
        self.record_result = record_result_options[0]['data']

        # button to start the experiment
        def start_experiment():
            p1 = self.player1_type(Board.X, self.player1_time_limit)
            p2 = self.player2_type(Board.O, self.player2_time_limit)
            # SceneManager.go_to_experiment(self, p1, p2)

        start_game_btn = Button(self.CENTER_X - self.PICKER_WIDTH*0.5, 850,
                                   self.PICKER_WIDTH, self.PICKER_HEIGHT, "Start Experiment", start_experiment)
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
        screen.blit(self.num_games_label_surface, self.num_games_label_location)
        screen.blit(self.record_result_label_surface, self.record_result_label_location)

        for widget in self.widgets:
            widget.render(screen)
