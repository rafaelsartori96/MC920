## Rafael Sartori M. Santos, 186154
##
## python codificar.py imagem_entrada.png texto_entrada.txt plano_bits imagem_saida.png

import getpass # para pedir senha
import argparse # para recebermos as entradas facilmente

import numpy as np

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
        help="Arquivo de texto que condém a mensagem a ser codificada."
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

    ## Recebemos as entradas

    argumentos = vars(parser.parse_args())
    print('argumentos:', argumentos)
    # caminho dos arquivos de imagem
    caminho_entrada = argumentos['imagem_entrada']
    caminho_saida = argumentos['imagem_saida']
    # plano a ser utilizado para a mensagem
    plano_bits = argumentos['plano_bits']
    # texto a ser escondido
    texto_entrada = argumentos['texto_entrada'].read() # lemos o arquivo todo

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
        texto_entrada = aes.aes_encrypt(texto_entrada, passphrase)
    else:
        # convertemos texto para vetor de bytes simplesmente
        texto_entrada = str.encode(texto_entrada)
    # Calculamos seu tamanho
    tamanho_mensagem = len(texto_entrada)

    # Criamos um bytearray para armazenar a mensagem
    mensagem_bytes = bytearray()
    # Adicionamos a quantidade de bytes a serem lidos antes da mensagem
    mensagem_bytes.extend((tamanho_mensagem).to_bytes(4, 'big'))
    # Adicionamos a mensagem
    mensagem_bytes.extend(texto_entrada)
    tamanho_bytes = len(mensagem_bytes)
    print('tamanho =', tamanho_mensagem, 'tamanho array =', tamanho_bytes)

    ## Incluímos a mensagem na imagem

    # Abrimos as camadas da imagem
    entrada = abrir_imagem(caminho_entrada)

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
            bits = 8
            for msg in it_mensagem:
                # Preenchemos a mensagem com o bit correspondente
                msg[...] = (byte & 1)
                # Preenchemos a máscara com 1
                msc = next(it_mascara)
                msc[...] = 1
                # Fazemos o shift do byte para trazer o mais significativo
                byte = byte >> 1
                # Indicamos que já lemos um bit do byte
                bits -= 1
                # Se acabamos os bits desse byte, pegamos outro
                if bits == 0:
                    # Restauramos o contador de bits remanescentes
                    bits = 8
                    # Adicionamos um ao índice do byte que estamos
                    indice += 1
                    # Verificamos se acabamos a mensagem
                    if indice >= tamanho_bytes:
                        break
                    # Se não acabamos, pegamos a próxima
                    byte = mensagem_bytes[indice]

    # Agora temos a máscara com todos os bits afetados e a mensagem em uma
    # matriz binária. Basta colocarmos na imagem no plano correspondente.

    # Corrigimos a máscara para o plano de bit que desejamos
    mascara = np.left_shift(mascara, int(plano_bits))
    # Invertemos a máscara para retirar os bits da imagem principal utilizando
    # um NOT
    mascara_not = np.invert(mascara)
