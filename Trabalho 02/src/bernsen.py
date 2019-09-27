## Rafael Sartori M. Santos, 186154
##
## Método de limiarização de Bernsen

import numpy as np
import util


# Aplicamos a limiarização de Bernsen
def aplicar_bernsen(imagem):
    return np.where(imagem >= LIMIAR, 255, 0)
