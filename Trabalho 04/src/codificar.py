## Rafael Sartori M. Santos, 186154
##
## python codificar.py imagem_entrada.png texto_entrada.txt plano_bits imagem_saida.png

import getpass # para pedir senha
import argparse # para recebermos as entradas facilmente

import numpy as np # para manipulações da imagem

from util import * # funções de utilidades do projeto


if __name__ == '__main__':
    # Criamos um parser de argumentos do programa
    parser = argparse.ArgumentParser()

    # Adicionamos um argumento para determinar qual imagem utilizaremos
    parser.add_argument(
        'imagem_entrada',
        help="Caminho da imagem de entrada para codificarmos a mensagem."
    )
    # argumento para texto a ser codificado
    parser.add_argument(
        'texto_entrada',
        type=open,
        help="Arquivo de texto que contém a mensagem a ser codificada."
    )
    # argumento para definir o plano de bits a serem utilizados
    parser.add_argument(
        'plano_bits',
        type=int,
        choices=range(0, 8),
        default=0,
        help="Valor de 0 a 7. Define o plano a ser utilizado para guardar a"
        " mensagem."
    )
    # Adicionamos um argumento para determinar qual imagem de saída
    parser.add_argument(
        'imagem_saida',
        help="Caminho para imagem de saída com a mensagem decodificada."
    )

    # argumento opcional para requisitar senha
    parser.add_argument(
        '-ap','--ask-passphrase',
        action='store_true',
        help='Se mencionado, pedirá pelo input a senha para algoritmo AES.'
    )
    # argumento opcional especificar a senha
    parser.add_argument(
        '-p','--passphrase',
        metavar='senha',
        help='Se mencionado, utilizará a senha fornecida para o algoritmo AES.'
    )

    # argumento opcional para imprimir o que fazemos
    parser.add_argument(
        '-v','--verbose',
        action='store_true',
        help='Se mencionado, informará o usuário do que o programa está'
        ' fazendo.'
    )


    ## Recebemos as entradas

    argumentos = vars(parser.parse_args())
    # caminho dos arquivos de imagem
    caminho_entrada = argumentos['imagem_entrada']
    caminho_saida = argumentos['imagem_saida']
    # plano a ser utilizado para a mensagem
    plano_bits = int(argumentos['plano_bits'])
    # texto a ser escondido
    texto_entrada = argumentos['texto_entrada'].read() # lemos o arquivo todo
    # se imprimiremos outputs
    verbose = argumentos['verbose']

    # Declaramos função para verbose
    if verbose:
        def verbose(*args, **kwargs):
            print(*args, **kwargs)
    else:
        def verbose(*args, **kwargs):
            pass

    verbose('argumentos:', argumentos)

    # Conferimos o formato de saída
    if not caminho_saida.endswith('.png'):
        # Adicionamos ".png"
        caminho_saida = caminho_saida + ".png"
        # Avisamos usuário
        print('O formato de saída parece não ser PNG. Adicionando extensão '
        '".png" no formato:', caminho_saida)


    ## Transformamos o texto de entrada a depender dos argumentos de passphrase

    # Conferimos se há passphrase fornecida
    passphrase = argumentos['passphrase'] # None caso não mencionado
    # Se não há passphrase e existe flag para pedir, pedimos
    if argumentos['ask_passphrase'] and passphrase is None:
        passphrase = getpass.getpass('Entre com a senha para a mensagem: ')

    # Transformamos a mensagem em bytes (com AES ou sem)
    if passphrase is not None:
        # Importamos nossas funções para codificação e decodificação AES
        import aes
        # Passamos o texto por AES (retorna bytes)
        texto_entrada = texto_entrada.encode('utf-8')
        texto_entrada = aes.aes_encrypt(texto_entrada, passphrase)
    else:
        # convertemos texto para vetor de bytes simplesmente
        texto_entrada = str.encode(texto_entrada, 'utf-8')
    # Calculamos seu tamanho
    tamanho_mensagem = len(texto_entrada)

    # Criamos um bytearray para armazenar a mensagem
    mensagem_bytes = bytearray()
    # Adicionamos a quantidade de bytes a serem lidos antes da mensagem
    mensagem_bytes.extend((tamanho_mensagem).to_bytes(4, 'big'))
    # Adicionamos a mensagem
    mensagem_bytes.extend(texto_entrada)
    tamanho_bytes = len(mensagem_bytes)


    ## Incluímos a mensagem na imagem

    # Abrimos as camadas da imagem
    entrada = abrir_imagem(caminho_entrada)

    # Calculamos espaço disponível
    # linhas x colunas x camadas de cores / 8 bits por byte
    # (dividimos por 8 pois podemos utilizar apenas um bit em cada ponto da
    # imagem)
    tamanho_disponivel = entrada.size / 8
    razao_espaco_utilizado = tamanho_bytes / tamanho_disponivel
    verbose(
        'tamanho da mensagem:', tamanho_mensagem,
        'espaço necessário:', tamanho_bytes,
        'espaço disponível:', tamanho_disponivel,
        'espaço utilizado: {:.3f}'.format(razao_espaco_utilizado)
    )
    # Avisamos usuário se espaço utilizado é muito grande
    if razao_espaco_utilizado > 1:
        print('Não há espaço suficiente para a mensagem. Tentamos mesmo assim.')

    verbose('Preparando máscara de bits para mistura com imagem')
    # Preparamos matrizes que serão utilizadas para incluir a mensagem na imagem
    mensagem = np.zeros(entrada.shape, dtype=int)
    mascara = np.zeros(entrada.shape, dtype=int)
    # Percorremos o texto de entrada para colocar na matriz mensagem
    # Observação: iteramos nas camadas primeiro, depois colunas e depois linhas
    with np.nditer(mensagem, op_flags=['writeonly']) as it_mensagem:
        with np.nditer(mascara, op_flags=['writeonly']) as it_mascara:
            # Pegamos a mensagem byte a byte
            indice = 0
            byte = mensagem_bytes[indice]
            bits = 7
            for msg in it_mensagem:
                # Preenchemos a mensagem com o bit correspondente
                msg[...] = (byte & (1 << bits)) >> bits
                # Preenchemos a máscara com 1
                msc = next(it_mascara)
                msc[...] = 1
                # Indicamos que já lemos um bit do byte
                bits -= 1
                # Se acabamos os bits desse byte, pegamos outro
                if bits < 0:
                    # Restauramos o contador de bits remanescentes
                    bits = 7
                    # Adicionamos um ao índice do byte que estamos
                    indice += 1
                    # Verificamos se acabamos a mensagem
                    if indice >= tamanho_bytes:
                        break
                    # Se não acabamos, pegamos a próxima
                    byte = mensagem_bytes[indice]
            # Conferimos se salvamos toda a mensagem
            if indice < tamanho_bytes:
                raise Exception(
                    'Não há espaço suficiente na memória para mensagem! Foi '
                    'possível inserir apenas {} bytes.'.format(indice)
                )

    # Agora temos a máscara com todos os bits afetados e a mensagem em uma
    # matriz binária. Basta colocarmos na imagem no plano correspondente.

    # Corrigimos a máscara para o plano de bit que desejamos
    mensagem = np.left_shift(mensagem, plano_bits)
    mascara = np.left_shift(mascara, plano_bits)
    # Invertemos a máscara para retirar os bits da imagem principal utilizando
    # um NOT
    mascara_not = np.invert(mascara)
    verbose('Máscaras prontas')

    # Zeramos os bits da imagem
    verbose('Preparando imagem')
    entrada = np.bitwise_and(entrada, mascara_not)
    verbose('Imagem pronta para receber mensagem')

    # Incluímos a mensagem na imagem com bits zerados
    verbose('Incluindo mensagem na imagem')
    saida = np.bitwise_or(entrada, mensagem)

    # Salvamos a imagem
    verbose('Mensagem na imagem, salvando imagem')
    salvar_imagem(caminho_saida, saida)
