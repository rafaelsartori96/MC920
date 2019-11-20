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
    # argumento opcional para utilizar o método SVD do numpy
    parser.add_argument(
        '-np-svd','--numpy-svd',
        action='store_true',
        help='Se mencionado, utilizará o método SVD de Numpy.'
    )
    # argumento opcional para
    parser.add_argument(
        '-r','--substituir-original',
        action='store_true',
        help='Se mencionado, substituirá a imagem original utilizando mesmo'
        'método do OpenCV.'
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

    # Links que utilizei para escrever algumas coisas (algumas delas já desfiz)
    # https://www2.imm.dtu.dk/pubdb/views/edoc_download.php/4000/pdf/imm4000
    # https://math.stackexchange.com/questions/733612/using-svd-in-pca-for-image-compression
    # http://danielnee.com/2015/04/computing-pca-with-svd/
    # https://towardsdatascience.com/pca-and-svd-explained-with-numpy-5d13b0d2a4d8
    # https://machinelearningmastery.com/singular-value-decomposition-for-machine-learning/
    # https://stackoverflow.com/questions/24913232/using-numpy-np-linalg-svd-for-singular-value-decomposition
    # web.mit.edu/be.400/www/SVD/Singular_Value_Decomposition.htm
    # http://www.scielo.br/pdf/eins/v10n2/pt_a04v10n2.pdf
    # https://arxiv.org/pdf/1404.1100.pdf
    # além dos slides de aula

    # Para toda camada da imagem, comprimimos utilizando PCA com dado k
    for i in range(0, img_in.shape[2]):
        # Isolamos a camada atual:
        # camada de dados, cada linha é um vetor de atributos
        verbose('Isolando camada', i)
        camada = img_in[:,:,i]

        # Conferimos o método que utilizaremos
        if argumentos['numpy_svd']:
            # Solução automática (utilizando SVD do Numpy)
            verbose('Produzindo matrizes de SVD')
            U, D, Vt = np.linalg.svd(camada)
            verbose('Refazendo a imagem com os k componentes')
            img_out[:,:, i] = U[:, :k] @ np.diag(D[:k]) @ Vt[:k, :]
            continue

        # Calculamos a média de cada coluna
        verbose('Preparando média das colunas')
        media_colunas = camada.mean(axis=0)

        # Removemos a média de cada linha da camada
        verbose('"Normalizando" em relação às médias')
        camada_norm = camada - media_colunas

        # Fazemos a matriz de covariância
        verbose('Fazendo a matriz de covariância')
        # usando função de numpy
        #covariancia = np.cov(camada_norm)
        # usando (X * X^{T})
        covariancia = np.dot(camada_norm, camada_norm.transpose())
        #covariancia = covariancia / camada.shape[0] # vi em algum site, mas
        # não faz diferença aparente e não está no slide

        # Fazemos autovalores e autovetores da matriz de covariância
        verbose('Calculando autovalores e autovetores da matriz de covariância')
        autovalores, autovetores = np.linalg.eig(covariancia)
        if np.iscomplex(autovetores).any():
            print('Imagem', caminho_entrada, 'possui autovetores complexos.')
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
    if argumentos['substituir_original']:
        verbose('Escrevendo a imagem original (usando mesma compressão PNG)')
        cv2.imwrite(caminho_entrada, img_in)


