import pygame
from constants import TRANG
# Lớp Điểm Số theo dõi và cập nhật điểm hiện tại và điểm cao nhất
class DiemSo:
    def __init__(self):
        self.diem_hien_tai = 0
        self.diem_cao = self.doc_diem_cao()

    def doc_diem_cao(self):
        # Đọc điểm cao nhất từ file
        try:
            with open('high_score.txt', 'r') as file:
                return int(file.read())
        except FileNotFoundError:
            return 0

    # Cập nhật điểm dựa trên loại thức ăn ăn được
    def cap_nhat_diem(self, loai):
        self.diem_hien_tai += 3 if loai == 'dac_biet' else 1
        if self.diem_hien_tai > self.diem_cao:
            self.diem_cao = self.diem_hien_tai
            with open('high_score.txt', 'w') as file:
                file.write(str(self.diem_cao))

    # Hiển thị điểm trên cửa sổ trò chơi
    def hien_thi_diem(self, cua_so):
        font = pygame.font.SysFont('Arial', 25)
        diem_surface = font.render(f'Diem: {self.diem_hien_tai}  Cao nhat: {self.diem_cao}', True, TRANG)
        cua_so.blit(diem_surface, (10, 10))