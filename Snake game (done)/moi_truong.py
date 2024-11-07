import pygame
import random
from constants import KICH_THUOC_O, RONG_CUA_SO, CAO_CUA_SO, XANH_LA, XANH_DUONG, DEN

# Lớp Môi Trường quản lý các yếu tố trên màn hình như rắn, thức ăn, và chướng ngại vật
class MoiTruong:
    def __init__(self, rong_cua_so, cao_cua_so):
        self.rong_cua_so = rong_cua_so
        self.cao_cua_so = cao_cua_so
        self.cua_so = pygame.display.set_mode((self.rong_cua_so, self.cao_cua_so))
        pygame.display.set_caption('Tro choi Ran san moi')
        self.blocks = self.tao_block_moi([])

    # Tạo vị trí ngẫu nhiên cho các chướng ngại vật
    def tao_block_moi(self, ran_body, thuc_an=None):
        blocks = []
        while len(blocks) < 4:
            x = random.randint(0, (self.rong_cua_so - KICH_THUOC_O) // KICH_THUOC_O) * KICH_THUOC_O
            y = random.randint(0, (CAO_CUA_SO - KICH_THUOC_O) // KICH_THUOC_O) * KICH_THUOC_O
            if (x, y) not in ran_body and (thuc_an is None or (x, y) != thuc_an.vi_tri):
                blocks.append((x, y))
        return blocks

    # Vẽ các yếu tố trò chơi như rắn, thức ăn, và chướng ngại vật
    def ve_cac_phan_tu(self, ran, thuc_an):
        self.cua_so.fill(DEN)  # Xóa màn hình
        # Vẽ rắn
        for vi_tri in ran.body:
            pygame.draw.rect(self.cua_so, XANH_LA, (vi_tri[0], vi_tri[1], KICH_THUOC_O, KICH_THUOC_O))
        # Vẽ thức ăn
        thuc_an.hien_thi_thuc_an(self.cua_so)
        # Vẽ chướng ngại vật
        for block in self.blocks:
            pygame.draw.rect(self.cua_so, XANH_DUONG, (block[0], block[1], KICH_THUOC_O, KICH_THUOC_O))
        pygame.display.flip()

    # Kiểm tra điều kiện game over
    def kiem_tra_game_over(self, ran):
        dau = ran.body[0]
        # Game over khi rắn va vào chướng ngại vật hoặc thân mình
        if dau in self.blocks or dau in ran.body[1:]:
            return True
        return False