## Trabalho 2

Programa para aplicação de efeitos de limiarização em imagens monocromáticas escrito por Rafael Sartori M. Santos, RA 186154 para disciplina de processamento de imagem (MC920) com H. Pedrini na Unicamp.


### Organização do programa

O programa Python fica na pasta `src/`, a função principal está em `main.py`, há funções auxiliares à todos os métodos em `util.py` e cada método de limiarização fica em um arquivo de mesmo nome, por exemplo, o método de Bernsen, `bernsen.py`.

O relatório é feito em LaTeX (texlive) na pasta `docs/`. Para compilar corretamente, será necessário converter as imagens para PNG utilizando o _script_ `converter_pgm.sh`.


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

Com todas as imagens prontas em `imgs/`, para compilar o relatório, é necessário utilizar o _script_ e executar:
```
$ bash converter_pgm.sh
$ cd docs/
$ latexmk
```
