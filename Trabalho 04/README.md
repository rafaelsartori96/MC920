## Trabalho 4

Programa para codificar e decodificar mensagens nos bits menos significativos de imagens escrito por Rafael Sartori M. Santos, RA 186154 para disciplina de processamento de imagem (MC920) com H. Pedrini na Unicamp.


### Organização do programa

O programa Python fica na pasta `src/`, em `codificar.py` e `decodificar.py` que compartilham alguns arquivos auxiliares.

O relatório é feito em LaTeX (`texlive`) na pasta `docs/`.


### Execução

Requer os programas enunciados em [`requirements.txt`](../requirements.txt).

Para executar o programa, veja:
```
$ python3 codificar.py --help
$ python3 decodificar.py --help
```


### Relatório

Requer a [distribuição LaTeX texlive](https://tug.org/texlive/) e [`latexmk`](https://mg.readthedocs.io/latexmk.html).

Com todas as imagens prontas em `imgs/` nas posições esperadas, para compilar o relatório, é necessário executar:
```
$ cd docs/
$ latexmk
```
