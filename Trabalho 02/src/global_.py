## Rafael Sartori M. Santos, 186154
##
## Método global de limiarização

import numpy as np


# Aplicamos a limiarização global de forma vetorizada
def aplicar_global(imagem, k=128, **kwargs):
    return np.where(imagem >= k, 1, 0)
