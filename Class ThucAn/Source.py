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

class ThucAn:
    def __init__(self):
        self.vi_tri = (random.randint(0, (RONG_CUA_SO // KICH_THUOC_O) - 1) * KICH_THUOC_O,
                       random.randint(0, (CAO_CUA_SO // KICH_THUOC_O) - 1) * KICH_THUOC_O)

    def tao_vi_tri_moi(self, ran):
        while True:
            self.vi_tri = (random.randint(0, (RONG_CUA_SO // KICH_THUOC_O) - 1) * KICH_THUOC_O,
                           random.randint(0, (CAO_CUA_SO // KICH_THUOC_O) - 1) * KICH_THUOC_O)
            if self.vi_tri not in ran.vi_tri:
                break