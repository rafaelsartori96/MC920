#!/bin/sh

# Configurações
CAMINHO_ENTRADA=imgs/
CAMINHO_SAIDA=imgs_png/

# Pegamos imagens
IMAGENS=$CAMINHO_ENTRADA*.pgm

# Criamos pasta de saída se não existe
mkdir -p $CAMINHO_SAIDA

for imagem in $IMAGENS; do
    # Removemos extensão
    ARQUIVO=${imagem%\.*}
    # Removemos caminho de entrada da variável
    ARQUIVO=${ARQUIVO//$CAMINHO_ENTRADA/}

    # Definimos o caminho inicial da imagem
    IMAGEM_IN=$imagem
    # Definimos o final
    IMAGEM_OUT=$CAMINHO_SAIDA$ARQUIVO.png

    echo "Transformando: $IMAGEM_IN -> $IMAGEM_OUT"
    # Convertemos
    convert $IMAGEM_IN $IMAGEM_OUT
done

echo "Pronto!"
