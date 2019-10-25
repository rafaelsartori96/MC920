## Rafael Sartori M. Santos, 186154
##
## Programa de utilidades

import cv2


def abrir_imagem(caminho):
    """Abrimos uma imagem utilizando OpenCV"""
    return cv2.imread(caminho, cv2.IMREAD_UNCHANGED)


def salvar_imagem(caminho, imagem):
    """Salvamos a imagem utilizando OpenCV"""
    return cv2.imwrite(caminho, imagem)
