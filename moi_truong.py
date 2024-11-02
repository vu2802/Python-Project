import pygame
from constants import DEN, XANH_LA, DO, KICH_THUOC_O

class MoiTruong:
    def __init__(self, rong_cua_so, cao_cua_so):
        self.rong_cua_so = rong_cua_so
        self.cao_cua_so = cao_cua_so
        self.cua_so = pygame.display.set_mode((self.rong_cua_so, self.cao_cua_so))
        pygame.display.set_caption('Trò chơi Rắn săn mồi')
    
    def ve_cac_phan_tu(self, ran, thuc_an):
        self.cua_so.fill(DEN)
        
        for vi_tri in ran.body:
            pygame.draw.rect(self.cua_so, XANH_LA, 
                           (vi_tri[0], vi_tri[1], KICH_THUOC_O, KICH_THUOC_O))
        
        pygame.draw.rect(self.cua_so, DO, 
                        (thuc_an.vi_tri[0], thuc_an.vi_tri[1], KICH_THUOC_O, KICH_THUOC_O))
        
        pygame.display.flip()
    
    def kiem_tra_game_over(self, ran):
        dau = ran.body[0]
        if dau[0] >= self.rong_cua_so or dau[0] < 0 or \
           dau[1] >= self.cao_cua_so or dau[1] < 0:
            return True
        
        if dau in ran.body[1:]:
            return True
        
        return False