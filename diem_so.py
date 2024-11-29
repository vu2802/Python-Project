import pygame
from constants import TRANG

class DiemSo:
    def __init__(self):
        self.diem_hien_tai = 0

    def cap_nhat_diem(self):
        self.diem_hien_tai += 1

    def hien_thi_diem(self, cua_so):
        font = pygame.font.SysFont('Arial', 25)
        diem_surface = font.render(f'Điểm: {self.diem_hien_tai}', True, TRANG)
        cua_so.blit(diem_surface, (10, 10))