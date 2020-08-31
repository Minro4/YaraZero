from math import ceil


class Piece:

    def __init__(self):
        self.player = None
        self.other_player = None
        self.king = False
        self.captured = False
        self.position = None
        self.board = None
        self.capture_move_enemies = {}
        self.reset_for_new_board()

    def __eq__(self, other):
        return self.player == other.player and self.position == other.position and \
               self.king == other.king and self.captured == other.captured

    def __hash__(self):
        return hash((self.position, self.player))

    def reset_for_new_board(self):
        self.possible_capture_moves = None
        self.possible_positional_moves = None

    def is_movable(self):
        return (self.get_possible_capture_moves() or self.get_possible_positional_moves()) and not self.captured

    def capture(self):
        self.captured = True
        self.position = None

    def move(self, new_position):
        self.position = new_position
        self.king = self.king or self.is_on_enemy_home_row()

    def get_possible_capture_moves(self):
        if self.possible_capture_moves == None:
            self.possible_capture_moves = self.build_possible_capture_moves()

        return self.possible_capture_moves

    def build_possible_capture_moves(self):
        adjacent_enemy_positions = list(
            filter((lambda position: position in self.board.searcher.get_positions_by_player(self.other_player)),
                   self.get_adjacent_positions()))
        capture_move_positions = []

        for enemy_position in adjacent_enemy_positions:
            enemy_piece = self.board.searcher.get_piece_by_position(enemy_position)
            position_behind_enemy = self.get_position_behind_enemy(enemy_piece)

            if (position_behind_enemy is not None) and self.board.position_is_open(position_behind_enemy):
                capture_move_positions.append(position_behind_enemy)
                self.capture_move_enemies[position_behind_enemy] = enemy_piece

        return self.create_moves_from_new_positions(capture_move_positions)

    def nbr_possible_get_captured(self):
        count = 0
        adjacent_enemy_positions = list(
            filter((lambda position: position in self.board.searcher.get_positions_by_player(self.other_player)),
                   self.get_adjacent_positions()))

        for enemy_position in adjacent_enemy_positions:
            enemy_piece = self.board.searcher.get_piece_by_position(enemy_position)
            position_behind_self = self.get_position_behind_self(enemy_piece)

            if (position_behind_self is not None) and self.board.position_is_open(position_behind_self):
                count += 1
        return count

    def get_position_behind_enemy(self, enemy_piece):
        current_row = self.get_row()
        current_column = self.get_column()
        enemy_column = enemy_piece.get_column()
        enemy_row = enemy_piece.get_row()
        column_adjustment = -1 if current_row % 2 == 0 else 1
        column_behind_enemy = current_column + column_adjustment if current_column == enemy_column else enemy_column
        row_behind_enemy = enemy_row + (enemy_row - current_row)

        return self.board.position_layout.get(row_behind_enemy, {}).get(column_behind_enemy)

    def get_position_behind_self(self, enemy_piece):
        current_row = self.get_row()
        current_column = self.get_column()
        enemy_column = enemy_piece.get_column()
        enemy_row = enemy_piece.get_row()
        column_adjustment = 1 if current_row % 2 == 0 else -1
        column_behind_self = current_column + column_adjustment if current_column == enemy_column else current_column
        row_behind_self = current_row + (current_row - enemy_row)

        return self.board.position_layout.get(row_behind_self, {}).get(column_behind_self)

    def get_possible_positional_moves(self):
        if self.possible_positional_moves == None:
            self.possible_positional_moves = self.build_possible_positional_moves()

        return self.possible_positional_moves

    def build_possible_positional_moves(self):
        new_positions = list(
            filter((lambda position: self.board.position_is_open(position)), self.get_adjacent_positions()))

        return self.create_moves_from_new_positions(new_positions)

    def create_moves_from_new_positions(self, new_positions):
        return [[self.position, new_position] for new_position in new_positions]

    def get_adjacent_positions(self):
        return self.get_directional_adjacent_positions(forward=True) + (
            self.get_directional_adjacent_positions(forward=False) if self.king else [])

    def get_column(self):
        return (self.position - 1) % self.board.width

    def get_row(self):
        return Piece.get_row_from_position(self.board, self.position)

    def is_on_enemy_home_row(self):
        return self.get_row() == Piece.get_row_from_position(self.board,
                                                             (
                                                                 1 if self.other_player == 1 else self.board.position_count))

    @staticmethod
    def get_row_from_position(board, position):
        return ceil(position / board.width) - 1

    @staticmethod
    def get_column_from_position(board, position):
        return ((position - 1) % board.width) * 2 + (2 if Piece.get_row_from_position(board, position) % 2 == 0 else 1)

    @staticmethod
    def position_to_str(board, position):
        return "[" + str(Piece.get_row_from_position(board, position) + 1) + ", " + str(
            Piece.get_column_from_position(board, position)) + "]"

    def get_directional_adjacent_positions(self, forward):
        positions = []
        current_row = self.get_row()
        next_row = current_row + ((1 if self.player == 1 else -1) * (1 if forward else -1))

        if not next_row in self.board.position_layout:
            return []

        next_column_indexes = self.get_next_column_indexes(current_row, self.get_column())

        return [self.board.position_layout[next_row][column_index] for column_index in next_column_indexes]

    def get_next_column_indexes(self, current_row, current_column):
        column_indexes = [current_column, current_column + 1] if current_row % 2 == 0 else [current_column - 1,
                                                                                            current_column]

        return filter((lambda column_index: column_index >= 0 and column_index < self.board.width), column_indexes)

    def __str__(self):
        if self.captured:
            return "."
        elif self.player == 1:
            return "W" if self.king else "w"
        else:
            return "B" if self.king else "b"

    def __setattr__(self, name, value):
        super(Piece, self).__setattr__(name, value)

        if name == 'player':
            self.other_player = 1 if value == 2 else 2
