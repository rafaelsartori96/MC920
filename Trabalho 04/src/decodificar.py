## Rafael Sartori M. Santos, 186154
##
## python decodificar.py imagem_saida.png plano_bits texto_saida.txt

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
        help="Caminho da imagem de entrada para decodificarmos a mensagem."
    )
    # argumento para definir o plano de bits a serem utilizados
    parser.add_argument(
        'plano_bits',
        type=int,
        choices=range(0, 8),
        default=0,
        help="Valor de 0 a 7. Define o plano que foi utilizado para guardar a"
        " mensagem."
    )
    # argumento para texto a ser codificado
    parser.add_argument(
        'texto_saida',
        help="Caminho para arquivo de texto que conterá a mensagem codificada."
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
    # caminho do arquivo de entrada
    caminho_entrada = argumentos['imagem_entrada']
    # caminho do texto de saída
    texto_saida = argumentos['texto_saida']
    # plano a ser utilizado para a mensagem
    plano_bits = int(argumentos['plano_bits'])
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

    # Conferimos o formato de entrada
    if not caminho_entrada.endswith('.png'):
        # Avisamos o usuário
        print('O formato de entrada não parece ser PNG. A mensagem pode ter'
        'sido corrompida se o formato for lossy.')

    # Conferimos se há passphrase fornecida
    passphrase = argumentos['passphrase'] # None caso não mencionado
    # Se não há passphrase e existe flag para pedir, pedimos
    if argumentos['ask_passphrase'] and passphrase is None:
        passphrase = getpass.getpass('Entre com a senha para a mensagem: ')


    ## Retiramos a mensagem da imagem
    verbose('Iniciando isolamento da mensagem...')

    # Abrimos as camadas da imagem
    entrada = abrir_imagem(caminho_entrada)

    # Isolamos todo plano em um vetor de bytes
    plano_bytes = bytearray()

    # Fazemos uma máscara 1 em todo o plano
    mascara = np.left_shift(np.ones(entrada.shape, dtype=int), plano_bits)
    # Fazemos um AND com a entrada (zeramos todo o resto, mantemos o plano) e
    # deslocamos para a direita (tornando 1 ou 0)
    plano = np.right_shift(np.bitwise_and(entrada, mascara), plano_bits)

    # Agora isolamos o plano em bytes
    with np.nditer(plano, op_flags=['readonly']) as it_mensagem:
        # Pegamos a mensagem bit a bit
        indice = 0
        byte = 0
        bits = 0
        # Consideramos o limite o máximo possível enquanto não sabemos
        tamanho_mensagem = entrada.size / 8
        for bit in it_mensagem:
            # Colocamos esse bit no byte
            byte = byte << 1
            byte = byte | bit
            bits += 1

            # Verificamos se completamos o byte
            if bits >= 8:
                # Inserimos no vetor
                plano_bytes.extend(int(byte).to_bytes(1, 'big'))
                # Zeramos os acumuladores e contadores
                byte = 0
                bits = 0
                indice += 1

                # Verificamos se conseguimos determinar o tamanho
                if indice == 4:
                    tamanho_mensagem = int.from_bytes(plano_bytes[0:4], 'big')
                    verbose(
                        'Determinamos tamanho da mensagem em bytes:',
                        tamanho_mensagem
                    )

                # Verificamos se completamos todos os bytes
                if (indice - 4) >= tamanho_mensagem:
                    break

    verbose('Bytes da mensagem isolados, decifrando')
    # Removemos o inteiro (tamanho da mensagem) do array
    plano_bytes = plano_bytes[4:]

    # Agora com o plano de bytes completo, verificamos se é necessário AES
    if passphrase is not None:
        # Importamos nossas funções para codificação e decodificação AES
        import aes
        # Passamos o texto por AES (retorna bytes)
        plano_bytes = aes.aes_decrypt(plano_bytes, passphrase)
    # convertemos texto para vetor de bytes simplesmente
    mensagem = plano_bytes.decode('utf-8')

    # Escrevemos a mensagem em arquivo
    verbose('Escrevendo em arquivo', texto_saida)
    with open(texto_saida, 'w') as arquivo:
        arquivo.write(mensagem)
