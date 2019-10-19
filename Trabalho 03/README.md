## Trabalho 3

Programa para rotulação e extração de informações quantitativas de objetos em imagens simples escrito por Rafael Sartori M. Santos, RA 186154 para disciplina de processamento de imagem (MC920) com H. Pedrini na Unicamp.


### Organização do programa

O programa Python fica na pasta `src/`, a função principal está em `main.py`, sem arquivos adicionais. O relatório é feito em LaTeX (texlive) na pasta `docs/`.


### Execução

Requer os programas enunciados em [`requirements.txt`](../requirements.txt).

Para executar o programa, veja:
```
$ python3 main.py --help
```

Podemos especificar vários parâmetros para extração adicional de informações, como histograma, contornos de regiões e regiões.


### Relatório

Requer a [distribuição LaTeX texlive](https://tug.org/texlive/) e [`latexmk`](https://mg.readthedocs.io/latexmk.html).

Com todas as imagens prontas em `imgs/` nas posições esperadas, para compilar o relatório, é necessário executar:
```
$ cd docs/
$ latexmk
```
