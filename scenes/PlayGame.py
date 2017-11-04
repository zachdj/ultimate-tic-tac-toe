from .SceneBase import SceneBase
from models.game import Game, Board
from services import ImageService
import pygame


class PlayGame(SceneBase):
    def __init__(self, screen, player1, player2):
        SceneBase.__init__(self)
        # calculate constants used for drawing later
        # (these are all done in the fixed transform space, so we can safely use constants)
        self.MARGIN = 96
        self.CELL_SIZE = 83
        self.CELL_SPACING = 10
        self.LOCAL_BOARD_SPACING = 25
        self.BOARD_AREA_X = 1920 - self.MARGIN - 9*(self.CELL_SIZE + self.CELL_SPACING) - 2*self.LOCAL_BOARD_SPACING
        self.BOARD_AREA_Y = self.MARGIN

        self.cell_sprites = ImageService.get_board_cell_sprites()
        for key in self.cell_sprites.keys():
            self.cell_sprites[key] = pygame.transform.scale(self.cell_sprites[key], (self.CELL_SIZE, self.CELL_SIZE))

        self.game = Game(player1, player2)


    def process_input(self, events, pressed_keys):
        for widget in self.widgets:
            widget.process_input(events, pressed_keys)

    def update(self):
        pass

    def render(self, screen):
        bg = ImageService.get_game_bg()
        screen.blit(bg, (0, 0))

        for i in list(range(0, 9)):
            metarow = i // 3
            row = i % 3
            for j in list(range(0, 9)):
                metacol = j // 3
                col = j % 3
                cell = self.game.board.check_small_cell(metarow, metacol, row, col)

                # compute the location of the cell in the grid and shift it into the board area
                location_x = (metacol * 3 + col)*(self.CELL_SIZE + self.CELL_SPACING) \
                    + self.LOCAL_BOARD_SPACING*metacol \
                    + self.BOARD_AREA_X

                location_y = (metarow * 3 + row) * (self.CELL_SIZE + self.CELL_SPACING) \
                     + self.LOCAL_BOARD_SPACING * metarow \
                     + self.BOARD_AREA_Y

                screen.blit(self.cell_sprites['blank'], (location_x, location_y))

                # screen.blit(self.cell_sprites['p2_marker'], (location_x, location_y))

        for widget in self.widgets:
            widget.render(screen)
