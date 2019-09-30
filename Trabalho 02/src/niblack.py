## Rafael Sartori M. Santos, 186154
##
## Método de limiarização de Niblack
##
## Para uma vizinhança Z nxn, o limiar T do pixel (x, y) é dado por:
##      T(x, y) = Z_avg + k * Z_dp
## onde Z_{avg, dp} são, respectivamente, a média e desvio padrão de Z.

import numpy as np
import util


# Aplicamos a limiarização de Niblack (removendo borda)
def aplicar_niblack(imagem, **kwargs):
    return util.limiarizacao_local(
        imagem, aplicar_threshold, **kwargs
    )


# Função de aplicação da limiarização
def aplicar_threshold(imagem, y, x, padding, k=0.8, **kwargs):
    seccao = imagem[
        (y - padding):(y + padding + 1),
        (x - padding):(x + padding + 1)
    ]

    # Determinamos média
    z_avg, z_dp = (seccao.mean(), seccao.std())
    limiar = z_avg + k * z_dp

    # Fazemos a limiarização
    return 1 if imagem[y][x] >= limiar else 0
