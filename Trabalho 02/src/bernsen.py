## Rafael Sartori M. Santos, 186154
##
## Método de limiarização de Bernsen
##
## Para uma vizinhança Z nxn, o limiar T do pixel (x, y) é dado por:
##      T(x, y) = (Z_min + Z_max) / 2
## onde Z_{min, max} são, respectivamente, o mínimo e máximo valor em Z.

import numpy as np
import util


# Aplicamos a limiarização de Bernsen (removendo borda)
def aplicar_bernsen(imagem, **kwargs):
    return util.limiarizacao_local(
        imagem, aplicar_threshold, **kwargs
    )


# Função de aplicação da limiarização
def aplicar_threshold(imagem, y, x, padding, **kwargs):
    seccao = imagem[
        (y - padding):(y + padding + 1),
        (x - padding):(x + padding + 1)
    ]

    # Determinamos mínimo e máximo
    z_min, z_max = (seccao.min(), seccao.max())
    limiar = (z_min + z_max) / 2

    # Fazemos a limiarização
    return 1 if imagem[y][x] >= limiar else 0
