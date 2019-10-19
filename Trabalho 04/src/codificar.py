## Rafael Sartori M. Santos, 186154
##
## python codificar.py imagem_entrada.png texto_entrada.txt plano_bits imagem_saida.png

import argparse


if __name__ == '__main__':
    # Criamos um parser de argumentos do programa
    parser = argparse.ArgumentParser()

    # Adicionamos um argumento para determinar qual imagem utilizaremos
    parser.add_argument(
        'imagem_entrada',
        help="Imagem de entrada para codificarmos a mensagem."
    )
    # argumento para texto a ser codificado
    parser.add_argument(
        'texto_entrada',
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
        help="Imagem de saída com a mensagem decodificada."
    )

    # argumento opcional para requisitar senha
    parser.add_argument(
        '-ap','--ask-passphrase',
        action='store_true',
        help='Se mencionado, irá pedir uma senha para proteger a mensagem.'
        ' Implica "--phassphrase".'
    )
    # argumento opcional especificar a senha
    parser.add_argument(
        '-p','--passphrase',
        metavar='senha',
        help="Se mencionado, protegerá a mensagem utilizando algoritmo AES."
    )

    # Recebemos as entradas
    argumentos = vars(parser.parse_args())
    print('argumentos:', argumentos)
