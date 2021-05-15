from tetriminos import new_random_mino_at


class Tetris:
    level = 2
    lines_cleared = 0
    state = "start"
    field = []
    x = 100
    y = 60
    current_mino = None

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.field = [[0 for i in range(width)] for y in range(height)]

    def new_figure(self):
        self.current_mino = new_random_mino_at(int(self.width/2-2), 0)

    def intersects(self):
        intersection = False
        mino = self.current_mino
        for i in range(4):
            for j in range(4):
                if i * 4 + j in mino.get_current_rotation():
                    if i + mino.y > self.height - 1 or \
                            j + mino.x > self.width - 1 or \
                            j + mino.x < 0 or \
                            self.field[i + mino.y][j + mino.x] > 0:
                        intersection = True
        return intersection

    # def exceeds_top(self):
    #     mino = self.current_mino

    def clear_lines(self):
        lines_to_remove = []
        for i, line in enumerate(self.field):
            if all(x > 0 for x in line):
                lines_to_remove.append(i)
        for line_index in lines_to_remove:
            self.field.pop(line_index)
            self.field.insert(0, [0 for y in range(self.width)])
        self.lines_cleared += len(lines_to_remove)

    def freeze_mino(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.current_mino.get_current_rotation():
                    self.field[i + self.current_mino.y][j +
                                                        self.current_mino.x] = self.current_mino.colorIndex
        self.clear_lines()
        self.new_figure()
        if self.intersects():
            self.state = "gameover"

    def move_sideways(self, dx):
        prev_x = self.current_mino.x
        self.current_mino.x += dx
        if self.intersects():
            self.current_mino.x = prev_x

    def move_down(self):
        self.current_mino.y += 1
        if self.intersects():
            self.current_mino.y -= 1
            self.freeze_mino()

    def rotate_mino(self, direction):
        self.current_mino.rotate(direction)
        if self.intersects():
            self.rotate_mino('right' if direction == 'left' else 'right')
