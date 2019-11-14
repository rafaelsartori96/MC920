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
    # Parâmetro k
    parser.add_argument(
        'k',
        type=int,
        help="Parâmetro k para produzir a imagem comprimida."
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
    # parâmetro k
    k = int(argumentos['k'])
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

    # Abrimos a imagem utilizando int
    img_in = cv2.imread(caminho_entrada, cv2.IMREAD_UNCHANGED)
    img_in = img_in.astype(np.float64)
    # Criamos a imagem para saída
    img_out = np.zeros(img_in.shape, dtype=np.float64)

    # Para toda camada da imagem, comprimimos
    for i in range(0, img_in.shape[2]):
        # Isolamos a camada atual
        camada = img_in[:,:,i]

        # Aplicamos decomposição em valores singulares (SVD em inglês)
        verbose('Calculando SVD da camada', i)
        U, S, VH = np.linalg.svd(camada, full_matrices=False)
        verbose('SVD calculado.')

        # Seccionamos em k
        Ug = U[:,:k]
        Sg = S[:k]
        Vg = VH[:k,:]

        # Fazemos a imagem final
        verbose('Calculando camada', i, 'final')
        img_out[:,:,i] = (Ug * Sg) @ Vg
        verbose('Camada final pronta')

        # Imprimimos informações da imagem
        verbose('Formato das matrizes:')
        verbose('camada original', camada.shape)
        verbose('U', U.shape)
        verbose('S', S.shape)
        verbose('VH', VH.shape)
        verbose('camada final', img_out[:,:,i].shape)
        verbose()

    # Salvamos a imagem final
    cv2.imwrite(caminho_saida, img_out, [cv2.IMWRITE_PNG_COMPRESSION, 9])


