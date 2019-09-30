## Rafael Sartori M. Santos, 186154
##
## Método de limiarização de Phansalskar-More-Sabale
##
## Para uma vizinhança Z nxn, o limiar T do pixel (x, y) é dado por:
##      T(x, y) = Z_avg * (1 + p * exp(-q * Z_avg) + k * ((Z_dp / R) - 1))
## onde Z_{avg, dp} são, respectivamente, a média e desvio padrão de Z, k, R, p
## e q, parâmetros.

import numpy as np
import util


# Aplicamos a limiarização de Phansalskar-More-Sabale (removendo borda)
def aplicar_pms(imagem, **kwargs):
    return util.limiarizacao_local(imagem, aplicar_threshold, **kwargs)


# Função de aplicação da limiarização
def aplicar_threshold(
    imagem, y, x, padding, k=0.25, R=0.5, p=2, q=10, **kwargs
):
    seccao = imagem[
        (y - padding):(y + padding + 1),
        (x - padding):(x + padding + 1)
    ]

    # Determinamos média e desvio padrão
    z_avg, z_dp = (seccao.mean(), seccao.std())
    limiar = z_avg * (1 + p * np.exp(-q * z_avg) + k * ((z_dp / R) - 1))

    # Fazemos a limiarização
    return 1 if imagem[y][x] >= limiar else 0
