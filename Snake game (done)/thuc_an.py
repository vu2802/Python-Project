import random
import pygame
from constants import KICH_THUOC_O, RONG_CUA_SO, CAO_CUA_SO, VANG, DO

# Lớp Thức Ăn tạo thức ăn bình thường và đặc biệt
class ThucAn:
    # Khởi tạo loại thức ăn (bình thường hoặc đặc biệt) và vị trí ngẫu nhiên
    def __init__(self):
        self.loai = random.choices(['thuong', 'dac_biet'], weights=[80, 20])[0]
        self.vi_tri = self.tao_vi_tri_moi()

    # Tạo vị trí ngẫu nhiên cho thức ăn, đảm bảo không trùng với thân rắn
    def tao_vi_tri_moi(self, ran=None):
        while True:
            x = random.randint(0, (RONG_CUA_SO - KICH_THUOC_O) // KICH_THUOC_O) * KICH_THUOC_O
            y = random.randint(0, (CAO_CUA_SO - KICH_THUOC_O) // KICH_THUOC_O) * KICH_THUOC_O
            if ran is None or (x, y) not in ran.body:
                return (x, y)

    # Hiển thị thức ăn lên cửa sổ trò chơi
    def hien_thi_thuc_an(self, cua_so):
        color = DO if self.loai == 'thuong' else VANG
        pygame.draw.rect(cua_so, color, (self.vi_tri[0], self.vi_tri[1], KICH_THUOC_O, KICH_THUOC_O))