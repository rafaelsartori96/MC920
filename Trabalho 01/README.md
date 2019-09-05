## Trabalho 1

Objetivo é tratar algumas imagens quanto a meios-tons (_halftoning_) e analisar criticamente o resultado.

### Pré-requisitos

É necessário possuir instalado as bibliotecas [xtensor](https://quantstack.net/xtensor.html) para cálculos (biblioteca parecida com numpy), a biblioteca [FreeImage](http://freeimage.sourceforge.net/) para abrir e salvar imagens, utilizaremos o _wrapper_ `FreeImagePlus` para C++. Em Ubuntu, temos:
```
apt install --no-install-recommends xtensor-dev libfreeimageplus-dev
```

### Compilando

Com os pré-requisitos instalados, basta executar `make` para produzir o executável na pasta `out/`.

Para executar:
```
./out/main
```
