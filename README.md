# MC920 -- Processamento digital de imagem

Repositório que utilizarei para a disciplina ministrada por H. Pedrini no segundo semestre de 2019 na Unicamp.

## Pré-requisitos

É necessário possuir `pipenv` para instalar o _virtual environment_ utilizado nos projetos, como [OpenCV](https://opencv.org/) (que, no nosso caso, será o [disponível em pip](https://pypi.org/project/opencv-python/)), [Jupyter Notebook](https://jupyter.org/) e [numpy](https://www.numpy.org/).

## Instalação e execução do ambiente

Utilizando o `pipenv`, na raiz do projeto, execute:
```
# Para instalar:
$ pipenv install

# Para executar:
$ pipenv shell

# E, no ambiente, abrimos o notebook:
(MC920) $ jupyter notebook
```

## Organização do projeto

Cada trabalho será um Notebook diferente no Jupyter, as imagens estarão dentro de cada trabalho, assim como a saída dos programas. Há algumas funções de utilidade que provavelmente utilizarei em mais de um trabalho, deixei no módulo Python `util` (na raiz do projeto).
