import pygame, sys
from player_manager import PlayerManager
from button import Button

def search_player(screen, bg, get_font, clock, framerate):
    input_box = pygame.Rect(300, 300, 200, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    search_name = ''

    player_manager = PlayerManager()
    player_manager.load_players("scoreboard.csv")

    while True:
        screen.blit(bg, (0, 0))
        search_text = get_font(40).render("SEARCH PLAYER", True, "#b68f40")
        search_rect = search_text.get_rect(center=(screen.get_width() // 2, 500))
        screen.blit(search_text, search_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        player = player_manager.find_player(search_name)
                        if player:
                            result_text = f"Found: {player.name}, Score: {player.score}"
                        else:
                            result_text = f"Player '{search_name}' not found!"
                        display_message(screen, result_text, get_font)
                        search_name = ''
                    elif event.key == pygame.K_BACKSPACE:
                        search_name = search_name[:-1]
                    else:
                        search_name += event.unicode

        pygame.draw.rect(screen, color, input_box, 2)
        txt_surface = get_font(30).render(search_name, True, (255, 255, 255))
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        input_box.w = max(200, txt_surface.get_width() + 10)

        pygame.display.flip()
        clock.tick(framerate)

def superHardScoreBoard():
    fileName = "superhardscoreboard.csv"
    try:
        with open(fileName, "r") as file:
            reader = csv.reader(file)
            data = list(reader)
    except FileNotFoundError:
        show_message("Super Hard Scoreboard file not found! ", RED)
        return

    if not data:  # Kiểm tra danh sách trống
        show_message("No players found in the Super Hard Scoreboard!", RED)
        return

    data.sort(key=lambda row: int(row[1]), reverse=True)  # Sắp xếp theo điểm giảm dần

    current_page = 0
    items_per_page = 5

    while True:
        SCREEN.blit(BG, (0, 0))
        SCOREBOARD_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(TEXT_TOP).render("SUPER HARD SCORE BOARD", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.1))

        BACK_BUTTON = Button(image=None, pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.9),
                             text_input="HOME", font=get_font(TEXT_SIZE), base_color="#d7fcd4", hovering_color="Red")
        NEXT_BUTTON = Button(image=None, pos=(SCREEN_WIDTH * 0.75, SCREEN_HEIGHT * 0.9),
                             text_input=">", font=get_font(TEXT_SIZE), base_color="#d7fcd4", hovering_color="Red")
        PREV_BUTTON = Button(image=None, pos=(SCREEN_WIDTH * 0.25, SCREEN_HEIGHT * 0.9),
                             text_input="<", font=get_font(TEXT_SIZE), base_color="#d7fcd4", hovering_color="Red")
        SEARCH_BUTTON = Button(image=None, pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.8),
                               text_input="SEARCH", font=get_font(TEXT_SIZE), base_color="#d7fcd4", hovering_color="Red")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [BACK_BUTTON, NEXT_BUTTON, PREV_BUTTON, SEARCH_BUTTON]:
            button.changeColor(SCOREBOARD_MOUSE_POS)
            button.update(SCREEN)

        # Hiển thị dữ liệu bảng xếp hạng
        x_name = 200
        x_score = 650
        y_start = 120
        line_height = 50

        for i in range(current_page * items_per_page, min((current_page + 1) * items_per_page, len(data))):
            rank = i + 1
            name = data[i][0]
            score = data[i][1]
            y = y_start + (i - current_page * items_per_page) * line_height

            rank_text = get_font(TEXT_SIZE).render(f"{rank}. ", True, WHITE)
            name_text = get_font(TEXT_SIZE).render(name, True, WHITE)
            score_text = get_font(TEXT_SIZE).render(score, True, WHITE)

            SCREEN.blit(rank_text, (x_name - rank_text.get_width() - 10, y))
            SCREEN.blit(name_text, (x_name, y))
            SCREEN.blit(score_text, (x_score, y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_BUTTON.checkForInput(SCOREBOARD_MOUSE_POS):
                    return  # Quay lại bảng xếp hạng
                if NEXT_BUTTON.checkForInput(SCOREBOARD_MOUSE_POS) and (current_page + 1) * items_per_page < len(data):
                    current_page += 1
                if PREV_BUTTON.checkForInput(SCOREBOARD_MOUSE_POS) and current_page > 0:
                    current_page -= 1
                if SEARCH_BUTTON.checkForInput(SCOREBOARD_MOUSE_POS):
                    search_player_in_superhard_scoreboard(fileName, SCREEN, BG, get_font, clock, framerate)

        pygame.display.update()
        clock.tick(framerate)

def search_player_in_scoreboard(fileName, screen, bg, get_font, clock, framerate):
    player_manager = PlayerManager()
    player_manager.load_players(fileName)

    input_box = pygame.Rect(300, 300, 200, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    search_name = ''

    while True:
        screen.blit(bg, (0, 0))
        search_text = get_font(40).render("SEARCH PLAYER", True, "#b68f40")
        search_rect = search_text.get_rect(center=(screen.get_width() // 2, 100))
        screen.blit(search_text, search_rect)

        BACK_BUTTON = Button(image=None, pos=(screen.get_width() // 2, 500),
                             text_input="BACK", font=get_font(30), base_color="#d7fcd4", hovering_color="Red")

        BACK_BUTTON.changeColor(pygame.mouse.get_pos())
        BACK_BUTTON.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    return  # Quay lại bảng xếp hạng
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        player = player_manager.find_player(search_name)
                        if player:
                            display_message(screen, f"Found: {player.name} - Score: {player.score}", get_font)
                        else:
                            display_message(screen, f"Player '{search_name}' not found!", get_font)
                        search_name = ''  # Reset sau khi tìm kiếm
                    elif event.key == pygame.K_BACKSPACE:
                        search_name = search_name[:-1]
                    else:
                        search_name += event.unicode

        pygame.draw.rect(screen, color, input_box, 2)
        txt_surface = get_font(30).render(search_name, True, (255, 255, 255))
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        input_box.w = max(200, txt_surface.get_width() + 10)

        pygame.display.flip()
        clock.tick(framerate)


def display_message(screen, message, get_font):
    msg_surface = get_font(30).render(message, True, (255, 0, 0))
    msg_rect = msg_surface.get_rect(center=(screen.get_width() // 2, 400))
    screen.blit(msg_surface, msg_rect)
    pygame.display.update()
    pygame.time.wait(2000)