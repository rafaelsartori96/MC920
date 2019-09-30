## Rafael Sartori M. Santos, 186154
##
## Método de limiarização local da média

import numpy as np
import util


# Aplicamos a limiarização da média (removendo borda)
def aplicar_media(imagem, **kwargs):
    return util.limiarizacao_local(imagem, aplicar_threshold, **kwargs)


# Função de aplicação da limiarização
def aplicar_threshold(imagem, y, x, padding, **kwargs):
    seccao = imagem[
        (y - padding):(y + padding + 1),
        (x - padding):(x + padding + 1)
    ]

    # Determinamos a média e esse será nosso limiar
    limiar = seccao.mean()
    # Fazemos a limiarização
    return 1 if imagem[y][x] >= limiar else 0
