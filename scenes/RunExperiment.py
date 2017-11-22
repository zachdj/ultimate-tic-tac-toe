import pygame, threading
from math import floor
from services import SettingsService as Settings, FontService, ImageService, SceneManager
from widgets import Button
from scenes.SceneBase import SceneBase
from scenes.DrawingUtils import *
from models.game import Board
from models.data import DatabaseConnection as DB


class RunExperiment(SceneBase):
    """ Scene that shows the progress of an experiment with some summary stats
    """

    def __init__(self, experiment):
        SceneBase.__init__(self)
        # data to keep track of the experiment's progress
        self.experiment = experiment
        self.total = experiment.iterations
        self.wins_for_x = 0
        self.ties = 0
        self.wins_for_o = 0
        self.played = 0

        # constants defining where stuff can be drawn
        self.MARGIN = 96
        self.TITLE_SIZE = 56
        self.LABEL_SIZE = 48
        self.INFO_BOX = pygame.Rect(self.MARGIN, self.MARGIN*1.5, 1920 - self.MARGIN*2, 1080*0.66 - 2*self.MARGIN)
        self.PROGRESS_BAR_WIDTH = 1920 - 2*self.MARGIN
        self.PROGRESS_BAR_HEIGHT = 100
        self.PROGRESS_BAR_X = self.MARGIN
        self.PROGRESS_BAR_Y = self.INFO_BOX.y + self.INFO_BOX.height + 0.5*self.PROGRESS_BAR_HEIGHT
        self.PROGRESS_BORDER = pygame.Rect(self.PROGRESS_BAR_X, self.PROGRESS_BAR_Y, self.PROGRESS_BAR_WIDTH, self.PROGRESS_BAR_HEIGHT)
        self.PROGRESS_BG = pygame.Rect(self.PROGRESS_BAR_X+4, self.PROGRESS_BAR_Y+4, self.PROGRESS_BAR_WIDTH-8, self.PROGRESS_BAR_HEIGHT-8)
        self.title_font = FontService.get_regular_font(self.TITLE_SIZE)
        self.label_font = FontService.get_regular_font(self.LABEL_SIZE)
        font_color = Settings.theme['font']

        self.heading_surface = self.title_font.render("%s   vs   %s" % (self.experiment.p1.name, self.experiment.p2.name), False, font_color)
        self.heading_size = self.title_font.size("%s   vs   %s" % (self.experiment.p1.name, self.experiment.p2.name))
        self.heading_location = (self.INFO_BOX.centerx - 0.5*self.heading_size[0], self.INFO_BOX.top - 1.5*self.heading_size[1])

        # "Done" button
        def back_to_mm():
            SceneManager.go_to_main_menu(self)

        self.done_btn = Button(1920*0.5 - 150, self.PROGRESS_BG.bottom + 24,
                                   300, 100, "Done", back_to_mm)

        # kick dis party off in a separate thread
        def experiment_callback(count, winner):
            self.played = count
            if winner == Board.X:
                self.wins_for_x += 1
            elif winner == Board.O:
                self.wins_for_o += 1
            else:
                self.ties += 1

        # unset SQLite objects from the main thread
        DB.close()

        def run_experiment():
            # Initialize SQLite objects in this thread
            DB.init()
            self.experiment.run(experiment_callback)
            DB.close()

        experiment_thread = threading.Thread(target=run_experiment)
        experiment_thread.start()

    def process_input(self, events, pressed_keys):
        for widget in self.widgets:
            widget.process_input(events, pressed_keys)

        self.done_btn.process_input(events, pressed_keys)

    def update(self):
        pass

    def render(self, screen):
        bg = ImageService.get_game_bg()
        screen.blit(bg, (0, 0))

        aa_border_rounded_rect(screen, self.INFO_BOX, Settings.theme['widget_background'], Settings.theme['widget_highlight'], radius=0.1)
        screen.blit(self.heading_surface, self.heading_location)

        # draw progress bar
        progress = self.played / self.experiment.iterations
        pygame.draw.rect(screen,Settings.theme['widget_highlight'], self.PROGRESS_BORDER)
        pygame.draw.rect(screen, Settings.theme['widget_background'], self.PROGRESS_BG)
        progress_bar = self.PROGRESS_BG.copy()
        progress_bar.width = floor(self.PROGRESS_BG.width*progress)
        pygame.draw.rect(screen, Settings.theme['primary'], progress_bar)

        # draw labels for num wins/losses
        num_wins_surface = self.label_font.render("Wins for X :   %s Games" % self.wins_for_x, False, Settings.theme['font'])
        num_wins_size = self.label_font.size("X has won :   %s Games" % self.wins_for_x)
        num_wins_location = (self.INFO_BOX.x + 48, self.INFO_BOX.y + self.INFO_BOX.height*0.25 - num_wins_size[1]*0.5)
        screen.blit(num_wins_surface, num_wins_location)

        num_ties_surface = self.label_font.render("Number of Ties :   %s Games" % self.ties, False, Settings.theme['font'])
        num_ties_size = self.label_font.size("Number of Ties :   %s Games" % self.ties)
        num_ties_location = (self.INFO_BOX.x + 48, self.INFO_BOX.y + self.INFO_BOX.height*0.50 - num_ties_size[1]*0.5)
        screen.blit(num_ties_surface, num_ties_location)

        num_losses_surface = self.label_font.render("Wins for O :   %s Games" % self.wins_for_o, False, Settings.theme['font'])
        num_losses_size = self.label_font.size("Wins for O :   %s Games" % self.wins_for_o)
        num_losses_location = (self.INFO_BOX.x + 48, self.INFO_BOX.y + self.INFO_BOX.height*0.75 - num_losses_size[1]*0.5)
        screen.blit(num_losses_surface, num_losses_location)

        # draw labels for win/tie/loss rates
        win_rate, loss_rate, tie_rate = 0, 0, 0
        if self.played > 0:
            win_rate = floor((self.wins_for_x / self.played)*100)
            loss_rate = floor((self.wins_for_o / self.played)*100)
            tie_rate = floor((self.ties / self.played)*100)
        num_wins_surface = self.label_font.render("X Win Percentage :   %s %%" % win_rate, False, Settings.theme['font'])
        num_wins_size = self.label_font.size("X Win Percentage: %s %%" % win_rate)
        num_wins_location = (self.INFO_BOX.centerx + 48, self.INFO_BOX.y + self.INFO_BOX.height*0.25 - num_wins_size[1]*0.5)
        screen.blit(num_wins_surface, num_wins_location)

        num_ties_surface = self.label_font.render("Tied Percentage :   %s %%" % tie_rate, False, Settings.theme['font'])
        num_ties_size = self.label_font.size("Tied Percentage: %s %%" % tie_rate)
        num_ties_location = (self.INFO_BOX.centerx + 48, self.INFO_BOX.y + self.INFO_BOX.height*0.50 - num_ties_size[1]*0.5)
        screen.blit(num_ties_surface, num_ties_location)

        num_losses_surface = self.label_font.render("X Loss Percentage :   %s %%" % loss_rate, False, Settings.theme['font'])
        num_losses_size = self.label_font.size("X Loss Percentage: %s %%" % loss_rate)
        num_losses_location = (self.INFO_BOX.centerx + 48, self.INFO_BOX.y + self.INFO_BOX.height*0.75 - num_losses_size[1]*0.5)
        screen.blit(num_losses_surface, num_losses_location)

        progress_text = "%s %%" % round(progress * 100)
        progress_text_surface = self.label_font.render(progress_text, False, Settings.theme['font'])
        progress_text_size = self.label_font.size(progress_text)
        progress_text_location = (progress_bar.centerx - 0.5*progress_text_size[0], progress_bar.centery - 0.5*progress_text_size[1])
        screen.blit(progress_text_surface, progress_text_location)

        for widget in self.widgets:
            widget.render(screen)

        self.done_btn.render(screen)