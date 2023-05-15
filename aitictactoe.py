import random, time, math 
import pygame as pyg

# COLOURS
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
red = (255, 0, 0)

# DISPLAY PARAMETERS
(board_width, board_height) = (500, 500)  # dimensions of board.
banner_height = 100  # height of info banner at bottom of screen.

# INITIALISING GAME WINDOW
pyg.init()
screen = pyg.display.set_mode((board_width, board_height + banner_height))
pyg.display.set_caption("Tic-Tac-Toe")

# DEFINING FONTS
font_title = pyg.font.SysFont('verdana', 30, bold=True)
font_instructions = pyg.font.SysFont('verdana', 20)

# RENDERING FONTS
text_title = font_title.render("Tic-Tac-Toe (vs. AI)", True, black)
text_instructions_1 = font_instructions.render("You are naughts, the AI is crosses.", True, black)
text_instructions_2 = font_instructions.render("Press r to reset.", True, black)
text_turn_1 = font_instructions.render("(Your Turn)", True, red)
text_turn_2 = font_instructions.render("(AI Turn)", True, black)
text_win_1 = font_instructions.render("You Win!", True, red)
text_win_2 = font_instructions.render("AI Wins :(", True, black)
text_win_3 = font_instructions.render("Stalemate", True, black)


# DRAWING INITIAL WINDOW
def make_window():
    '''
    This function draws all the elements of the initialised diplay window by layering them up.
    It is called everytime the game is reset.
    '''

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


# CLICK FUNCTIONS
def check_click(pos):
    '''
    This function return the zone number that has been clicked in based on the click coords.
    Zones are numbered 0-8 from left to right, top to bottom.
    '''

    col = math.floor(int(pos[0] / (board_width/3)))
    row = math.floor(int(pos[1] / (board_height/3))) * 3
    zone = col + row

    return zone


def zone_into_coords(zone):
    '''
    This returns the central coord for each zone based on its number identifier.
    Returns the coord as two values.
    '''

    base_width = board_width / 6
    base_height = board_height / 6

    x_coord_mult = (zone % 3)
    x_coord = base_width + (x_coord_mult * 2 * base_width)

    y_coord_mult = int(math.ceil((zone + 1) / 3) - 1)
    y_coord = base_height + (y_coord_mult * 2 * base_height)

    return x_coord, y_coord


def draw_shape(player, zone):
    '''
    This function draws the icon for the current player into the zone clicked on.
    '''

    offset = min(board_width / 12, board_height / 12)  # this is the offset value for placing the corners of the cross.
    coords = zone_into_coords(zone)

    if player == 1:
        # this is the human player.
        pyg.draw.circle(screen, black, coords, min(board_width, board_height) / 12, 5)
    elif player == 2:
        # this is the AI player.
        pyg.draw.line(screen, black, (coords[0] - offset, coords[1] - offset), (coords[0] + offset, coords[1] + offset), 5)
        pyg.draw.line(screen, black, (coords[0] - offset, coords[1] + offset), (coords[0] + offset, coords[1] - offset), 5)

    pyg.display.update()


def check_win(board):
    '''
    This functions checks the board for a winning state. The board input contains a list of values for each zone:
    0 - empty.
    1 - player 1 (naught).
    2 - player 2 (cross).

    It is called after every move.
    '''

    win = False  # defaults the win indication to False.
    player = 0  # this will be updated with the winning player.
    win_zones = 0, 0  # this will be updated with the non-adjacent winning zones.

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

    return win, player, win_zones


def draw_win(zones):
    '''
    This function draws across the winning line, as indicated by the input zones.
    '''

    pyg.draw.line(screen, red, zone_into_coords(zones[0]), zone_into_coords(zones[1]), 5)


# AI
def ai_turn(board_state):
    '''
    Processes a decision by the AI. Each zone is cycled through a scored. 
    Unavailable zones are discarded. Prioritises winning if it can. If it can't win or block a win, chooses randomly.
    '''

    scores = [0, 0, 0, 0, 0, 0, 0, 0, 0]  # initialising scores and zone.
    current_zone = 0

    for zone_score in scores:
        # cycles through each zone.
        board_state_edit = board_state  # copies the board for editing.
        
        if board_state_edit[current_zone] != 0:
            zone_score = -9999  # discards this zone.

        else:
            board_state_edit[current_zone] = 1
            checking = check_win(board_state_edit)  # checks if the human player can win here on the next move.
            if checking[0] == True:
                zone_score = 500

            board_state_edit[current_zone] = 2
            checking = check_win(board_state_edit)  # checks if the AI can win here now.
            if checking[0] == True:
                zone_score = 1000
            
            board_state_edit[current_zone] = 0

        scores[current_zone] = zone_score  # places zone_score into the scores list.
        current_zone += 1

    max_score_index = scores.index(max(scores))  # finds zone of greatest score and assigns this to choice,
    choice = max_score_index
    
    valid_choice = False
    while valid_choice == False:

        if scores[choice] == 0:  # if the AI can't win or block a win, it chooses randomly.
            choice = random.randint(0, 8)
            if scores[choice] != -9999:  # checks if random choice is already taken.
                valid_choice = True

        else:
            valid_choice = True  # defaults to this if the AI can win or block a win.

    return choice


# RUNNING THE GAME
def main():
    '''
    This function contains the game running sequences. The human player begins.
    '''

    make_window()  # initialise window.
    board_state = [0, 0, 0, 0, 0, 0, 0, 0, 0]  # initialise board state.

    running = True
    player_turn = 1
    stale = 0  # counts the number of turns. When 9 have been taken, declares a draw.


    while running:

        win_check, win_player, win_zones = check_win(board_state)  # begins each turn by checking for a winning state.

        if win_check == True:
            draw_win(win_zones)  # draws the winning line.
            pyg.draw.rect(screen, white, pyg.Rect(board_width - 150, board_height + 70, board_width, board_height + banner_height))

            if win_player == 1:  # Human wins text.
                screen.blit(text_win_1, [board_width - 150, board_height + 70])
            elif win_player == 2:  # AI wins text.
                screen.blit(text_win_2, [board_width - 150, board_height + 70])

            pyg.display.update()


        if stale == 9:  # checks the stale counter for a draw.
            pyg.draw.rect(screen, white, pyg.Rect(board_width - 150, board_height + 70, board_width, board_height + banner_height))
            screen.blit(text_win_3, [board_width - 150, board_height + 70])
            pyg.display.update()


        if player_turn == 2 and stale != 9 and win_check == False:  # AI turn.
            pyg.draw.rect(screen, white, pyg.Rect(board_width - 150, board_height + 70, board_width, board_height + banner_height))
            screen.blit(text_turn_2, [board_width - 150, board_height + 70])
            pyg.display.update()

            time.sleep(random.randint(1, 20) / 10)  # adds a random delay to make it seem like it's thinking.
        
            ai_choice = ai_turn(board_state)  # makes a choice based on the board state.
            draw_shape(player_turn, ai_choice)  # draws choice onto board.
            board_state[ai_choice] = 2  # updates board state.
            stale += 1  # updates stale counter.

            player_turn = 1  # ends turn.
            pyg.draw.rect(screen, white, pyg.Rect(board_width - 150, board_height + 70, board_width, board_height + banner_height))
            screen.blit(text_turn_1, [board_width - 150, board_height + 70])
            pyg.display.update()


        for event in pyg.event.get():  # manages interactions with the game window.
            if event.type == pyg.QUIT:  # closing the window.
                running = False


            if event.type == pyg.KEYDOWN:  # keyboard is pressed.
                if event.key == pyg.K_r:  # 'r' key is pressed.
                    running = False
                    main()  # resets and reruns game.


            if event.type == pyg.MOUSEBUTTONDOWN and player_turn == 1 and stale != 9 and win_check == False:  # mouse is clicked during players turn.
                clicked_coord = pyg.mouse.get_pos()  # gets the coord clicked.
                clicked_zone = check_click(clicked_coord)  # gets the zone clicked.

                if board_state[clicked_zone] == 0:  # checks if zone is empty.
                    draw_shape(player_turn, clicked_zone)  # draws choice onto board.
                    board_state[clicked_zone] = 1  # updates board state.
                    stale += 1  # updates stales counter.
                    player_turn = 2  # ends player turn.


main()
