## Rafael Sartori M. Santos, 186154
##
## Método global de limiarização

import util

def retorna(imagem, y, x):
    return imagem[y][x]

camadas = util.abrir_imagem("imgs/baboon.pgm")
camadas_final = []

for camada in camadas:
    camadas_final.append(util.limiarizacao_local(camada, (31, 31), retorna))

util.salvar_imagem("imgs/baboon-faznada.pgm", camadas_final)

