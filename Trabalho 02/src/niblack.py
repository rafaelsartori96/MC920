## Rafael Sartori M. Santos, 186154
##
## Método de limiarização de Niblack
##
## Para uma vizinhança Z nxn, o limiar T do pixel (x, y) é dado por:
##      T(x, y) = Z_avg + k * Z_dp
## onde Z_{avg, dp} são, respectivamente, a média e desvio padrão de Z.

# Definimos o tamanho do filtro (deve ser ímpar)
DIMENSAO_FILTRO_N = 7

import numpy as np
import util


# Aplicamos a limiarização de Niblack (removendo borda)
def aplicar_niblack(imagem, args):
    return util.limiarizacao_local(
        imagem, filtro_shape, aplicar_threshold, args
    )


# Função de aplicação da limiarização
def aplicar_threshold(imagem, y, x, k=0.8, **kwargs):
    seccao = imagem[
        (y - filtro_centro):(y + filtro_centro + 1),
        (x - filtro_centro):(x + filtro_centro + 1)
    ]

    # Determinamos média
    z_avg, z_dp = (seccao.mean(), seccao.std())
    limiar = z_avg + k * z_dp

    # Fazemos a limiarização
    return 1 if imagem[y][x] >= limiar else 0


# Criamos o filtro
filtro_shape = (DIMENSAO_FILTRO_N, DIMENSAO_FILTRO_N)
filtro_centro = DIMENSAO_FILTRO_N // 2
