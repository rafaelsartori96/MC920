## Rafael Sartori M. Santos, 186154
##
## Método de limiarização local do contraste

import numpy as np
import util


# Aplicamos a limiarização do contraste (removendo borda)
def aplicar_filtro_contraste(imagem, **kwargs):
    return util.limiarizacao_local(imagem, aplicar_threshold, **kwargs)


# Função de aplicação da limiarização
def aplicar_threshold(imagem, y, x, padding, **kwargs):
    seccao = imagem[
        (y - padding):(y + padding + 1),
        (x - padding):(x + padding + 1)
    ]

    # Determinamos a contraste e esse será nosso limiar
    min_, max_ = (seccao.min(), seccao.max())
    imagem_ = imagem[y][x]

    # Determinamos a distância até o mínimo e máximo e limiarizamos
    return 1 if np.abs(imagem_ - min_) > np.abs(imagem_ - max_) else 0
    # se a distância do pixel até o mínimo é maior que a distância do pixel até
    # o máximo, significa que está mais próximo do máximo e que deve ser
    # considerado pertencente ao objeto (não fundo)
