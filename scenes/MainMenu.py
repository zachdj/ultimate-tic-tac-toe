from .SceneBase import SceneBase
from .PlayGame import PlayGame
from .SetupGame import SetupGame
from models.game import Player, BogoBot, Board, MonteCarloBot
from services import ImageService
from widgets import Button


class MainMenu(SceneBase):
    def __init__(self, screen):
        SceneBase.__init__(self)
        # get screen dimensions to position buttons
        s_width = screen.get_width()
        s_height = screen.get_height()
        center_x = s_width*0.5
        center_y = s_height*0.5

        def go_to_game_setup():
            setup_scene = SetupGame()
            self.switch_to_scene(setup_scene)

        def go_to_singleplayer():
            p1 = Player(Board.X)
            p2 = MonteCarloBot(Board.O, 5)
            game_scene = PlayGame(p1, p2)
            self.switch_to_scene(game_scene)

        def go_to_multiplayer():
            p1 = Player(Board.X)
            p2 = Player(Board.O)
            game_scene = PlayGame(p1, p2)
            self.switch_to_scene(game_scene)

        single_player_btn = Button(center_x - s_width*0.2, center_y - s_height*0.4, s_width*0.4, s_height*0.1,
                                   "Start a Game", go_to_game_setup)

        two_player_btn = Button(center_x - s_width * 0.2, center_y - s_height * 0.2, s_width * 0.4, s_height * 0.1,
                                   "Two Player Game", go_to_multiplayer)

        experiment_btn = Button(center_x - s_width * 0.2, center_y, s_width * 0.4, s_height * 0.1,
                                "Run Experiment", lambda: print("Experiment time!"))

        settings_btn = Button(center_x - s_width * 0.2, center_y + s_height * 0.2, s_width * 0.4, s_height * 0.1,
                                "Settings", lambda: print("Change some settings!"))

        self.widgets.extend([single_player_btn, two_player_btn, experiment_btn, settings_btn])

    def process_input(self, events, pressed_keys):
        for widget in self.widgets:
            widget.process_input(events, pressed_keys)

    def update(self):
        pass

    def render(self, screen):
        bg = ImageService.get_main_menu_bg()
        screen.blit(bg, (0, 0))
        for widget in self.widgets:
            widget.render(screen)
