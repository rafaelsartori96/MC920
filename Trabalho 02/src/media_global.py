## Rafael Sartori M. Santos, 186154
##
## Método de limiarização global da média

import numpy as np
import util


# Aplicamos a limiarização da média globalmente
def aplicar_media(imagem, **kwargs):
    limiar = imagem.mean()
    return np.where(imagem >= limiar, 1, 0)
