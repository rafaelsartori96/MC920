#!/bin/sh

# Configurações
CAMINHO_ENTRADA=imgs_in/
CAMINHO_SAIDA=imgs_out/
MAIN_PY=src/main.py

# Pegamos as imagens
IMAGENS=$CAMINHO_ENTRADA*.png

# Conferindo se executaremos em paralelo
if [[ -z "${MC920_PARALELO}" ]]; then
    echo "Execução não paralela. Para paralelizar, defina a environment variable MC920_PARALELO com qualquer valor."
else
    echo "Execução paralela."
fi

for COMPONENTES in 32 64 128 192 256; do
    for imagem in $IMAGENS; do
        # Removemos extensão
        ARQUIVO=${imagem%\.*}
        # Removemos caminho de entrada da variável
        ARQUIVO=${ARQUIVO//$CAMINHO_ENTRADA/}

        # Definimos o caminho inicial da imagem
        IMAGEM_IN=$imagem

        # Com SVD
        IMAGEM_OUT=$CAMINHO_SAIDA$ARQUIVO-$COMPONENTES-svd.png
        RELATORIO_OUT=$CAMINHO_SAIDA$ARQUIVO-$COMPONENTES-svd-relatorio.txt

        echo "Produzindo $IMAGEM_OUT de $IMAGEM_IN..."
        python3 $MAIN_PY \
            $IMAGEM_IN \
            $COMPONENTES \
            $IMAGEM_OUT \
            -r $RELATORIO_OUT \
            -np-svd &
        if [[ -z "${MC920_PARALELO}" ]]; then
            wait
        fi

        # Sem SVD
        IMAGEM_OUT=$CAMINHO_SAIDA$ARQUIVO-$COMPONENTES.png
        RELATORIO_OUT=$CAMINHO_SAIDA$ARQUIVO-$COMPONENTES-relatorio.txt

        echo "Produzindo $IMAGEM_OUT de $IMAGEM_IN..."
        python3 $MAIN_PY \
            $IMAGEM_IN \
            $COMPONENTES \
            $IMAGEM_OUT \
            -r $RELATORIO_OUT &
        if [[ -z "${MC920_PARALELO}" ]]; then
            wait
        fi
    done
done

echo "Aguardando programas..."
wait
echo "Pronto!"
