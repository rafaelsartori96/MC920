## Rafael Sartori M. Santos, 186154
##
## Utilidades para processamento de imagem

import numpy as np # Para vetorizar a imagem
import cv2 # OpenCV para lidar com imagens


## Função para abrir imagem
def abrir_imagem(caminho):
    # Carregamos imagem utilizando OpenCV
    return list(map(np.asfarray, cv2.split(cv2.imread(caminho, cv2.IMREAD_UNCHANGED))))


## Função para salvar a imagem
def salvar_imagem(caminho, imagem):
    # Utilizamos OpenCV para salvar imagem no novo caminho
    cv2.imwrite(caminho, imagem)
