import pygame, sys
from pygame.locals import *
import random
import time
import csv
from button import Button
from PhaoHoa import Firework
from login import login_screen
from search import search_player_in_scoreboard
from player_manager import PlayerManager, Player

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

pygame.display.set_caption("Snake Game")

# Tải âm thanh
apple_sound = pygame.mixer.Sound("eat_sound.mp3")
game_over_sound = pygame.mixer.Sound("game_over.mp3")
button_click_sound = pygame.mixer.Sound("soundclick.mp3")  # Tải âm thanh nhấn nút

# Tải ảnh nền
BG_LOGIN = pygame.image.load("images/b1.jpg")  # Đường dẫn đến ảnh nền đăng nhập
BG_GAME = pygame.image.load("images/b1.jpg")
BG = pygame.image.load("images/b2.jpg")  # Tải ảnh b2
BG_MENU = pygame.image.load("images/b2.jpg")  # Đường dẫn đến ảnh nền menu


# Thay đổi kích thước ảnh để phù hợp với màn hình
BG_LOGIN = pygame.transform.scale(BG_LOGIN, (SCREEN_WIDTH, SCREEN_HEIGHT))
BG_GAME = pygame.transform.scale(BG_GAME, (SCREEN_WIDTH, SCREEN_HEIGHT))
BG_MENU = pygame.transform.scale(BG_MENU, (SCREEN_WIDTH, SCREEN_HEIGHT))
BG = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Phóng to ảnh b2


SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

beep_sound = pygame.mixer.Sound("soundclick.mp3")

clock = pygame.time.Clock()

framerate = 60
TEXT_SIZE = 30
TEXT_TOP = 40

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GOLD = (255, 215, 0)

SNAKE_BLOCK_SIZE = 20
SNAKE_SPEED = 10  # Normal speed
SNAKE_SPEED_HARD = 15  # Hard speed

OBSTACLE_COUNT = 10  # Number of obstacles in hard mode

def get_font(size):
    return pygame.font.Font("font/font.ttf", size)

def show_message(message, color=RED):
    font = get_font(25)
    text = font.render(message, True, color)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
    SCREEN.blit(text, text_rect)
    pygame.display.update()
    time.sleep(2)

def generate_apple(snake_body, obstacles):
    while True:
        apple_x = random.randrange(0, SCREEN_WIDTH // SNAKE_BLOCK_SIZE) * SNAKE_BLOCK_SIZE
        apple_y = random.randrange(0, SCREEN_HEIGHT // SNAKE_BLOCK_SIZE) * SNAKE_BLOCK_SIZE
        apple = (apple_x, apple_y)

        if apple not in snake_body and apple not in obstacles:
            is_golden = random.random() < 0.2  # 20% chance of golden apple
            return apple, is_golden

def generate_obstacles():
    obstacles = []
    for _ in range(OBSTACLE_COUNT):
        while True:
            obstacle_x = random.randrange(0, SCREEN_WIDTH // SNAKE_BLOCK_SIZE) * SNAKE_BLOCK_SIZE
            obstacle_y = random.randrange(0, SCREEN_HEIGHT // SNAKE_BLOCK_SIZE) * SNAKE_BLOCK_SIZE
            obstacle = (obstacle_x, obstacle_y)
            if obstacle not in obstacles:
                obstacles.append(obstacle)
                break
    return obstacles

def draw_snake(snake_body):
    # Tạo màu sắc ngẫu nhiên cho mỗi đoạn rắn
    for index, (x, y) in enumerate(snake_body):
        random_color = (
            random.randint(50, 255),  # Giá trị đỏ
            random.randint(50, 255),  # Giá trị xanh lá
            random.randint(50, 255)   # Giá trị xanh dương
        )
        pygame.draw.rect(SCREEN, random_color, [x, y, SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE])
        pygame.draw.rect(SCREEN, (0, 0, 0), [x, y, SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE], 1)  # Viền đen



def draw_apple(apple, is_golden):
    color = GOLD if is_golden else RED
    pygame.draw.rect(SCREEN, color, [apple[0], apple[1], SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE])


def draw_obstacles(obstacles):
    for x, y in obstacles:
        pygame.draw.rect(SCREEN, WHITE, [x, y, SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE])

def display_choices():
    font = get_font(30)
    play_again_text = font.render("Play Again", True, WHITE)
    back_to_menu_text = font.render("Back to Menu", True, WHITE)

    # Vẽ chữ lên màn hình
    SCREEN.blit(play_again_text, (SCREEN_WIDTH // 2 - play_again_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
    SCREEN.blit(back_to_menu_text, (SCREEN_WIDTH // 2 - back_to_menu_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

def game_loop(difficulty, scoreboard_file="scoreboardnormal.csv"):
    game_over = False
    game_close = False

    x1 = SCREEN_WIDTH / 2
    y1 = SCREEN_HEIGHT / 2
    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    apple, is_golden = generate_apple([], [])
    obstacles = generate_obstacles() if difficulty in ["hard", "super_hard"] else []
    snake_speed = SNAKE_SPEED_HARD if difficulty in ["hard", "super_hard"] else SNAKE_SPEED
    score = 0
    start_time = time.time()
    last_obstacle_update = time.time()

    fireworks = []  # Danh sách chứa các pháo hoa

    player_manager = PlayerManager()
    player_manager.load_players(scoreboard_file)  # Load trước danh sách người chơi

    while not game_over:

        flag = True
        while game_close:
            # Vẽ lại màn hình liên tục
            SCREEN.blit(BG, (0, 0))

            # Hiển thị thông báo thua cuộc
            font = get_font(40)
            game_over_text = font.render("GAME OVER", True, RED)
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
            SCREEN.blit(game_over_text, game_over_rect)

            # Tạo các nút
            play_again_button = Button(
                image=None,
                pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
                text_input="Play Again",
                font=get_font(30),
                base_color=WHITE,
                hovering_color=GREEN
            )
            
            menu_button = Button(
                image=None,
                pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100),
                text_input="Main Menu",
                font=get_font(30),
                base_color=WHITE,
                hovering_color=GREEN
            )

            # Lấy vị trí chuột
            MOUSE_POS = pygame.mouse.get_pos()

            # Cập nhật màu sắc nút khi di chuột
            play_again_button.changeColor(MOUSE_POS)
            menu_button.changeColor(MOUSE_POS)

            # Vẽ các nút
            play_again_button.update(SCREEN)
            menu_button.update(SCREEN)

            

            if game_close:
                if score >=  0 and flag:  # Chỉ lưu nếu điểm số hợp lệ
                    player = Player(USERNAME, None, None, None, score)
                    # player = Player("Thang", None, None, None, 12)
                    existing_player = player_manager.find_player(USERNAME)

                    if existing_player:
                        # Cập nhật nếu điểm mới cao hơn
                        if score > existing_player.score:
                            player_manager.update_player_score(USERNAME, score)
                    else:
                        # Thêm người chơi mới nếu chưa tồn tại
                        player_manager.add_player(player)

                    # Lưu vào file CSV
                    flag = False
                    player_manager.save_players(scoreboard_file)

            # Xử lý sự kiện
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_again_button.checkForInput(MOUSE_POS):
                        # Chơi lại với cùng độ khó
                        return game_loop(difficulty)
                    
                    if menu_button.checkForInput(MOUSE_POS):
                        # Quay về menu chính
                        main_menu()

            # Cập nhật màn hình
            pygame.display.update()
            clock.tick(60)

        # Lưu điểm vào file khi kết thúc trò chơi
        # Sau khi trò chơi kết thúc, lưu điểm của người chơi
        # main.py - game_loop
        

        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -SNAKE_BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = SNAKE_BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -SNAKE_BLOCK_SIZE
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = SNAKE_BLOCK_SIZE
                    x1_change = 0

        # Cập nhật vị trí chướng ngại vật mỗi 2 giây nếu ở chế độ siêu khó
        if difficulty == "super_hard":
            current_time = time.time()
            if current_time - last_obstacle_update >= 2:
                obstacles = generate_obstacles()
                last_obstacle_update = current_time

        # Check if the snake hit itself
        snake_Head = [x1, y1]
        if snake_Head in snake_List[:-1]:
            game_over_sound.play()
            game_close = True
        x1 += x1_change
        y1 += y1_change

        # Check for collisions with walls and obstacles
        if x1 >= SCREEN_WIDTH or x1 < 0 or y1 >= SCREEN_HEIGHT or y1 < 0:
            game_close = True
        if difficulty in ["hard", "super_hard"]:
            if any(x1 == obs_x and y1 == obs_y for obs_x, obs_y in obstacles):
                game_close = True

        # Clear the screen and draw background
        SCREEN.blit(BG, (0, 0))

        # Add the new head to the snake
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # Draw the snake
        draw_snake(snake_List)
        draw_apple(apple, is_golden)
        if difficulty in ["hard", "super_hard"]:
            draw_obstacles(obstacles)

        # Display score and time
        elapsed_time = int(time.time() - start_time)
        font = get_font(20)
        score_text = font.render(f"Score: {score}", True, WHITE)
        time_text = font.render(f"Time: {elapsed_time}", True, WHITE)
        SCREEN.blit(score_text, (10, 10))
        SCREEN.blit(time_text , (SCREEN_WIDTH - time_text.get_width() - 10, 10))

        pygame.display.update()

        # Check for apple collision
        if x1 == apple[0] and y1 == apple[1]:
            apple_sound.play()
            apple, is_golden = generate_apple(snake_List, obstacles)
            Length_of_snake += 1
            score += 1

        clock.tick(snake_speed)

    pygame.quit()
    sys.exit()

def game_over_fireworks(fireworks):
    for firework in fireworks:
        firework.update()
        firework.draw(SCREEN)

    # Thêm một số pháo hoa mới vào danh sách
    for _ in range(2):  # Số pháo hoa sẽ được thêm mỗi lần thua cuộc
        fireworks.append(Firework(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)))

def draw_firework(x, y):
    # Example code to draw a firework
    pygame.draw.circle(SCREEN, (255, 0, 0), (x, y), 5)  # Red firework
    # Add more effects as needed


def scoreBoardMenu():
    while True:
        SCREEN.blit(BG, (0, 0))
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(TEXT_TOP).render("SCORE BOARD", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.1))

        NORMAL_BUTTON = Button(image=None, pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.4),
                               text_input="NORMAL", font=get_font(TEXT_SIZE), base_color="#d7fcd4", hovering_color="Red")
        ADVANCED_BUTTON = Button(image=None, pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.5),
                                 text_input="HARD", font=get_font(TEXT_SIZE), base_color="#d7fcd4", hovering_color="Red")
        SUPER_HARD_BUTTON = Button(image=None, pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.6),
                                 text_input="SUPER HARD", font=get_font(TEXT_SIZE), base_color="#d7fcd4", hovering_color="Red")
        BACK_BUTTON = Button(image=None, pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.8),
                             text_input="BACK", font=get_font(TEXT_SIZE), base_color="#d7fcd4", hovering_color="Red")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [NORMAL_BUTTON, ADVANCED_BUTTON, SUPER_HARD_BUTTON, BACK_BUTTON]:
            button.changeColor(PLAY_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if NORMAL_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    button_click_sound.play()
                    scoreBoard("scoreboardnormal.csv")  # Dùng file NORMAL
                if ADVANCED_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    button_click_sound.play()
                    scoreBoard("scoreboardadvanced.csv")  # Dùng file ADVANCED
                if SUPER_HARD_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    button_click_sound.play()
                    scoreBoard("superhardscoreboard.csv")  # Dùng file SUPER HARD
                if BACK_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    button_click_sound.play()
                    main_menu()

        pygame.display.update()
        clock.tick(framerate)




def scoreBoard(fileName):
    try:
        with open(fileName, "r") as file:
            reader = csv.reader(file)
            # Chỉ lấy các hàng hợp lệ
            data = [row for row in reader if len(row) >= 2 and row[1].isdigit()]
    except FileNotFoundError:
        show_message("Scoreboard file not found!", RED)
        return

    if not data:  # Kiểm tra nếu file rỗng hoặc không có dữ liệu hợp lệ
        show_message("Scoreboard is currently empty!", RED)
        return

    try:
        # Sắp xếp theo điểm giảm dần
        data.sort(key=lambda row: int(row[1]), reverse=True)
    except ValueError:
        show_message("Invalid score format in scoreboard!", RED)
        return

    data.sort(key=lambda row: int(row[1]), reverse=True)  # Sắp xếp dữ liệu theo điểm số giảm dần

    current_page = 0
    items_per_page = 5

    while True:
        SCREEN.blit(BG, (0, 0))
        SCOREBOARD_MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = get_font(TEXT_TOP).render("SCORE BOARD", True, "#b68f40")
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

            rank_text = get_font(TEXT_SIZE).render(f"{rank}.", True, WHITE)
            name_text = get_font(TEXT_SIZE).render(name, True, WHITE)
            score_text = get_font(TEXT_SIZE).render(score, True, WHITE)

            SCREEN.blit(rank_text, (x_name - rank_text.get_width()-10, y))
            SCREEN.blit(name_text, (x_name, y))
            SCREEN.blit(score_text, (x_score, y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_BUTTON.checkForInput(SCOREBOARD_MOUSE_POS):
                    scoreBoardMenu()
                if NEXT_BUTTON.checkForInput(SCOREBOARD_MOUSE_POS) and (current_page + 1) * items_per_page < len(data):
                    current_page += 1
                if PREV_BUTTON.checkForInput(SCOREBOARD_MOUSE_POS) and current_page > 0:
                    current_page -= 1
                if SEARCH_BUTTON.checkForInput(SCOREBOARD_MOUSE_POS):
                    search_player_in_scoreboard(fileName)

        pygame.display.update()
        clock.tick(framerate)  

def scoreBoard(fileName):
    try:
        with open(fileName, "r") as file:
            reader = csv.reader(file)
            data = list(reader)
    except FileNotFoundError:
        show_message("Scoreboard file not found!", RED)
        return

    if not data:  # Kiểm tra danh sách trống
        show_message("Scoreboard is currently empty!", RED)
        return

    data.sort(key=lambda row: int(row[1]), reverse=True)  # Sắp xếp theo điểm giảm dần

    current_page = 0
    items_per_page = 5

    while True:
        SCREEN.blit(BG, (0, 0))
        SCOREBOARD_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(TEXT_TOP).render("SCORE BOARD", True, "#b68f40")
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
        y_start = 150
        line_height = 70

        for i in range(current_page * items_per_page, min((current_page + 1) * items_per_page, len(data))):
            rank = i + 1
            name = data[i][0]
            score = data[i][1]
            y = y_start + (i - current_page * items_per_page) * line_height

            rank_text = get_font(TEXT_SIZE).render(f"{rank}.", True, WHITE)
            name_text = get_font(TEXT_SIZE).render(name, True, WHITE)
            score_text = get_font(TEXT_SIZE).render(score, True, WHITE)

            SCREEN.blit(rank_text, (x_name - rank_text.get_width()-10, y))
            SCREEN.blit(name_text, (x_name, y))
            SCREEN.blit(score_text, (x_score, y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_BUTTON.checkForInput(SCOREBOARD_MOUSE_POS):
                    scoreBoardMenu()
                if NEXT_BUTTON.checkForInput(SCOREBOARD_MOUSE_POS) and (current_page + 1) * items_per_page < len(data):
                    current_page += 1
                if PREV_BUTTON.checkForInput(SCOREBOARD_MOUSE_POS) and current_page > 0:
                    current_page -= 1
                if SEARCH_BUTTON.checkForInput(SCOREBOARD_MOUSE_POS):
                    search_player_in_scoreboard(fileName, SCREEN, BG, get_font, clock, framerate)  # Gọi hàm tìm kiếm

        pygame.display.update()
        clock.tick(framerate)
 

def nhapTen(): 
    input_box = pygame.Rect(100, 100, 140, 32) 
    color_inactive = pygame.Color('lightskyblue3') 
    color_active = pygame.Color('dodgerblue2') 
    color = color_inactive 
    text = '' 
    active = False 

    while True: 
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
                        return text 
                    elif event.key == pygame.K_BACKSPACE: 
                        text = text[:-1] 
                    else: 
                        text += event.unicode 

        SCREEN.fill((30, 30, 30)) 
        txt_surface = get_font(TEXT_SIZE).render(text, True, color) 
        width = max(200, txt_surface.get_width()+10) 
        input_box.w = width 
        SCREEN.blit(txt_surface, (input_box.x+5, input_box.y+5)) 
        pygame.draw.rect(SCREEN, color, input_box, 2) 
        pygame.display.flip() 
        clock.tick(30) 

def choose_difficulty():
    while True:
        SCREEN.blit(BG, (0, 0))
        USER_MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = get_font(TEXT_TOP).render("CHOOSE DIFFICULTY", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(SCREEN_WIDTH // 2, 100))

        EASY_BUTTON = Button(image=None, pos=(SCREEN_WIDTH // 2, 200),
                            text_input="NORMAL", font=get_font(TEXT_SIZE), base_color="#d7fcd4", hovering_color="Red")
        HARD_BUTTON = Button(image=None, pos=(SCREEN_WIDTH // 2, 260),
                            text_input="HARD", font=get_font(TEXT_SIZE), base_color="#d7fcd4", hovering_color="Red")
        SUPER_HARD_BUTTON = Button(image=None, pos=(SCREEN_WIDTH // 2, 320),  # Thêm nút "SIÊU KHÓ"
                            text_input="SUPER HARD", font=get_font(TEXT_SIZE), base_color="#d7fcd4", hovering_color="Red")
        BACK_BUTTON = Button(image=None, pos=(SCREEN_WIDTH // 2, 450),
                            text_input="BACK", font=get_font(TEXT_SIZE), base_color="#d7fcd4", hovering_color="Red")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [EASY_BUTTON, HARD_BUTTON, SUPER_HARD_BUTTON, BACK_BUTTON]:
            button.changeColor(USER_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if EASY_BUTTON.checkForInput(USER_MOUSE_POS):
                    game_loop("normal")
                if HARD_BUTTON.checkForInput(USER_MOUSE_POS):
                    game_loop("hard", "scoreboardadvanced.csv")
                if SUPER_HARD_BUTTON.checkForInput(USER_MOUSE_POS):
                    game_loop("super_hard", "superhardscoreboard.csv")
                if BACK_BUTTON.checkForInput(USER_MOUSE_POS):
                    main_menu()

        pygame.display.update()
        clock.tick(framerate)


def play():
    while True:
        SCREEN.blit(BG, (0, 0))
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = get_font(TEXT_TOP).render("SNAKE GAME", True, "#b68f40")  # Changed title
        MENU_RECT = MENU_TEXT.get_rect(center=(SCREEN_WIDTH // 2, 100))

        # Changed button texts and positions for better layout
        PLAY_GAME_BUTTON = Button(image=None, pos=(SCREEN_WIDTH // 2, 200),
                                 text_input="PLAY GAME", font=get_font(TEXT_SIZE), base_color="#d7fcd4",
                                 hovering_color="Red")
        DIFFICULTY_BUTTON = Button(image=None, pos=(SCREEN_WIDTH // 2, 260),
                                   text_input="DIFFICULTY", font=get_font(TEXT_SIZE), base_color="#d7fcd4",
                                   hovering_color="Red")

        BACK_BUTTON = Button(image=None, pos=(SCREEN_WIDTH // 2, 420),
                             text_input="BACK", font=get_font(TEXT_SIZE), base_color="#d7fcd4", hovering_color="Red")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_GAME_BUTTON, DIFFICULTY_BUTTON, BACK_BUTTON]:  # Removed SCOREBOARD_BUTTON
            button.changeColor(PLAY_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_GAME_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    choose_difficulty() # Default difficulty is normal
                if DIFFICULTY_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    choose_difficulty()
                if BACK_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        pygame.display.update()
        clock.tick(framerate)

USERNAME = ""  # Biến toàn cục lưu tên người dùng

def main_menu():
    global USERNAME
    while True:
        SCREEN.blit(BG, (0, 0))

        if not USERNAME:
            login_text = get_font(TEXT_TOP).render("PLEASE LOGIN", True, "red")
            login_rect = login_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
            SCREEN.blit(login_text, login_rect)

            LOGIN_BUTTON = Button(None, (400, 300), "LOGIN", get_font(TEXT_SIZE), "white", "red")
            LOGIN_BUTTON.changeColor(pygame.mouse.get_pos())
            LOGIN_BUTTON.update(SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if LOGIN_BUTTON.checkForInput(pygame.mouse.get_pos()):
                        USERNAME = login_screen(SCREEN, BG, get_font, clock, framerate)
                        print(f"Logged in as: {USERNAME}")

            pygame.display.update()
            clock.tick(framerate)
            continue

        menu_text = get_font(TEXT_TOP).render(f"WELCOME {USERNAME.upper()}", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        SCREEN.blit(menu_text, menu_rect)

        PLAY_BUTTON = Button(None, (400, 200), "PLAY GAME", get_font(TEXT_SIZE), "white", "red")
        SCOREBOARD_BUTTON = Button(None, (400, 300), "SCOREBOARD", get_font(TEXT_SIZE), "white", "red")
        QUIT_BUTTON = Button(None, (400, 400), "QUIT", get_font(TEXT_SIZE), "white", "red")

        for button in [PLAY_BUTTON, SCOREBOARD_BUTTON, QUIT_BUTTON]:
            button.changeColor(pygame.mouse.get_pos())
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    choose_difficulty()  # Gọi trực tiếp màn hình chọn độ khó
                if SCOREBOARD_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    scoreBoardMenu()
                if QUIT_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        clock.tick(framerate)




def main():
    global USERNAME
    pygame.init()
    SCREEN = pygame.display.set_mode((800, 600))
    BG = pygame.image.load("images/b2.jpg")
    clock = pygame.time.Clock()
    framerate = 60

    USERNAME = ""  # Lưu tên người dùng
    USERNAME = login_screen(SCREEN, BG_GAME, get_font, clock, framerate)  # Đăng nhập trước khi vào menu
    print(f"Logged in as: {USERNAME}")
    main_menu()

if __name__ == '__main__':
    main()