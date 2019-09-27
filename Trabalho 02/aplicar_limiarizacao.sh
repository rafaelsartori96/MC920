#!/bin/sh

#
CAMINHO_ENTRADA=imgs/
CAMINHO_SAIDA=imgs_out/

# Pegamos as imagens
IMAGENS=$CAMINHO_ENTRADA*.pgm

for imagem in $IMAGENS; do
    # Definimos o nome inicial
    ARQUIVO_IN=$imagem

    # Removemos extensão
    ARQUIVO=${imagem%\.*}
    # Removemos caminho de entrada da variável
    ARQUIVO=${ARQUIVO//$CAMINHO_ENTRADA/}

    # Definimos o nome final
    ARQUIVO_OUT=$CAMINHO_SAIDA$ARQUIVO

    #
done
