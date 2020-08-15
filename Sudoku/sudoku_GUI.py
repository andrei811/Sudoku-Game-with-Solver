import os
import pygame
import random
import time
import sudoku_text as sk

pygame.init()

fnt = pygame.font.SysFont("Bookman Old Style", 40)


class Board:
    fnt2 = pygame.font.SysFont("Bookman Old Style", 25)

    Xmark = pygame.transform.scale(
        pygame.image.load("Sudoku/Resources/X.png"), (30, 30))

    matrix = [
        [0, 0, 0, 0, 3, 0, 2, 0, 0],
        [7, 0, 5, 2, 0, 0, 0, 9, 0],
        [8, 3, 0, 4, 6, 9, 1, 5, 0],
        [2, 0, 0, 0, 9, 4, 0, 3, 0],
        [9, 8, 0, 0, 0, 3, 0, 0, 2],
        [6, 1, 3, 8, 0, 2, 0, 0, 9],
        [4, 0, 0, 1, 0, 0, 7, 0, 3],
        [3, 7, 8, 0, 2, 0, 4, 0, 0],
        [0, 6, 1, 0, 0, 0, 0, 0, 0]]

    R = []

    lines_color = (0, 0, 0)
    thick_big_line = 4
    thick_small_line = 1

    mouse_selected = [-1, -1]
    mistakes = 0

    st_time = 0
    pl_time = 0

    game_over = False
    solved_with_algorithm = False

    def __init__(self, cube_size, win_height, is_random_generated):
        self.width = win_height
        self.height = win_height
        self.cube_size = cube_size

        file = open("Sudoku\\sudokumatrix.txt")

        for i in range(9):
            for j in range(9):
                self.matrix[i][j] = int(file.read(2))

        self.board = [[Cube(i, j, self.matrix[i][j], self.cube_size, self.thick_small_line, self.thick_big_line, "black")
                       for j in range(9)] for i in range(9)]

    def set_pl_time(self):
        # updating time
        if self.mistakes == 3:
            return
        self.pl_time = round(time.time() - self.st_time)

    def is_full(self):
        # check if the matrix is completed
        for i in range(9):
            for j in range(9):
                if self.matrix[i][j] == 0:
                    return False
        return True

    def print_message(self, win):
        # printing final messages
        if self.mistakes == 3:
            pygame.time.delay(30)
            game_over = True
            txt = fnt.render("YOU LOST!", 1, (255, 255, 255))
            rectangle = pygame.Rect(
                self.board[4][2].pos[0]-1, self.board[3][2].pos[1] + 35, 236, 65)
            pygame.draw.rect(win, (230, 0, 0), rectangle)
            win.blit(txt, (self.board[3][2].pos[0] +
                           8, self.board[3][2].pos[1] + 43))
        elif self.is_full() and not self.solved_with_algorithm:
            txt = fnt.render("YOU WON!", 1, (255, 255, 255))
            rectangle = pygame.Rect(
                self.board[4][2].pos[0]-1, self.board[3][2].pos[1] + 35, 236, 65)
            pygame.draw.rect(win, (0, 204, 0), rectangle)
            win.blit(txt, (self.board[3][2].pos[0] +
                           10, self.board[3][2].pos[1] + 43))

    def mouse_click(self):
        # getting the position of mouse click
        xpos, ypos = pygame.mouse.get_pos()
        if xpos <= self.height and ypos <= self.width:
            self.mouse_selected = [ypos // 47, xpos // 47]

    def set_as_value(self):

        if self.mouse_selected[0] != -1:
            vr = self.board[self.mouse_selected[0]
                            ][self.mouse_selected[1]].set_temp_to_val(self.matrix)
            if vr != None:
                if not vr:
                    self.mistakes += 1

    def set_temp_val(self, Tvalue):
        if self.mouse_selected[0] != -1:
            self.board[self.mouse_selected[0]
                       ][self.mouse_selected[1]].update_temp_value(Tvalue)

    def clear_temp_value(self):
        if self.mouse_selected[0] != -1:
            self.board[self.mouse_selected[0]
                       ][self.mouse_selected[1]].clear_t()

    def draw(self, win, solved=False, with_algorithm=False):

        win.fill((255, 255, 255))

        # drawing vertical lines
        for i in range(1, 9):
            if i % 3 == 0 and i != 9:
                xpos = i * self.cube_size + 2 * \
                    (i // 3) * self.thick_small_line + \
                    self.thick_big_line * (i // 3 - 1)
                xpos += 2
                pygame.draw.line(win, self.lines_color, (xpos, 0),
                                 (xpos, self.height), self.thick_big_line)
            else:
                xpos = i * self.cube_size + (i - 1) * self.thick_small_line + (
                    i // 3) * (self.thick_big_line - self.thick_small_line)
                xpos += 1
                pygame.draw.line(win, self.lines_color, (xpos, 0),
                                 (xpos, self.height), self.thick_small_line)

        # drawing horizontal lines
        for j in range(1, 10):
            if j % 3 == 0:
                ypos = j * self.cube_size + 2 * \
                    (j // 3) * self.thick_small_line + \
                    self.thick_big_line * (j // 3 - 1)
                ypos += 2
                pygame.draw.line(win, self.lines_color, (0, ypos),
                                 (self.width, ypos), self.thick_big_line)
            else:
                ypos = j * self.cube_size + (j - 1) * self.thick_small_line + (
                    j // 3) * (self.thick_big_line - self.thick_small_line)
                ypos += 1
                pygame.draw.line(win, self.lines_color, (0, ypos),
                                 (self.width, ypos), self.thick_small_line)

        # drawing numbers on board
        for i in range(9):
            for j in range(9):
                self.board[i][j].draw(win)

        if self.mouse_selected[0] != -1 and self.board[self.mouse_selected[0]][self.mouse_selected[1]].value == 0:
            self.board[self.mouse_selected[0]
                       ][self.mouse_selected[1]].draw_cube(win, (0, 0, 0))

        self.print_message(win)

        for i in range(0, self.mistakes):
            if self.mistakes >= 1:
                win.blit(self.Xmark, (5, 432))
            if self.mistakes >= 2:
                win.blit(self.Xmark, (40, 432))
            if self.mistakes == 3:
                win.blit(self.Xmark, (75, 432))

        if not self.is_full() and not self.game_over:
            # updating time, just if the game is not over
            self.set_pl_time()

        t = self.format_t(self.pl_time)
        time_txt = self.fnt2.render("Time: " + t, 1,  (0, 0, 0))
        win.blit(time_txt, (280, 432))

        pygame.display.update()

    def format_t(self, seccs):
        # formatting time; from seconds -> min:sec
        sec = seccs % 60
        minutes = seccs // 60
        hours = minutes // 60
        minutes %= 60

        m = ""

        if hours > 0:
            m = str(hours) + ":" + str(minutes) + ":" + str(seccs)
        else:
            m = str(minutes) + ":" + str(seccs)

        return m

    def init_solve(self):
        # getting the position of all 0s in matrix
        for i in range(9):
            for j in range(9):
                if self.matrix[i][j] == 0:
                    self.R.append([i, j])

        self.lenght_R = len(self.R)

    def solve(self, pos, win, wait_time=100):
        # checking if the user wants to close the window
        checking_for_exit()

        self.solved_with_algorithm = True

        # backtracking solving
        if pos >= self.lenght_R:
            return True

        x = self.R[pos][0]
        y = self.R[pos][1]

        for i in range(1, 10):
            if sk.valid(x, y, i, self.matrix):

                self.matrix[x][y] = i
                self.board[x][y].update_value(i)
                self.draw(win)
                checking_for_exit()
                pygame.time.wait(wait_time)

                if self.solve(pos + 1, win, wait_time):
                    return True

                self.matrix[x][y] = 0
                self.board[x][y].update_value(0)
                self.draw(win)
                checking_for_exit()
                pygame.time.wait(wait_time)


class Cube:
    t_fnt = pygame.font.SysFont("Bookman Old Style", 20)

    temp_value = 0

    had_value = False
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)

    pos = []

    def __init__(self, row, col, value, size, thick_small_line, thick_big_line, color):
        self.thick_big_line = thick_big_line
        self.thick_small_line = thick_small_line
        self.row = row
        self.col = col
        self.value = value
        self.size = size
        self.color = color
        self.wasnull = None
        self.pos = self.calculate_the_pos()

        if value != 0:
            self.wasnull = False
        else:
            self.wasnull = True

    def update_temp_value(self, t_value):
        if self.value == 0:
            self.temp_value = t_value

    def update_value_without_color(self, value):
        self.value = value

    def update_value(self, value):
        self.value = value
        if value == 0:
            self.color = "red"
            self.had_value = True
        else:
            self.color = "green"

    def set_temp_to_val(self, matrix):
        if self.temp_value != 0:
            matrix[self.row][self.col] = self.temp_value

            ret = False
            ret = sk.is_solvable_and_valid(
                self.row, self.col, self.temp_value, matrix)
            if ret:
                matrix[self.row][self.col] = self.temp_value
                self.update_value(self.temp_value)
                self.temp_value = 0
            else:
                matrix[self.row][self.col] = 0

            return ret
        return None

    def clear_t(self):
        self.temp_value = 0

    def draw_cube(self, win, COLOR):
        pygame.draw.line(
            win, COLOR, (self.pos[0], self.pos[1]), (self.pos[0], self.pos[3]))

        pygame.draw.line(
            win, COLOR, (self.pos[0], self.pos[1]), (self.pos[2], self.pos[1]))

        pygame.draw.line(
            win, COLOR, (self.pos[0], self.pos[3]), (self.pos[2], self.pos[3]))

        pygame.draw.line(
            win, COLOR, (self.pos[2], self.pos[1]), (self.pos[2], self.pos[3]))

    def calculate_the_pos(self):
        position_x = self.col * self.size + self.col * self.thick_small_line
        position_x += (self.thick_big_line -
                       self.thick_small_line) * (self.col // 3)

        position_y = self.row * self.size + self.row * self.thick_small_line
        position_y += (self.thick_big_line -
                       self.thick_small_line) * (self.row // 3)

        pos_fin_x = (self.col+1) * self.size + self.col * self.thick_small_line
        pos_fin_x += (self.thick_big_line -
                      self.thick_small_line) * (self.col // 3) - 1

        pos_fin_y = (self.row+1) * self.size + self.row * self.thick_small_line
        pos_fin_y += (self.thick_big_line -
                      self.thick_small_line) * (self.row // 3) - 1

        if self.col != 0:
            position_x += 2
        if self.row != 0:
            position_y += 2

        return [position_x, position_y, pos_fin_x, pos_fin_y]

    def draw(self, win):
        if self.value != 0:
            txt = fnt.render(str(self.value), 1, (0, 0, 0))

            win.blit(txt, (self.pos[0] + 9, self.pos[1] - 2))

            if self.wasnull:
                self.draw_cube(win, self.GREEN)

        elif self.temp_value != 0:
            aux_txt = self.t_fnt.render(
                str(self.temp_value), 1, (100, 100, 100))

            win.blit(aux_txt, (self.pos[0], self.pos[1] - 2))

        elif self.had_value:
            self.draw_cube(win, self.RED)


def input_number(event):
    if event.key == pygame.K_1:
        return 1
    if event.key == pygame.K_2:
        return 2
    if event.key == pygame.K_3:
        return 3
    if event.key == pygame.K_4:
        return 4
    if event.key == pygame.K_5:
        return 5
    if event.key == pygame.K_6:
        return 6
    if event.key == pygame.K_7:
        return 7
    if event.key == pygame.K_8:
        return 8
    if event.key == pygame.K_9:
        return 9
    return None


def checking_for_exit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()


def main():
    cube_size = 45

    delay = 50  # ms

    is_random = True

    win_width = 9 * cube_size + 6 + 2 * 4
    win_height = win_width + 50

    os.environ['SDL_VIDEO_WINDOW_POS'] = "550,200"
    win = pygame.display.set_mode((win_width, win_height))

    pygame.display.set_caption('Sudoku Solver')

    board = Board(cube_size, win_width, is_random)

    solved = False
    with_algorithm = False

    board.st_time = time.time()

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if not board.game_over:

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not solved:
                        board.init_solve()
                        board.solve(0, win, delay)
                        solved = True
                        with_algorithm = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        board.set_as_value()

                    elif event.key == pygame.K_DELETE:
                        board.clear_temp_value()

                    else:
                        nr = input_number(event)

                        if nr != None:
                            board.set_temp_val(nr)

                if event.type == pygame.MOUSEBUTTONUP:
                    board.mouse_click()

        board.draw(win, solved, with_algorithm)


main()
