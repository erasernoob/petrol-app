import pandas as pd
from service import utils


def main(guiji, lbmx, pailiang, fluidden, n, K, miu, taof, Dw, Rzz, rzz, Lzz, Rzt, rzt, Lzt, yx, yxmd, H):
    
    print("\nCalculating ECD...")
    ECD, ECDyx, Sk = utils.hydro_limit_eye(guiji, lbmx, pailiang, fluidden, n, K, miu, taof, Dw, Rzz, rzz, Lzz, Rzt, rzt, Lzt, yx, yxmd, H)
    
    if yx == 1:
        return ECDyx.flatten(), Sk.flatten()
    else:
        return ECD.flatten(), Sk.flatten()
    