## Trabalho 2

Programa para rotulação e extração de informações quantitativas de objetos em imagens simples escrito por Rafael Sartori M. Santos, RA 186154 para disciplina de processamento de imagem (MC920) com H. Pedrini na Unicamp.


### Organização do programa

O programa Python fica na pasta `src/`, a função principal está em `main.py`, sem arquivos adicionais. O relatório é feito em LaTeX (texlive) na pasta `docs/`.


### Execução

Para executar o programa, veja:
```
$ python3 main.py --help
```

Podemos especificar o método de limiarização, devemos especificar a imagem de entrada e saída.

Para execução automática (em todas as imagens da pasta `imgs/`), execute:
```
$ bash aplicar_limiarizacao.sh
```

Para execução automática em paralelo, é necessário definir qualquer valor à _environment variable_ `MC920_PARALELO` e executar o _script_ da mesma forma.


### Relatório

Requer a [distribuição LaTeX texlive](https://tug.org/texlive/) e [`latexmk`](https://mg.readthedocs.io/latexmk.html).

Com todas as imagens prontas em `imgs/` nas posições esperadas, para compilar o relatório, é necessário executar:
```
$ cd docs/
$ latexmk
```
