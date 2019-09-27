## Rafael Sartori M. Santos, 186154
##
## Utilidades para processamento de imagem

import numpy as np # Para vetorizar a imagem
import cv2 # OpenCV para lidar com imagens


## Função para abrir imagem
def abrir_imagem(caminho):
    # Carregamos imagem utilizando OpenCV
    return list(map(
        # para cada camada, fazemos vetor numpy
        np.asfarray,
        # dividimos em camadas
        cv2.split(cv2.imread(caminho, cv2.IMREAD_UNCHANGED))
    ))


## Função para salvar a imagem dada suas camadas
def salvar_imagem(caminho, camadas):
    # Juntamos as camadas da imagem e salvamos
    imagem = cv2.merge(camadas)
    # Utilizamos OpenCV para salvar imagem no novo caminho
    cv2.imwrite(caminho, imagem)


## Função para aplicar threasholding (limiarização) local dada a função de
## aplicação de threshold:
##      aplicar_threshold(imagem, y, x): retorna 0 ou 1
## Ignoraremos a borda da imagem através da tupla shape_filtro, que considera
## filtro quadrado.
def limiarizacao_local(imagem, shape_filtro, aplicar_threshold):
    # Copiamos a camada
    imagem_final = imagem.copy()

    # Verificamos se conseguimos dividir igualmente (tirando o pixel central de
    # aplicação)
    if ((shape_filtro[0] % 2 == 0) or (shape_filtro[1] % 2 == 0)):
        raise ValueError('O formato do filtro não é dividido igualmente nas'
        ' laterais')

    # Calculamos o padding (= índice inicial)
    pad_x = shape_filtro[0] // 2
    pad_y = shape_filtro[1] // 2
    # Calculamos o índice final
    max_x = imagem.shape[0] - pad_x
    max_y = imagem.shape[1] - pad_y

    # Para toda linha e coluna da imagem
    for y in range(pad_x, max_x):
        for x in range(pad_y, max_y):
            # Aplicamos a função dada de threshold
            imagem_final[y][x] = aplicar_threshold(imagem, y, x)

    # Tiramos o padding da imagem final
    imagem_final = imagem_final[pad_y:max_y, pad_x:max_x]

    # Retornamos a imagem final
    return imagem_final

