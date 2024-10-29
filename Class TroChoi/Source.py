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
        chay = True
        while chay:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    chay = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.ran.thay_doi_huong('LEN')
                    elif event.key == pygame.K_DOWN:
                        self.ran.thay_doi_huong('XUONG')
                    elif event.key == pygame.K_LEFT:
                        self.ran.thay_doi_huong('TRAI')
                    elif event.key == pygame.K_RIGHT:
                        self.ran.thay_doi_huong('PHAI')
            
            # Cap nhat vi tri ran
            self.ran.di_chuyen()
            
            # Kiem tra ran voi thuc an
            if self.ran.lay_vi_tri_dau() == self.thuc_an.vi_tri:
                self.ran.tang_chieu_dai()
                self.diem.cap_nhat_diem()
                self.thuc_an.tao_vi_tri_moi(self.ran)
            
            #Kiem tra ket thuc tro choi
            if self.moi_truong.kiem_tra_game_over(self.ran):
                chay = False
            
            # Hien thi cac thanh phan tro choi
            self.moi_truong.ve_cac_phan_tu(self.ran, self.thuc_an)
            self.diem.hien_thi_diem(self.moi_truong.cua_so)
            
            # Toc do tro choi
            self.dong_ho.tick(10)

        # Thoat game
        pygame.quit()
    
