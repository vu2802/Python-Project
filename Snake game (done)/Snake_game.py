# Import các thư viện cần thiết
import random   # Để tạo vị trí ngẫu nhiên cho thức ăn và chướng ngại vật
import pygame   # Thư viện hỗ trợ đồ họa và âm thanh cho trò chơi
import sys      # Thư viện hệ thống dùng để quản lý sự kiện thoát trò chơi

# Hằng số cho kích thước cửa sổ trò chơi và ô trong trò chơi
RONG_CUA_SO = 600       # Chiều rộng của cửa sổ trò chơi
CAO_CUA_SO = 400        # Chiều cao của cửa sổ trò chơi
KICH_THUOC_O = 20       # Kích thước mỗi ô vuông

# Định nghĩa các màu sắc sử dụng trong trò chơi
DEN = (0, 0, 0)         # Màu nền cho cửa sổ trò chơi
TRANG = (255, 255, 255) # Màu cho điểm số và thông báo
XANH_LA = (0, 255, 0)   # Màu của thân rắn
DO = (255, 0, 0)        # Màu của thức ăn bình thường
VANG = (255, 255, 0)    # Màu của thức ăn đặc biệt
XANH_DUONG = (0, 0, 255) # Màu của chướng ngại vật

# Lớp Rắn quản lý thân rắn và hướng di chuyển
class Ran:
    # Khởi tạo thân rắn và hướng di chuyển ban đầu
    def __init__(self):
        self.body = [(100, 100), (80, 100), (60, 100)]  # Vị trí ban đầu của thân rắn
        self.huong = 'PHAI'                             # Hướng di chuyển ban đầu của rắn
        self.huong_thay_doi = self.huong                # Hướng thay đổi khi có lệnh từ bàn phím

    # Thay đổi hướng dựa trên phím người chơi nhấn
    def thay_doi_huong(self, huong):
        # Điều kiện để tránh cho rắn tự quay ngược lại và ăn vào chính nó
        if (huong == 'LEN' and self.huong != 'XUONG') or \
           (huong == 'XUONG' and self.huong != 'LEN') or \
           (huong == 'TRAI' and self.huong != 'PHAI') or \
           (huong == 'PHAI' and self.huong != 'TRAI'):
            self.huong_thay_doi = huong

    # Phương thức di chuyển của rắn
    def di_chuyen(self):
        # Cập nhật hướng di chuyển và vị trí mới của đầu rắn
        self.huong = self.huong_thay_doi
        x, y = self.body[0]

        # Thay đổi vị trí đầu rắn dựa trên hướng di chuyển hiện tại
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

        self.body.insert(0, (x, y))  # Cập nhật đầu rắn vào thân
        self.body.pop()  # Loại bỏ đoạn cuối của thân để duy trì chiều dài

    # Tăng chiều dài thân rắn khi ăn thức ăn
    def tang_chieu_dai(self):
        self.body.append(self.body[-1])

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

# Lớp Môi Trường quản lý các yếu tố trên màn hình như rắn, thức ăn, và chướng ngại vật
class MoiTruong:
    def __init__(self, rong_cua_so, cao_cua_so):
        self.rong_cua_so = rong_cua_so
        self.cao_cua_so = cao_cua_so
        self.cua_so = pygame.display.set_mode((self.rong_cua_so, self.cao_cua_so))
        pygame.display.set_caption('Tro choi Ran san moi')
        self.blocks = self.tao_block_moi([])

    # Tạo vị trí ngẫu nhiên cho các chướng ngại vật
    def tao_block_moi(self, ran_body, thuc_an=None):
        blocks = []
        while len(blocks) < 4:
            x = random.randint(0, (self.rong_cua_so - KICH_THUOC_O) // KICH_THUOC_O) * KICH_THUOC_O
            y = random.randint(0, (CAO_CUA_SO - KICH_THUOC_O) // KICH_THUOC_O) * KICH_THUOC_O
            if (x, y) not in ran_body and (thuc_an is None or (x, y) != thuc_an.vi_tri):
                blocks.append((x, y))
        return blocks

    # Vẽ các yếu tố trò chơi như rắn, thức ăn, và chướng ngại vật
    def ve_cac_phan_tu(self, ran, thuc_an):
        self.cua_so.fill(DEN)  # Xóa màn hình
        # Vẽ rắn
        for vi_tri in ran.body:
            pygame.draw.rect(self.cua_so, XANH_LA, (vi_tri[0], vi_tri[1], KICH_THUOC_O, KICH_THUOC_O))
        # Vẽ thức ăn
        thuc_an.hien_thi_thuc_an(self.cua_so)
        # Vẽ chướng ngại vật
        for block in self.blocks:
            pygame.draw.rect(self.cua_so, XANH_DUONG, (block[0], block[1], KICH_THUOC_O, KICH_THUOC_O))
        pygame.display.flip()

    # Kiểm tra điều kiện game over
    def kiem_tra_game_over(self, ran):
        dau = ran.body[0]
        # Game over khi rắn va vào chướng ngại vật hoặc thân mình
        if dau in self.blocks or dau in ran.body[1:]:
            return True
        return False

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

def main():
    tro_choi = TroChoi()
    tro_choi.chay_game()

if __name__ == "__main__":
    main()
