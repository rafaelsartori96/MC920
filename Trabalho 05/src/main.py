## Rafael Sartori M. Santos, 186154
##
## Compressão através de análise de principais componentes (PCA)

import cv2
import argparse
import numpy as np


if __name__ == '__main__':
    # Criamos um parser de argumentos do programa
    parser = argparse.ArgumentParser()

    # Adicionamos um argumento para determinar qual imagem utilizaremos
    parser.add_argument(
        'imagem_entrada',
        help="Caminho da imagem de entrada para comprimirmos."
    )
    # Adicionamos um argumento para determinar qual imagem produziremos
    parser.add_argument(
        'imagem_saida',
        help="Caminho da imagem produzida comprimida."
    )
    # argumento opcional para imprimir o que fazemos
    parser.add_argument(
        '-v','--verbose',
        action='store_true',
        help='Se mencionado, informará o usuário do que o programa está'
        ' fazendo.'
    )

    # Pegamos os argumentos da entrada
    argumentos = vars(parser.parse_args())
    # caminho dos arquivos de imagem
    caminho_entrada = argumentos['imagem_entrada']
    caminho_saida = argumentos['imagem_saida']
    # se imprimiremos outputs
    verbose = argumentos['verbose']

    # Declaramos função para verbose
    if verbose:
        def verbose(*args, **kwargs):
            print(*args, **kwargs)
    else:
        def verbose(*args, **kwargs):
            pass

    # Imprimimos as opções recebidas
    verbose('argumentos:', argumentos)

    # Conferimos o formato de saída
    if not caminho_saida.endswith('.png'):
        # Adicionamos ".png"
        caminho_saida = caminho_saida + ".png"
        # Avisamos usuário
        print('O formato de saída foi alterado para PNG:', caminho_saida)

    # Abrimos a imagem utilizando float
    img_in = cv2.imread(caminho_entrada, cv2.IMREAD_UNCHANGED)
    img_in = img_in.astype(np.float64)
    img_out = np.zeros(img_in.shape, dtype=np.float64)

