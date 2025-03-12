import pandas as pd
from service import utils


def main(guiji, lbmx, pailiang, fluidden, n, K, miu, taof, Dw, Rzz, rzz, Lzz, Rzt, rzt, Lzt, yx, yxmd, H):
    
    print("\nCalculating ECD...")
    ECD, ECDyx, Sk = utils.hydro_limit_eye(guiji, lbmx, pailiang, fluidden, n, K, miu, taof, Dw, Rzz, rzz, Lzz, Rzt, rzt, Lzt, yx, yxmd, H)
    
    outfolder = utils.get_output_folder("裸眼延伸极限")
    timestamp = utils.get_timestamp()

    print("Hydro function parameters:")
    for name, value in locals().items():
        print(f"{name}: {value}")


    if yx == 1:
        ecd_df = pd.DataFrame({
            'Depth (m)': Sk.flatten(),
            'ECD (g/cm³)': ECDyx.flatten(),
        })
        ecd_df.to_excel( outfolder  / f'ECD_{timestamp}.xlsx', index=False)
        return ECDyx.flatten(), Sk.flatten()
    else:
        ecd_df = pd.DataFrame({
            'Depth (m)': Sk.flatten(),
            'ECD (g/cm³)': ECD.flatten(),
        })
        ecd_df.to_excel( outfolder  / f'ECD_{timestamp}.xlsx', index=False)
        return ECD.flatten(), Sk.flatten()
    