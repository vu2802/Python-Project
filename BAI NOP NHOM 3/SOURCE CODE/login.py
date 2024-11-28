import pygame
import sys
from player_manager import PlayerManager, Player

def login_screen(screen, bg, get_font, clock, framerate):
    pygame.mixer.init()
    pygame.mixer.music.load("background_music.mp3")
    pygame.mixer.music.play(-1)

    input_box = pygame.Rect(300, 300, 200, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    username = ''
    message = ''  # Biến để lưu thông báo

    player_manager = PlayerManager()
    player_manager.load_players("scoreboardnormal.csv")

    while True:
        screen.blit(bg, (0, 0))
        login_text = get_font(40).render("LOGIN", True, "#b68f40")
        login_rect = login_text.get_rect(center=(screen.get_width() // 2, 100))
        screen.blit(login_text, login_rect)

        # Hiển thị thông báo nếu có
        if message:
            message_surface = get_font(30).render(message, True, (255, 0, 0))  # Màu đỏ cho thông báo
            message_rect = message_surface.get_rect(center=(screen.get_width() // 2, 200))
            screen.blit(message_surface, message_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
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
                        if not username.strip():  # Kiểm tra tên trống
                            message = "Username cannot be empty!"
                        elif player_manager.find_player(username):
                            message = "Username already exists!"
                        else:
                            player = Player(username, None, None, None, 0)
                            player_manager.add_player(player)  # Thêm người chơi mới vào danh sách trong bộ nhớ
                            # Không lưu vào file tại đây
                            return username  # Trả lại tên người dùng

                    elif event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                        message = ''  # Xóa thông báo khi người dùng nhập lại tên
                    else:
                        username += event.unicode
                        message = ''  # Xóa thông báo khi người dùng nhập lại tên

        txt_surface = get_font(32).render(username, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()
        clock.tick(framerate)

def display_message(screen, message, get_font):
    """Hiển thị thông báo tạm thời trên màn hình."""
    msg_surface = get_font(30).render(message, True, (255, 0, 0))
    msg_rect = msg_surface.get_rect(center=(screen.get_width() // 2, 400))
    screen.blit(msg_surface, msg_rect)
    pygame.display.update()
    pygame.time.wait(2000)