## Rafael Sartori M. Santos, 186154
##
## Método global de limiarização

# Constante de limiar global
LIMIAR = 128

import numpy as np


# Aplicamos a limiarização global de forma vetorizada
def aplicar_global(imagem, **kwargs):
    return np.where(imagem >= LIMIAR, 1, 0)
