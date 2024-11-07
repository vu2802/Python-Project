from constants import KICH_THUOC_O, RONG_CUA_SO, CAO_CUA_SO
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