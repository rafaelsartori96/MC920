## Rafael Sartori M. Santos, 186154
##
## Programa para identificação e caracterização de objetos

import os
import cv2
import argparse
import numpy as np
import skimage.measure as skm
import matplotlib.pyplot as plt


if __name__ == '__main__':
    # Criamos um parser de argumentos do programa
    parser = argparse.ArgumentParser()

    # Adicionamos um argumento para determinar qual imagem utilizaremos
    parser.add_argument(
        'img_in',
        help="Imagem de entrada para determinação de propriedades dos objetos. O nome do arquivo DEVE possuir extensão."
    )
    # argumento para saída de imagem em escala de cinza
    parser.add_argument(
        '-g', '--img-greyscale',
        metavar='caminho',
        help="Imagem de saída após processo de escala de cinza."
    )

    # argumento para imprimirmos as regiões separadamente
    parser.add_argument(
        '-pr','--print-regions',
        metavar='caminho',
        help="Imprime as imagens das regiões em uma pasta."
    )
    # argumento para imprimirmos histograma
    parser.add_argument(
        '-ph','--print-histogram',
        metavar='caminho',
        help="Salva do histograma dos tamanhos das regiões. Utiliza formatos do"
        " matplotlib (permite PDF, PNG etc)."
    )
    # argumento para imprimirmos as regiões separadamente
    parser.add_argument(
        '-pc','--print-contours',
        metavar='caminho',
        help="Imprime os contornos de cada região em uma pasta."
    )
    # argumento para imprimirmos os contornos
    parser.add_argument(
        '-c','--img-contour',
        metavar='caminho',
        help="Salva a imagem dos contornos de cada região."
    )

    # Recebemos as entradas
    argumentos = vars(parser.parse_args())

    # Pegamos o nome da imagem
    nome_imagem = (os.path.split(argumentos['img_in'])[1])[::-1].split('.')[::-1]
    nome_imagem.pop() # retiramos a extensão
    nome_imagem = '.'.join([nome[::-1] for nome in nome_imagem])

    # Abrimos a imagem e transformamos em escala de cinza
    imagem = cv2.imread(argumentos['img_in'], cv2.IMREAD_GRAYSCALE)
    # Salvamos a imagem em escala de cinza se requisitado
    if argumentos['img_greyscale'] is not None:
        cv2.imwrite(argumentos['img_greyscale'], imagem)

    # Contamos os objetos conexos
    labels, nlabels = skm.label(imagem, return_num=True)
    # Imprimimos o número de regiões
    print('Número de regiões:', nlabels)

    # Criamos imagem que contém todos os contornos
    img_contornos = np.zeros(imagem.shape)
    # Criamos uma categorização das diferentes imagens
    categorias = {
        'pequenas': (lambda x: x in range(0, 1500), []),
        'médias': (lambda x: x in range(1500, 3000), []),
        'grandes': (lambda x: x >= 3000, [])
    }

    # Pegamos as propriedades de cada rótulo
    for regiao, region_props in enumerate(skm.regionprops(labels), start=1):
        # Binarizamos a região atual
        region = np.where(labels == regiao, 1, 0)

        # Verificamos se temos que imprimir as regiões
        if argumentos['print_regions'] is not None:
            # Salvamos a imagem do contorno atual na pasta
            caminho = '{}/{}-region-{}.png'.format(
                argumentos['print_regions'],
                nome_imagem,
                regiao
            )
            cv2.imwrite(caminho, region * 255)

        # Imprimimos os dados
        print(
            'região {}:'.format(regiao),
            'área:', region_props.area,
            'centróide: ({c[0]:.2f}, {c[1]:.2f})'.format(c=region_props.centroid),
            'perímetro: {:.2f}'.format(skm.perimeter(region))
        )

        # Categorizamos a imagem
        for key, (condicao, lista) in categorias.items():
            # Se a região satisfaz a condição da categoria
            if condicao(region_props.area):
                # Adicionamos a região na categoria
                lista.append(regiao)

        # Mostramos contorno
        contornos = skm.find_contours(region, 0.5)
        img_contorno = np.zeros(region.shape)
        for contorno in contornos:
            for y, x in contorno:
                img_contorno[int(y)][int(x)] = 255

        # Colocamos o contorno atual no acumulador
        img_contornos = img_contornos + img_contorno

        # Verificamos se temos que imprimir contornos
        if argumentos['print_contours'] is not None:
            # Salvamos a imagem do contorno atual na pasta
            caminho = '{}/{}-region-{}-contornos.png'.format(
                argumentos['print_contours'],
                nome_imagem,
                regiao
            )
            cv2.imwrite(caminho, img_contorno)

    # Salvamos o contorno se necessário
    if argumentos['img_contour'] is not None:
        cv2.imwrite(argumentos['img_contour'], img_contornos)

    # Dados para histograma
    bar_x = []
    bar_height = []

    # Imprimimos a categorização
    print()
    for categoria, (condicao, lista) in categorias.items():
        print('número de regiões {}: {}'.format(categoria, len(lista)))
        # Adicionamos ao histograma
        bar_x.append(u'{}'.format(categoria))
        bar_height.append(len(lista))

    # Conferimos se é necessário salvar o histograma
    if argumentos['print_histogram'] is not None:
        # Salvamos o histograma através de uma barra no matplotlib
        # Fonte: https://stackoverflow.com/questions/30228069/how-to-display-the-value-of-the-bar-on-each-bar-with-pyplot-barh
        plot, axis = plt.subplots()
        indices = np.arange(len(bar_x))
        width = 0.75
        plt.barh(indices, bar_height, width)
        axis.set_yticks(indices)
        axis.set_yticklabels(bar_x, minor=False)
        plt.ylabel('Categoria')
        plt.xlabel('Número de objetos')
        plt.title('Histograma do tamanho dos objetos')
        plt.savefig(argumentos['print_histogram'])
