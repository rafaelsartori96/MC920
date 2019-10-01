#!/bin/sh

# Configurações
CAMINHO_ENTRADA=imgs/
CAMINHO_SAIDA=imgs/
MAIN_PY=src/main.py

# Pegamos as imagens
IMAGENS=$CAMINHO_ENTRADA*.pgm

# Conferindo se executaremos em paralelo
if [[ -z "${MC920_PARALELO}" ]]; then
    echo "Execução não paralela. Para paralelizar, defina a environment variable MC920_PARALELO com qualquer valor."
else
    echo "Execução paralela."
fi

for imagem in $IMAGENS; do
    # Removemos extensão
    ARQUIVO=${imagem%\.*}
    # Removemos caminho de entrada da variável
    ARQUIVO=${ARQUIVO//$CAMINHO_ENTRADA/}

    # Definimos o caminho inicial da imagem
    IMAGEM_IN=$imagem
    # Definimos o nome final do histograma
    HISTOGRAMA_IN=$CAMINHO_SAIDA$ARQUIVO-histograma_in.png

    # Flag histograma_in
    HISTOGRAMA_IN_FLAG="--histograma-original $HISTOGRAMA_IN"

    for METODO in global bernsen niblack sauvola-pietikainen pms contraste media-local mediana-local media-global mediana-global; do
        # Para cada método, definimos o nome do arquivo
        IMAGEM_OUT=$CAMINHO_SAIDA$ARQUIVO-final-$METODO.pgm
        HISTOGRAMA_OUT=$CAMINHO_SAIDA$ARQUIVO-histograma_out-$METODO.png
        PROPORCOES_OUT=$CAMINHO_SAIDA$ARQUIVO-proporcoes-$METODO.txt

        echo "Produzindo $IMAGEM_OUT..."
        python3 $MAIN_PY \
            --limiarizacao $METODO \
            --histograma-final $HISTOGRAMA_OUT \
            --proporcao-preto $PROPORCOES_OUT \
            $IMAGEM_IN \
            $IMAGEM_OUT \
            $HISTOGRAMA_IN_FLAG &
        if [[ -z "${MC920_PARALELO}" ]]; then
            wait
        else
            sleep 2
        fi

        # Apagamos a flag do histograma
        HISTOGRAMA_IN_FLAG=""
    done
done

echo "Aguardando programas..."
wait
echo "Pronto!"
