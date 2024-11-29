import random
import pygame
import sys

# Hằng số cho cửa sổ trò chơi
RONG_CUA_SO = 600
CAO_CUA_SO = 400
KICH_THUOC_O = 20

# Màu sắc
DEN = (0, 0, 0)
TRANG = (255, 255, 255)
XANH_LA = (0, 255, 0)
DO = (255, 0, 0)  # Màu cho thức ăn bình thường
VANG = (255, 255, 0)  # Màu cho thức ăn đặc biệt
XANH_DUONG = (0, 0, 255)

class Ran:
    def __init__(self):
        self.body = [(100, 100), (80, 100), (60, 100)]
        self.huong = 'PHAI'
        self.huong_thay_doi = self.huong

    def thay_doi_huong(self, huong):
        if (huong == 'LEN' and self.huong != 'XUONG') or \
           (huong == 'XUONG' and self.huong != 'LEN') or \
           (huong == 'TRAI' and self.huong != 'PHAI') or \
           (huong == 'PHAI' and self.huong != 'TRAI'):
            self.huong_thay_doi = huong

    def di_chuyen(self):
        self.huong = self.huong_thay_doi
        x, y = self.body[0]

        if self.huong == 'LEN':
            y -= KICH_THUOC_O
        elif self.huong == 'XUONG':
            y += KICH_THUOC_O
        elif self.huong == 'TRAI':
            x -= KICH_THUOC_O
        elif self.huong == 'PHAI':
            x += KICH_THUOC_O

        # Di chuyển xuyên qua tường
        x = x % RONG_CUA_SO
        y = y % CAO_CUA_SO

        self.body.insert(0, (x, y))
        self.body.pop()

    def tang_chieu_dai(self):
        self.body.append(self.body[-1])

class ThucAn:
    def __init__(self):
        # Xác suất để thức ăn là loại đặc biệt
        self.loai = random.choices(['thuong', 'dac_biet'], weights=[80, 20])[0]
        self.vi_tri = self.tao_vi_tri_moi()

    def tao_vi_tri_moi(self, ran=None):
        while True:
            x = random.randint(0, (RONG_CUA_SO - KICH_THUOC_O) // KICH_THUOC_O) * KICH_THUOC_O
            y = random.randint(0, (CAO_CUA_SO - KICH_THUOC_O) // KICH_THUOC_O) * KICH_THUOC_O
            if ran is None or (x, y) not in ran.body:
                return (x, y)

    def hien_thi_thuc_an(self, cua_so):
        color = DO if self.loai == 'thuong' else VANG
        pygame.draw.rect(cua_so, color, (self.vi_tri[0], self.vi_tri[1], KICH_THUOC_O, KICH_THUOC_O))

class DiemSo:
    def __init__(self):
        self.diem_hien_tai = 0
        self.diem_cao = self.doc_diem_cao()

    def doc_diem_cao(self):
        try:
            with open('high_score.txt', 'r') as file:
                return int(file.read())
        except FileNotFoundError:
            return 0

    def cap_nhat_diem(self, loai):
        self.diem_hien_tai += 3 if loai == 'dac_biet' else 1
        if self.diem_hien_tai > self.diem_cao:
            self.diem_cao = self.diem_hien_tai
            with open('high_score.txt', 'w') as file:
                file.write(str(self.diem_cao))

    def hien_thi_diem(self, cua_so):
        font = pygame.font.SysFont('Fira Code', 25)
        diem_surface = font.render(f'Diem: {self.diem_hien_tai}  Cao nhat: {self.diem_cao}', True, TRANG)
        cua_so.blit(diem_surface, (10, 10))

class MoiTruong:
    def __init__(self, rong_cua_so, cao_cua_so):
        self.rong_cua_so = rong_cua_so
        self.cao_cua_so = cao_cua_so
        self.cua_so = pygame.display.set_mode((self.rong_cua_so, self.cao_cua_so))
        pygame.display.set_caption('Tro choi Ran san moi')
        self.blocks = self.tao_block_moi([])

    def tao_block_moi(self, ran_body, thuc_an=None):
        blocks = []
        while len(blocks) < 4:
            x = random.randint(0, (self.rong_cua_so - KICH_THUOC_O) // KICH_THUOC_O) * KICH_THUOC_O
            y = random.randint(0, (CAO_CUA_SO - KICH_THUOC_O) // KICH_THUOC_O) * KICH_THUOC_O
            if (x, y) not in ran_body and (thuc_an is None or (x, y) != thuc_an.vi_tri):
                blocks.append((x, y))
        return blocks

    def ve_cac_phan_tu(self, ran, thuc_an):
        self.cua_so.fill(DEN)
        
        for vi_tri in ran.body:
            pygame.draw.rect(self.cua_so, XANH_LA, (vi_tri[0], vi_tri[1], KICH_THUOC_O, KICH_THUOC_O))
        
        thuc_an.hien_thi_thuc_an(self.cua_so)
        
        for block in self.blocks:
            pygame.draw.rect(self.cua_so, XANH_DUONG, (block[0], block[1], KICH_THUOC_O, KICH_THUOC_O))

        pygame.display.flip()

    def kiem_tra_game_over(self, ran):
        dau = ran.body[0]

        if dau in self.blocks or dau in ran.body[1:]:
            return True

        return False

class TroChoi:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load('background_music.mp3')
        pygame.mixer.music.play(-1)  # Chơi nhạc nền liên tục
        self.an_thuc_an_am_thanh = pygame.mixer.Sound('eat_sound.wav')
        self.thua_am_thanh = pygame.mixer.Sound('game_over.wav')

        self.ran = Ran()
        self.thuc_an = ThucAn()
        self.diem = DiemSo()
        self.moi_truong = MoiTruong(RONG_CUA_SO, CAO_CUA_SO)
        self.dong_ho = pygame.time.Clock()

    def hien_thi_thong_bao(self, message):
        font = pygame.font.SysFont('Fira Code', 40)
        thong_bao = font.render(message, True, TRANG)
        rect = thong_bao.get_rect(center=(RONG_CUA_SO // 2, CAO_CUA_SO // 2))
        self.moi_truong.cua_so.blit(thong_bao, rect)
        pygame.display.flip()
        pygame.time.wait(2000)

    def cap_nhat_toc_do(self):
        toc_do = 10 + (self.diem.diem_hien_tai // 5)
        self.dong_ho.tick(toc_do)

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
                self.an_thuc_an_am_thanh.play(maxtime=500)  # Phát âm thanh khi ăn thức ăn và ngừng sau 500ms
                self.ran.tang_chieu_dai()
                self.diem.cap_nhat_diem(self.thuc_an.loai)
                self.thuc_an = ThucAn()
                self.moi_truong.blocks = self.moi_truong.tao_block_moi(self.ran.body, self.thuc_an)
            
            if self.moi_truong.kiem_tra_game_over(self.ran):
                pygame.mixer.music.stop()  # Dừng nhạc nền
                self.thua_am_thanh.play()  # Phát âm thanh kết thúc trò chơi
                self.hien_thi_thong_bao("Ban da thua!")
                chay = self.choi_lai_hoac_dung()
                if not chay:
                    break
            
            self.moi_truong.ve_cac_phan_tu(self.ran, self.thuc_an)
            self.diem.hien_thi_diem(self.moi_truong.cua_so)
            self.cap_nhat_toc_do()

        pygame.quit()

    def choi_lai_hoac_dung(self):
        self.moi_truong.cua_so.fill(DEN)
        self.diem.hien_thi_diem(self.moi_truong.cua_so)
        pygame.display.flip()
        
        font = pygame.font.SysFont('Fira Code', 26)
        thong_bao = font.render("Nhan C de choi tiep hoac Q de dung.", True, TRANG)
        rect = thong_bao.get_rect(center=(RONG_CUA_SO // 2, CAO_CUA_SO // 2))
        self.moi_truong.cua_so.blit(thong_bao, rect)
        pygame.display.flip()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        pygame.mixer.music.play(-1)  # Phát lại nhạc nền nếu chơi lại
                        self.ran = Ran()
                        self.thuc_an = ThucAn()
                        self.diem = DiemSo()
                        return True
                    elif event.key == pygame.K_q:
                        return False

def main():
    tro_choi = TroChoi()
    tro_choi.chay_game()

if __name__ == "__main__":
    main()
