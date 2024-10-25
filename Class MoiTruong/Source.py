import pygame
import random

pygame.init()

# Hang so cho cua so tro choi
RONG_CUA_SO = 600
CAO_CUA_SO = 400
KICH_THUOC_O = 20

# Mau sac
DEN = (0, 0, 0)
TRANG = (255, 255, 255)
XANH_LA = (0, 255, 0)
DO = (255, 0, 0)

# Viet tiep code tu day tro xuong

class MoiTruong:
    def __init__(self, rong_cua_so, cao_cua_so):
        self.rong_cua_so = rong_cua_so
        self.cao_cua_so = cao_cua_so
        self.cua_so = pygame.display.set_mode((self.rong_cua_so, self.cao_cua_so))
        pygame.display.set_caption('Tro choi Ran san moi')
    
    def ve_cac_phan_tu(self, ran, thuc_an):

    def kiem_tra_game_over(self, ran):
        dau = ran.body[0]
        if dau[0] >= self.rong_cua_so or dau[0] < 0 or dau[1] >= self.cao_cua_so or dau[1] < 0:
            return True  # Game over nếu đầu rắn va chạm với tường

        # Kiểm tra va chạm với chính mình
        if dau in ran.body[1:]:
            return True

        # Nếu không có va chạm, trò chơi tiếp tục
        return False
