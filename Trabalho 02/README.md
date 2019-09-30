## Trabalho 2

Programa para aplicação de efeitos de limiarização em imagens monocromáticas escrito por Rafael Sartori M. Santos, RA 186154 para disciplina de processamento de imagem (MC920) com H. Pedrini na Unicamp.


### Organização do programa

O programa Python fica na pasta `src/`, a função principal está em `main.py`, há funções auxiliares à todos os métodos em `util.py` e cada método de limiarização fica em um arquivo de mesmo nome, por exemplo, o método de Bernsen, `bernsen.py`.


### Execução

Para executar o programa, veja:
```
$ python3 main.py --help
```

Podemos especificar o método de limiarização, devemos especificar a imagem de entrada e saída.

Para execução automática (em todas as imagens da pasta `imgs/`), execute:
```
$ sh aplicar_limiarizacao.sh
```

Para execução automática em paralelo, é necessário definir qualquer valor à _environment variable_ `MC920_PARALELO` e executar o script da mesma forma.
