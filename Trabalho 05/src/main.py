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
        # Isolamos a camada atual:
        # camada de dados, cada linha é um vetor de atributos
        verbose('Isolando camada', i)
        camada = img_in[:,:,i]

        # Calculamos a média de cada coluna
        verbose('Preparando média das colunas')
        media_colunas = camada.mean(axis=0)

        # Removemos a média de cada linha da camada
        verbose('"Normalizando" em relação às médias')
        camada_norm = camada - media_colunas

        # Fazemos a matriz de covariância
        verbose('Fazendo a matriz de covariância')
        covariancia = np.cov(camada_norm)

        # Fazemos autovalores e autovetores da matriz de covariância
        verbose('Calculando autovalores e autovetores da matriz de covariância')
        autovalores, autovetores = np.linalg.eig(covariancia)
        # Ordenamos decrescentemente autovalores e autovetores
        sort_indices = np.argsort(autovalores)[::-1]
        autovalores = autovalores[sort_indices]
        autovetores = autovetores[:,sort_indices]
        verbose('\tcamada.shape (nxd)', camada.shape)
        verbose('\tautovalores.shape (n)', autovalores.shape)
        verbose('\tautovetores.shape (nxn)', autovetores.shape)

        # Pegando os k primeiros valores da matriz de autovetores
        verbose('Isolando autovetores com k =', k)
        autovetores = autovetores[:,:k]
        verbose('\tautovetores.shape (nxd)', autovetores.shape)
        verbose('\tautovetores.transpose().shape (dxn)', autovetores.transpose().shape)

        # Calculamos a matriz X chapeu de saída
        verbose('Fazendo matriz de saída')
        camada_ = np.dot(autovetores.transpose(), camada_norm)
        verbose('\tx_chapeu.shape (nxk)', camada_.shape)
        img_out[:,:,i] = np.dot(autovetores, camada_) + media_colunas
        verbose('\timg_out[i].shape (nxd)', img_out[:,:,i].shape)

    # Salvamos a imagem final
    verbose('Escrevendo a imagem final', caminho_saida)
    cv2.imwrite(caminho_saida, img_out)
    verbose('Escrevendo a imagem original (usando mesma compressão PNG)')
    cv2.imwrite(caminho_entrada, img_in)


