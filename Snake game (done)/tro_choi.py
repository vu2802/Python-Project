import pygame
import random
from constants import KICH_THUOC_O, RONG_CUA_SO, CAO_CUA_SO, TRANG, DEN
from ran import Ran
from thuc_an import ThucAn
from diem_so import DiemSo
from moi_truong import MoiTruong

# Lớp Tro Choi quản lý toàn bộ trò chơi, bao gồm điều khiển và vòng lặp chính
class TroChoi:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load('background_music.mp3')
        pygame.mixer.music.play(-1)
        self.an_thuc_an_am_thanh = pygame.mixer.Sound('eat_sound.wav')
        self.thua_am_thanh = pygame.mixer.Sound('game_over.wav')

        self.ran = Ran()
        self.thuc_an = ThucAn()
        self.diem = DiemSo()
        self.moi_truong = MoiTruong(RONG_CUA_SO, CAO_CUA_SO)
        self.dong_ho = pygame.time.Clock()

    # Hiển thị thông báo game over
    def hien_thi_thong_bao(self, message):
        font = pygame.font.SysFont('Arial', 40)
        thong_bao = font.render(message, True, TRANG)
        rect = thong_bao.get_rect(center=(RONG_CUA_SO // 2, CAO_CUA_SO // 2))
        self.moi_truong.cua_so.blit(thong_bao, rect)
        pygame.display.flip()
        pygame.time.wait(2000)

    # Cập nhật tốc độ di chuyển dựa trên điểm
    def cap_nhat_toc_do(self):
        toc_do = 10 + (self.diem.diem_hien_tai // 5)
        self.dong_ho.tick(toc_do)

    # Vòng lặp chính của trò chơi
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

            # Kiểm tra khi rắn ăn thức ăn
            if self.ran.body[0] == self.thuc_an.vi_tri:
                self.an_thuc_an_am_thanh.play(maxtime=500)
                self.ran.tang_chieu_dai()
                self.diem.cap_nhat_diem(self.thuc_an.loai)
                self.thuc_an = ThucAn()
                self.moi_truong.blocks = self.moi_truong.tao_block_moi(self.ran.body, self.thuc_an)

            # Kiểm tra điều kiện game over
            if self.moi_truong.kiem_tra_game_over(self.ran):
                pygame.mixer.music.stop()
                self.thua_am_thanh.play()
                self.hien_thi_thong_bao("Ban da thua!")
                chay = self.choi_lai_hoac_dung()
                if not chay:
                    break

            self.moi_truong.ve_cac_phan_tu(self.ran, self.thuc_an)
            self.diem.hien_thi_diem(self.moi_truong.cua_so)
            self.cap_nhat_toc_do()

        pygame.quit()

    # Lựa chọn chơi lại hoặc dừng trò chơi
    def choi_lai_hoac_dung(self):
        self.moi_truong.cua_so.fill(DEN)
        self.diem.hien_thi_diem(self.moi_truong.cua_so)
        pygame.display.flip()

        font = pygame.font.SysFont('Arial', 26)
        thong_bao = font.render("Nhan C de choi tiep hoac Q de dung.", True, TRANG)
        rect = thong_bao.get_rect(center=(RONG_CUA_SO // 2, CAO_CUA_SO // 2))
        self.moi_truong.cua_so.blit(thong_bao, rect)
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        pygame.mixer.music.play(-1)
                        self.ran = Ran()
                        self.thuc_an = ThucAn()
                        self.diem = DiemSo()
                        return True
                    elif event.key == pygame.K_q:
                        return False