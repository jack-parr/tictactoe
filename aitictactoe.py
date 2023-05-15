import random, time, pygame as pyg, math

# Parameters.
(board_width, board_height) = (500, 500)  # these values may be changed.
banner_height = 100  # do not change this value.
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)


# Setting the game window.
pyg.init()
screen = pyg.display.set_mode((board_width, board_height + banner_height))
pyg.display.set_caption("Tic-Tac-Toe")
font_title = pyg.font.SysFont('verdana', 30, bold=True)
font_instructions = pyg.font.SysFont('verdana', 20)
text_title = font_title.render("Tic-Tac-Toe (vs. AI)", True, black)
text_instructions_1 = font_instructions.render("You are naughts, the AI is crosses.", True, black)
text_instructions_2 = font_instructions.render("Press r to reset.", True, black)
text_turn_1 = font_instructions.render("(Your Turn)", True, red)
text_turn_2 = font_instructions.render("(AI Turn)", True, black)
text_win_1 = font_instructions.render("You Win!", True, red)
text_win_2 = font_instructions.render("AI Wins :(", True, black)
text_win_3 = font_instructions.render("Stalemate", True, black)


def make_window():
    screen.fill(white)
    pyg.draw.line(screen, blue, (board_width / 3, 0), (board_width / 3, board_height), 2)
    pyg.draw.line(screen, blue, (board_width / 1.5, 0), (board_width / 1.5, board_height), 2)
    pyg.draw.line(screen, blue, (0, board_height / 3), (board_width, board_height / 3), 2)
    pyg.draw.line(screen, blue, (0, board_height / 1.5), (board_width, board_height / 1.5), 2)
    pyg.draw.rect(screen, black, pyg.Rect(0, 0, board_width, board_height), 6)
    pyg.draw.rect(screen, white, pyg.Rect(0, board_height, board_width, board_height+banner_height))
    screen.blit(text_title, [10, board_height])
    screen.blit(text_instructions_1, [10, board_height + 40])
    screen.blit(text_instructions_2, [10, board_height + 70])
    screen.blit(text_turn_1, [board_width - 150, board_height + 70])

    pyg.display.update()


# Setting up Tic Tac Toe.
def check_win(board):
    win = False
    player = 0
    win_zones = 0, 0
    if board[0] == board[3] == board[6] != 0:
        win = True
        player = board[0]
        win_zones = 0, 6
    elif board[1] == board[4] == board[7] != 0:
        win = True
        player = board[1]
        win_zones = 1, 7
    elif board[2] == board[5] == board[8] != 0:
        win = True
        player = board[2]
        win_zones = 2, 8
    elif board[0] == board[1] == board[2] != 0:
        win = True
        player = board[0]
        win_zones = 0, 2
    elif board[3] == board[4] == board[5] != 0:
        win = True
        player = board[3]
        win_zones = 3, 5
    elif board[6] == board[7] == board[8] != 0:
        win = True
        player = board[6]
        win_zones = 6, 8
    elif board[0] == board[4] == board[8] != 0:
        win = True
        player = board[0]
        win_zones = 0, 8
    elif board[2] == board[4] == board[6] != 0:
        win = True
        player = board[2]
        win_zones = 2, 6

    return win, player, win_zones[0], win_zones[1]


def check_click(pos):
    x_pos = math.floor(int(pos[0] / (board_width/3)))
    y_pos = math.floor(int(pos[1] / (board_height/3))) * 3
    zone = x_pos + y_pos

    return zone


def zone_into_coords(zone):
    base_width = board_width / 6
    base_height = board_height / 6

    x_coord_mult = (zone % 3)
    x_coord = base_width + (x_coord_mult * 2 * base_width)

    y_coord_mult = int(math.ceil((zone + 1) / 3) - 1)
    y_coord = base_height + (y_coord_mult * 2 * base_height)

    return x_coord, y_coord


def draw_shape(player, zone):
    adjuster = min(board_width / 12, board_height / 12)
    coords = zone_into_coords(zone)
    if player == 1:
        pyg.draw.circle(screen, black, coords, min(board_width, board_height) / 12, 5)
    elif player == 2:
        pyg.draw.line(screen, black, (coords[0] - adjuster, coords[1] - adjuster), (coords[0] + adjuster, coords[1] + adjuster), 5)
        pyg.draw.line(screen, black, (coords[0] - adjuster, coords[1] + adjuster), (coords[0] + adjuster, coords[1] - adjuster), 5)

    pyg.display.update()


def draw_win(zone1, zone2):
    pyg.draw.line(screen, red, zone_into_coords(zone1), zone_into_coords(zone2), 5)


# AI.
def ai_turn(board_state):
    scores = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    current_zone = 0
    for zone_score in scores:
        board_state_edit = board_state
        if board_state_edit[current_zone] != 0:
            zone_score = -9999
        else:
            board_state_edit[current_zone] = 1
            checking = check_win(board_state_edit)
            if checking[0]:
                zone_score = 500
            board_state_edit[current_zone] = 2
            checking = check_win(board_state_edit)
            if checking[0]:
                zone_score = 1000
            board_state_edit[current_zone] = 0

        scores[current_zone] = zone_score
        current_zone += 1

    max_score_index = scores.index(max(scores))
    choice = max_score_index
    i = True
    while i:
        if scores[max_score_index] == 0:
            choice = random.randint(0, 8)
            if scores[choice] != -9999:
                i = False
        else:
            i = False

    return choice


# Running the game.
def main():
    make_window()
    board_state = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    running = True
    win = False
    player_turn = 1
    stale = 0
    while running:
        win_check = check_win(board_state)
        win = win_check[0]
        if win:
            draw_win(win_check[2], win_check[3])
            pyg.draw.rect(screen, white, pyg.Rect(board_width - 150, board_height + 70, board_width, board_height + banner_height))
            if win_check[1] == 1:
                screen.blit(text_win_1, [board_width - 150, board_height + 70])
            elif win_check[1] == 2:
                screen.blit(text_win_2, [board_width - 150, board_height + 70])
            pyg.display.update()

        if stale == 9:
            pyg.draw.rect(screen, white, pyg.Rect(board_width - 150, board_height + 70, board_width, board_height + banner_height))
            screen.blit(text_win_3, [board_width - 150, board_height + 70])
            pyg.display.update()

        if not win and player_turn == 2 and stale != 9:
            pyg.draw.rect(screen, white, pyg.Rect(board_width - 150, board_height + 70, board_width, board_height + banner_height))
            screen.blit(text_turn_2, [board_width - 150, board_height + 70])
            pyg.display.update()
            time.sleep(random.randint(1, 20) / 10)
            ai_choice = ai_turn(board_state)
            draw_shape(player_turn, ai_choice)
            board_state[ai_choice] = 2
            stale += 1
            player_turn = 1
            pyg.draw.rect(screen, white, pyg.Rect(board_width - 150, board_height + 70, board_width, board_height + banner_height))
            screen.blit(text_turn_1, [board_width - 150, board_height + 70])
            pyg.display.update()

        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                running = False

            if event.type == pyg.KEYDOWN:
                if event.key == pyg.K_r:
                    running = False
                    main()

            if event.type == pyg.MOUSEBUTTONDOWN and not win and player_turn == 1 and stale != 9:
                pos = pyg.mouse.get_pos()
                clicked_zone = check_click(pos)
                if board_state[clicked_zone] == 0:
                    draw_shape(player_turn, clicked_zone)
                    board_state[clicked_zone] = 1
                    stale += 1
                    player_turn = 2


main()
