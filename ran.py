from constants import KICH_THUOC_O

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

        self.body.insert(0, (x, y))
        self.body.pop()
        
    def tang_chieu_dai(self):
        self.body.append(self.body[-1])