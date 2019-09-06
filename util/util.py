# Rafael Sartori M. Santos, 186154
#
# Utilidades para processamento de imagem

from matplotlib import pyplot as plt # para gráficos e imagens
import numpy as np # Para vetorizar a imagem
import cv2 # OpenCV para lidar com imagens


## Função para abrir imagem
def abrir_imagem(caminho):
    # Carregamos imagem utilizando OpenCV
    r, g, b = cv2.split(cv2.imread(caminho, cv2.IMREAD_UNCHANGED))
    return (np.array(r), np.array(g), np.array(b))


## Função para salvar a imagem
def salvar_imagem(caminho, imagem):
    # Utilizamos OpenCV para salvar imagem no novo caminho
    cv2.imwrite(caminho, imagem)


## Função para mostrar imagem utilizando matplotlib
def mostrar_imagens(imagem_original, imagem_alterada):
    # Criamos espaço para duas figuras quadradas
    figura = plt.figure(figsize=[TAMANHO_IMAGEM*2, TAMANHO_IMAGEM])
    rows, columns = (1, 2)
    # Adicionamos a original a esquerda
    subplot = figura.add_subplot(rows, columns, 1)
    plt.imshow(imagem_original, cmap='gray', interpolation='bicubic')
    # Deixamos de mostrar as coordenadas
    plt.xticks([])
    plt.yticks([])
    plt.title('Imagem original')
    # Adicionamos a alterada a direita
    subplot = figura.add_subplot(rows, columns, 2)
    plt.imshow(imagem_alterada, cmap='gray', interpolation='bicubic')
    # Deixamos de mostrar as coordenadas
    plt.xticks([])
    plt.yticks([])
    plt.title('Imagem alterada')
    # Mostramos a figura final
    plt.show()
