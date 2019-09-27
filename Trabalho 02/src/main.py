## Rafael Sartori M. Santos, 186154
##
## Programa para limiarização

# Configuração das divisões do histograma
DIVISOES_HISTOGRAMA = 128
# Título padrão do histograma
TITULO_PADRAO = 'Histograma da imagem'

import argparse
import matplotlib.pyplot as plt
import numpy as np
import util

from global_ import aplicar_global
from bernsen import aplicar_bernsen


def plot_histograma(histograma, divisoes, caminho, titulo=TITULO_PADRAO):
    # Fazemos o plot
    plt.hist(histograma, divisoes)
    # Definimos os títulos
    plt.title(titulo)
    plt.ylabel('Número de pixels')
    plt.xlabel('Intensidade de cinza')
    # Salvamos o histograma no arquivo dado
    plt.savefig(caminho)
    # Limpamos o plot
    plt.clf() # "clear figure"


if __name__ == '__main__':
    # Criamos um dicionário: chave = nome efeito, valor = função de efeito
    # A função de efeito recebe a caamda de entrada e deve retornar a camada
    # alterada
    opcoes_efeitos = {
        'global': aplicar_global,
        'bernsen': aplicar_bernsen,
    }

    # Criamos um parser de argumentos
    parser = argparse.ArgumentParser()

    # Adicionamos um argumento para determinar qual função utilizamos
    parser.add_argument(
        '-l', '--limiarizacao',
        help="Função de limiarização a ser aplicada.",
        choices=opcoes_efeitos.keys(),
        default=next(iter(opcoes_efeitos.keys())),
        required=False,
        nargs=1
    )

    # argumento para imprimirmos o histograma
    parser.add_argument(
        '-Ho', '--histograma-original',
        help="Se especificado, indica o caminho em que o histograma da imagem"
        " original será salvo. Format PNG.",
        metavar='caminho'
    )
    parser.add_argument(
        '-Hf', '--histograma-final',
        help="Se especificado, indica o caminho em que o histograma da imagem"
        " final será salvo. Format PNG.",
        metavar='caminho'
    )

    # argumento para imprimirmos proporção de preto
    parser.add_argument(
        '-p', '--proporcao-pretos',
        help="Imprime em um arquivo texto a proporção de preto da imagem.",
        metavar='caminho'
    )

    # e um argumento para a imagem de entrada e saída (obrigatórios)
    parser.add_argument(
        'img_in',
        help="Imagem de entrada para aplicação de limiarização. Formato PGM."
    )
    parser.add_argument(
        'img_out',
        help="Imagem de saída para aplicação de limiarização. Formato PGM."
    )

    # Aguardamos a entrada
    argumentos = vars(parser.parse_args())

    # Abrimos a imagem dada
    camadas = util.abrir_imagem(argumentos['img_in'])
    # Conferimos se a imagem é monocromática
    if not len(camadas) == 1:
        raise ValueError('A imagem de entrada não é monocromática!')
    # Isolamos a única camada
    camada = camadas[0]

    # Fazemos a limiarização de acordo com a função dada
    camada_final = (opcoes_efeitos[argumentos['limiarizacao']])(camada)

    # Conferimos se devemos imprimir histograma
    if argumentos['histograma_original'] is not None:
        # Fazemos o histograma da imagem inicial
        histograma, divisoes = np.histogram(
            camada, bins=DIVISOES_HISTOGRAMA, range=(0, 255)
        )
        # Imprimimos histograma
        plot_histograma(
            histograma, divisoes,
            argumentos['histograma_original'],
            'Histograma da imagem original'
        )

    # Conferimos se devemos imprimir a proporção de preto
    imprimir_proporcao = argumentos['proporcao_pretos'] is not None
    imprimir_histograma = argumentos['histograma_final'] is not None
    if (imprimir_proporcao or imprimir_histograma):
        # Fazemos "histograma" da imagem final
        brancos = camada_final[camada_final >= 128].size
        pretos = camada_final[camada_final < 128].size
        total = brancos + pretos

        # Imprimimos num texto a proporção de preto para branco
        if imprimir_proporcao:
            with open(argumentos['proporcao_pretos'], 'w') as arquivo:
                arquivo.write('{0}/{1}={2}\n'.format(
                    pretos, brancos, pretos / brancos
                ))

        # Imprimimos histograma se necessário
        if imprimir_histograma:
            # Imprimimos diagrama de barra
            plt.bar(
                x=[0, 255],
                height=[pretos * 100 / total, brancos * 100 / total],
                width=1
            )
            # Definimos os títulos
            plt.title('Histograma da imagem final')
            plt.ylabel('Número de pixels em porcentagem')
            plt.xlabel('Intensidade de cinza')
            # Alteramos o range vertical do plot
            axes = plt.gca() # "get current axis"
            axes.set_ylim([0, 100])
            # Adicionamos grid horizontal
            plt.grid(True, axis='y')
            # Salvamos o histograma no arquivo dado
            plt.savefig(argumentos['histograma_final'])
            # Limpamos o plot
            plt.clf() # "clear figure"

    # Salvamos a imagem na única camada
    util.salvar_imagem(argumentos['img_out'], [camada_final])
