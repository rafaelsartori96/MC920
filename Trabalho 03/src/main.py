## Rafael Sartori M. Santos, 186154
##
## Programa para identificação e caracterização de objetos

import cv2
import argparse
import numpy as np
import skimage.measure as skm

if __name__ == '__main__':
    # Criamos um parser de argumentos do programa
    parser = argparse.ArgumentParser()

    # Adicionamos um argumento para determinar qual imagem utilizaremos
    parser.add_argument(
        'img_in',
        help="Imagem de entrada para determinação de propriedades dos objetos."
    )
    # argumento para saída de imagem em escala de cinza
    parser.add_argument(
        '--img_greyscale',
        help="Imagem de saída após processo de escala de cinza."
    )

    # Recebemos as entradas
    argumentos = vars(parser.parse_args())
    print('argumentos:', argumentos)

    # Abrimos a imagem e transformamos em escala de cinza
    imagem = cv2.imread(argumentos['img_in'], cv2.IMREAD_GRAYSCALE)
    # Salvamos a imagem em escala de cinza se requisitado
    if argumentos['img_greyscale'] is not None:
        cv2.imwrite(argumentos['img_greyscale'], imagem)

    # Contamos os objetos conexos
    labels, nlabels = skm.label(imagem, return_num=True)
    # Imprimimos o número de regiões
    print('Número de regiões:', nlabels)
