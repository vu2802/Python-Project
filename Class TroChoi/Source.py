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

#Viet tiep code tu day tro xuong

class TroChoi:
    def __init__(self):
        self.ran = Ran()
        self.thuc_an = ThucAn()
        self.diem = DiemSo()
        self.moi_truong = MoiTruong(RONG_CUA_SO, CAO_CUA_SO)
        self.dong_ho = pygame.time.Clock()
    
    def chay_game(self):

    