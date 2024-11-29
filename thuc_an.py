import random
from constants import RONG_CUA_SO, CAO_CUA_SO, KICH_THUOC_O

class ThucAn:
    def __init__(self):
        self.vi_tri = self.tao_vi_tri_moi()

    def tao_vi_tri_moi(self, ran=None):
        while True:
            x = random.randint(0, (RONG_CUA_SO - KICH_THUOC_O) // KICH_THUOC_O) * KICH_THUOC_O
            y = random.randint(0, (CAO_CUA_SO - KICH_THUOC_O) // KICH_THUOC_O) * KICH_THUOC_O
            if ran is None or (x, y) not in ran.body:
                return (x, y)