import pygame, numpy, threading, time
from .SceneBase import SceneBase
from models.game import Game, Board, Move
from services import ImageService


class PlayGame(SceneBase):
    """
    This scene shows a graphical representation of a game between two players
    If one or both of the players are human, then it allows that player to make moves with a mouse
    """
    def __init__(self, player1, player2):
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
        # game object needs to be locked when the board is being rendered or when Bot players are ready to make a move
        self.game_lock = threading.Lock()
        self.bot_is_thinking = False

        self.ghost_move = None  # this Move object is used to show human players where their mouse is hovering

        # compute cell bounding boxes - Each element is a 4-tuple (left, top, right, bottom)
        self.cell_locations = numpy.empty((3, 3, 3, 3), object)
        for i in list(range(0, 9)):
            metarow = i // 3
            row = i % 3
            for j in list(range(0, 9)):
                metacol = j // 3
                col = j % 3
                # compute the location of the cell in the grid and shift it into the board area
                location_x = (metacol * 3 + col)*(self.CELL_SIZE + self.CELL_SPACING) \
                    + self.LOCAL_BOARD_SPACING*metacol \
                    + self.BOARD_AREA_X

                location_y = (metarow * 3 + row) * (self.CELL_SIZE + self.CELL_SPACING) \
                     + self.LOCAL_BOARD_SPACING * metarow \
                     + self.BOARD_AREA_Y

                self.cell_locations[metarow][metacol][row][col] = (location_x, location_y, location_x + self.CELL_SIZE, location_y + self.CELL_SIZE)

    def process_input(self, events, pressed_keys):
        for widget in self.widgets:
            widget.process_input(events, pressed_keys)

        # if the current player is a human, then respond to mouse events
        if self.game.active_player.player_type == 'human':
            for event in events:
                if event.type == pygame.MOUSEMOTION:
                    # highlight the move that's about to be selected if the mouse moves over a cell
                    self.game_lock.acquire()  # acquire a lock while reading the board to get valid moves
                    valid_moves = self.game.get_valid_moves()
                    self.game_lock.release()
                    location = event.pos
                    ghost_move_found = False  # used to clear ghost marker if ghost move is not found
                    for move in valid_moves:
                        cell_location = self.cell_locations[move.metarow][move.metacol][move.row][move.col]
                        # check if mouse motion is within bounding box of cell
                        if cell_location[0] <= location[0] <= cell_location[2] and cell_location[1] <= location[1] <= cell_location[3]:
                            self.ghost_move = move
                            ghost_move_found = True
                    if not ghost_move_found:
                        self.ghost_move = None

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.ghost_move:
                        self.game.make_move(self.ghost_move)

    def update(self):
        if self.game.is_game_over():
            self.switch_to_scene(None)
            print("Game over!  \nCongratulations Player %s" % self.game.get_winner())

        self.game_lock.acquire()
        bots_turn = self.game.active_player.is_bot()
        self.game_lock.release()
        if bots_turn and not self.bot_is_thinking:
            self.bot_is_thinking = True
            print("Making bot move")
            def make_bot_move():
                move = self.game.active_player.compute_next_move(self.game.board, self.game.get_valid_moves())
                self.game_lock.acquire()
                self.game.make_move(move)
                self.game_lock.release()
                self.bot_is_thinking = False
            bot_thread = threading.Thread(target=make_bot_move)
            bot_thread.start()

    def render(self, screen):
        bg = ImageService.get_game_bg()
        screen.blit(bg, (0, 0))

        # render the board
        self.game_lock.acquire()  # need to read values from the board while rendering
        valid_moves = self.game.get_valid_moves()
        current_player = self.game.active_player
        current_player_symbol = self.game.active_player.number
        for i in list(range(0, 9)):
            metarow = i // 3
            row = i % 3
            for j in list(range(0, 9)):
                metacol = j // 3
                col = j % 3
                board_winner = self.game.board.check_cell(metarow, metacol)
                cell_owner = self.game.board.check_small_cell(metarow, metacol, row, col)
                move_object = Move(current_player_symbol, metarow, metacol, row, col)

                # compute the location of the cell in the grid and shift it into the board area
                location = self.cell_locations[metarow][metacol][row][col]
                location_x, location_y = location[0], location[1]

                # render the correct background for the cell:
                if board_winner == Board.X :
                    screen.blit(self.cell_sprites['p1_won'], (location_x, location_y))
                elif board_winner == Board.O:
                    screen.blit(self.cell_sprites['p2_won'], (location_x, location_y))
                elif move_object in valid_moves:
                    if current_player.number == Board.X:
                        screen.blit(self.cell_sprites['p1_highlight'], (location_x, location_y))
                    if current_player.number == Board.O:
                        screen.blit(self.cell_sprites['p2_highlight'], (location_x, location_y))
                else:
                    screen.blit(self.cell_sprites['blank'], (location_x, location_y))

                # render the cell's owner:
                if cell_owner == Board.X:
                    screen.blit(self.cell_sprites['p1_marker'], (location_x, location_y))
                elif cell_owner == Board.O:
                    screen.blit(self.cell_sprites['p2_marker'], (location_x, location_y))

                # render a ghost move if there is one:
                if self.ghost_move is not None:
                    move_location = self.cell_locations[self.ghost_move.metarow][self.ghost_move.metacol][self.ghost_move.row][self.ghost_move.col]
                    if self.ghost_move.player == Board.X:
                        screen.blit(self.cell_sprites['p1_marker'], (move_location[0], move_location[1]))
                    else:
                        screen.blit(self.cell_sprites['p2_marker'], (move_location[0], move_location[1]))

        self.game_lock.release()  # rendering is done

        for widget in self.widgets:
            widget.render(screen)
