## Rafael Sartori M. Santos, 186154
##
## Método de limiarização global da mediana

import numpy as np
import util


# Aplicamos a limiarização da mediana globalmente
def aplicar_mediana(imagem, **kwargs):
    limiar = np.median(imagem)
    return np.where(imagem >= limiar, 1, 0)
