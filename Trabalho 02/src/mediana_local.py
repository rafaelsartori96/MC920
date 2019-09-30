## Rafael Sartori M. Santos, 186154
##
## Método de limiarização local da mediana

import numpy as np
import util


# Aplicamos a limiarização da mediana (removendo borda)
def aplicar_mediana(imagem, **kwargs):
    return util.limiarizacao_local(imagem, aplicar_threshold, **kwargs)


# Função de aplicação da limiarização
def aplicar_threshold(imagem, y, x, padding, **kwargs):
    seccao = imagem[
        (y - padding):(y + padding + 1),
        (x - padding):(x + padding + 1)
    ]

    # Determinamos a mediana e esse será nosso limiar
    limiar = np.median(seccao)
    # Fazemos a limiarização
    return 1 if imagem[y][x] >= limiar else 0
