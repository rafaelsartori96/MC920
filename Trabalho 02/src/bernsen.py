## Rafael Sartori M. Santos, 186154
##
## Método de limiarização de Bernsen
##
## Para uma vizinhança Z nxn, o limiar T do pixel (x, y) é dado por:
##      T(x, y) = (Z_min + Z_max) / 2
## onde Z_{min, max} é, respectivamente, o mínimo e máximo valor em Z.

# Definimos o tamanho do filtro (deve ser ímpar)
DIMENSAO_FILTRO_N = 7

import numpy as np
import util


# Aplicamos a limiarização de Bernsen (removendo borda)
def aplicar_bernsen(imagem):
    return util.limiarizacao_local(imagem, filtro_shape, aplicar_threshold)


# Função de aplicação da limiarização
def aplicar_threshold(imagem, y, x):
    seccao = imagem[
        (y - filtro_centro):(y + filtro_centro + 1),
        (x - filtro_centro):(x + filtro_centro + 1)
    ]

    # Determinamos mínimo e máximo
    z_min, z_max = (seccao.min(), seccao.max())
    limiar = (z_min + z_max) / 2

    # Fazemos a limiarização
    return 1 if imagem[y][x] >= limiar else 0


# Criamos o filtro
filtro_shape = (DIMENSAO_FILTRO_N, DIMENSAO_FILTRO_N)
filtro_centro = DIMENSAO_FILTRO_N // 2
