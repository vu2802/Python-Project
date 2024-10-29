import pygame
import random
import keyboard

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

class Ran:
    def __init__(self):
        self.vi_tri = [(100, 100), (80, 100), (60, 100)]  # Vi tri ran ban dau
        self.huong = 'PHAI'
        self.huong_thay_doi = self.huong
    
    def thay_doi_huong(self, huong):
        while True:
            if keyboard.is_pressed("up"):
                self.huong_thay_doi = 'LEN'

            elif keyboard.is_pressed("down"):
                self.huong_thay_doi = 'XUONG'

            elif keyboard.is_pressed("left"):
                self.huong_thay_doi = 'TRAI'

            elif keyboard.is_pressed("right"):
                self.huong_thay_doi = 'PHAI'

            elif keyboard.is_pressed("esc"):
                break

    def di_chuyen(self):
        self.thay_doi_huong()
        self.huong = self.huong_thay_doi

        x,y = self.vi_tri[0]

        if self.huong == 'LEN':
            y += 20

        elif self.huong == 'XUONG':
            y -= 20

        elif self.huong == 'TRAI':
            x -= 20

        elif self.huong == 'PHAI':
            x += 20

        self.vi_tri.insert(0, (x,y))
        self.vi_tri.pop()

        
    def tang_chieu_dai(self):
        x,y = self.vi_tri[2]
        if '''Hàm ăn thức ăn''':
            self.vi_tri.append((x,y))
    
    def kiem_tra_va_cham(self):
        x,y = self.vi_tri[0]

        if (x,y) in self.vi_tri[1:]:
            return False
        
        return True

    def lay_vi_tri_dau(self):
        return self.vi_tri[0]
   