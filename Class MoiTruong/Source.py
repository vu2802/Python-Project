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
        # Vẽ nền game
        self.cua_so.fill(DEN)
        
        # Vẽ rắn
        for vi_tri in ran.body:
            pygame.draw.rect(self.cua_so, XANH_LA, (vi_tri[0], vi_tri[1], KICH_THUOC_O, KICH_THUOC_O))
        
        # Vẽ thức ăn
        pygame.draw.rect(self.cua_so, DO, (thuc_an.vi_tri[0], thuc_an.vi_tri[1], KICH_THUOC_O, KICH_THUOC_O))
        
        # Cập nhật màn hình
        pygame.display.flip()
    
    def kiem_tra_game_over(self, ran):
        # Kiểm tra va chạm với tường
        dau = ran.body[0]
        if dau[0] >= self.rong_cua_so or dau[0] < 0 or dau[1] >= self.cao_cua_so or dau[1] < 0:
            return True
        
        # Kiểm tra va chạm với chính mình
        if dau in ran.body[1:]:
            return True
        
        # Nếu không có va chạm, trò chơi tiếp tục
        return False