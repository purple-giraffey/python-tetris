import pygame

from tetris import Tetris
from colors import BLACK, BLUE, GRAY, WHITE, TETRIMINO_COLORS, MAGENTA, RED, GREEN, YELLOW


def run_tetris():
    pygame.init()
    size = (400, 500)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Tetris")
    done = False
    clock = pygame.time.Clock()
    fps = 50
    game = Tetris(20, 10)
    counter = 0
    zoom = 20
    score = 0

    pressing_down = False
    is_paused = False

    while not done:
        score = game.lines_cleared * 10

        if game.current_mino is None:
            game.new_figure()
        counter += 1
        if counter > 100000:
            counter = 0

        if counter % (fps // game.level // 2) == 0 or pressing_down:
            if game.state == "start" and not is_paused:
                game.move_down()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN and game.state != 'gameover':
                if event.key == pygame.K_d or event.key == pygame.K_UP:
                    game.rotate_mino('right')
                if event.key == pygame.K_a:
                    game.rotate_mino('left')
                if event.key == pygame.K_DOWN:
                    pressing_down = True
                if event.key == pygame.K_LEFT:
                    game.move_sideways(-1)
                if event.key == pygame.K_RIGHT:
                    game.move_sideways(1)
                if event.key == pygame.K_SPACE:
                    game.move_down()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_LSHIFT:
                    game.new_figure()
                if event.key == pygame.K_p:
                    is_paused = not is_paused

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    pressing_down = False

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_LSHIFT] and pressed_keys[pygame.K_r]:
            game = Tetris(20, 10)

        screen.fill(BLACK)

        for i in range(game.height):
            for j in range(game.width):
                pygame.draw.rect(screen, GRAY, [
                    game.x + zoom * j, game.y + zoom * i, zoom, zoom], 1)
                if game.field[i][j] > 0:
                    pygame.draw.rect(screen, TETRIMINO_COLORS[game.field[i][j]],
                                     [game.x + zoom * j + 1, game.y + zoom * i + 1, zoom - 2, zoom - 2])

        if game.current_mino is not None:
            for i in range(4):
                for j in range(4):
                    p = i * 4 + j
                    if p in game.current_mino.get_current_rotation():
                        pygame.draw.rect(screen, TETRIMINO_COLORS[game.current_mino.colorIndex],
                                         [game.x + zoom * (j + game.current_mino.x) + 1,
                                         game.y + zoom *
                                         (i + game.current_mino.y) + 1,
                                         zoom - 2, zoom - 2])

        font = pygame.font.SysFont('Calibri', 24, True)
        font1 = pygame.font.SysFont('Calibri', 48, True)
        text_score = font.render(
            "SCORE", True, WHITE)
        text_score_number = font.render(
            str(score), True, GREEN)
        text_lines_cleared = font.render(
            'LINES', True, WHITE)
        text_lines_cleared_number = font.render(
            str(game.lines_cleared), True, GRAY)
        text_game_over = font1.render("GAME OVER", True, BLACK)
        text_game_over1 = font.render(
            "Shift + R to try again", True, WHITE)
        text_game_over2 = font.render(
            "Shift + R to try again", True, BLUE)
        text_game_paused = font.render('PAUSED', True, WHITE)

        screen.blit(text_score, [size[0]-90, 15])
        screen.blit(text_score_number, [size[0]-90, 40])

        screen.blit(text_lines_cleared, [size[0]-90, 70])
        screen.blit(text_lines_cleared_number, [size[0]-90, 95])

        if game.state == "gameover":
            overlay = pygame.Surface(size)
            overlay.set_alpha(128)
            overlay.fill(GRAY)
            screen.blit(overlay, (0, 0))
            pygame.draw.rect(screen, RED, [
                             0, size[0]/2 + 10, size[0], 100])
            screen.blit(text_game_over, [50, 220])
            screen.blit(text_game_over1, [80, 270])

            rect = pygame.Rect(0, 270, size[0], 48)
            mpos = pygame.mouse.get_pos()
            if rect.collidepoint(mpos):
                screen.blit(text_game_over2, [80, 270])
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.MOUSEBUTTONDOWN:
                    game = Tetris(20, 10)

        if is_paused:
            overlay = pygame.Surface(size)
            overlay.set_alpha(128)
            overlay.fill(WHITE)
            screen.blit(overlay, (0, 0))
            pygame.draw.rect(screen, GRAY, [
                             0, size[0]/2 + 20, size[0], 50])
            screen.blit(text_game_paused, [150, 235])

        pygame.display.flip()
        clock.tick(fps)

    pygame.display.quit()
    pygame.quit()


run_tetris()
