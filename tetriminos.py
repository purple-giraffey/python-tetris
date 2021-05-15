import random
from colors import *

'''
Stores all tetrimino types by name, as well as their rotations (representations in a 4*4 matrix) and their color.
'''
TETRIMINOS = {
    'I': {'rotations': [[1, 5, 9, 13], [4, 5, 6, 7], [2, 6, 10, 14], [8, 9, 10, 11]], 'color': LIGHT_BLUE},
    'L': {'rotations': [[1, 5, 9, 10], [4, 5, 6, 8], [0, 1, 5, 9], [2, 4, 5, 6]], 'color': RED},
    'O': {'rotations': [[1, 2, 5, 6]], 'color': YELLOW},
    'S': {'rotations': [[1, 2, 4, 5], [1, 5, 6, 10], [5, 6, 8, 9], [0, 4, 5, 9]], 'color': MAGENTA},
    'T': {'rotations': [[1, 4, 5, 6], [1, 5, 6, 9], [4, 5, 6, 9], [1, 4, 5, 9]], 'color': PURPLE},
    'J': {'rotations': [[0, 4, 5, 6], [1, 2, 5, 9], [4, 5, 6, 10], [1, 5, 8, 9]], 'color': BLUE},
    'Z': {'rotations': [[0, 1, 5, 6], [2, 5, 6, 9], [4, 5, 9, 10], [1, 4, 5, 8]], 'color': GREEN}
}


class Tetrimino:
    '''
    Describes an individual tetrimino figure, it's absolute position (x, y) and current rotation.
    '''

    x = None
    y = None

    def __init__(self, name, x, y, current_rotation_index=0):
        self.name = name
        self.x = x
        self.y = y
        description = TETRIMINOS[name]
        self.rotations = description['rotations']
        self.colorIndex = TETRIMINO_COLORS.index(description['color'])
        self.current_rotation_index = current_rotation_index

    def get_current_rotation(self):
        return self.rotations[self.current_rotation_index]

    def rotate(self, direction):
        next_rotation_index = self.current_rotation_index + (
            1 if direction == 'right' else - 1)
        if next_rotation_index < 0:
            next_rotation_index = len(
                self.rotations) - abs(next_rotation_index)
        if next_rotation_index > len(self.rotations) - 1:
            next_rotation_index = len(self.rotations) - next_rotation_index
        self.current_rotation_index = next_rotation_index

    def get_default_rotation(self):
        return self.rotations[0]


def print_mino(mino, rotation_index=0):
    mino_layout = TETRIMINOS[mino]['rotations'][rotation_index]
    layout = []
    current_row = []
    for x in range(0, 16):
        if x in mino_layout:
            current_row.append('*')
        else:
            current_row.append('-')
        if (x+1) % 4 == 0:
            layout.append(current_row)
            current_row = []
    for r in layout:
        print(r)


def new_random_mino_at(x, y):
    random_mino_name = random.choice(list(TETRIMINOS.keys()))
    return Tetrimino(random_mino_name, x, y)
