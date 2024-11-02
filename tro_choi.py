import pygame
from ran import Ran
from thuc_an import ThucAn
from diem_so import DiemSo
from moi_truong import MoiTruong
from constants import RONG_CUA_SO, CAO_CUA_SO

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
            
            self.ran.di_chuyen()
            
            if self.ran.body[0] == self.thuc_an.vi_tri:
                self.ran.tang_chieu_dai()
                self.diem.cap_nhat_diem()
                self.thuc_an.vi_tri = self.thuc_an.tao_vi_tri_moi(self.ran)
            
            if self.moi_truong.kiem_tra_game_over(self.ran):
                chay = False
            
            # Sửa lại dòng này
            self.moi_truong.ve_cac_phan_tu(self.ran, self.thuc_an)
            self.diem.hien_thi_diem(self.moi_truong.cua_so)
            
            self.dong_ho.tick(10)

        pygame.quit()