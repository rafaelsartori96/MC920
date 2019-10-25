# MC920 - Processamento digital de imagem

[Repositório](https://github.com/rafaelsartori96/MC920/) que utilizarei para a disciplina ministrada por H. Pedrini no segundo semestre de 2019 na Unicamp.

## Pré-requisitos

É necessário possuir `virtualenv` para instalar o _virtual environment_ utilizado nos projetos, como [OpenCV](https://opencv.org/) (que, no nosso caso, será o [disponível em pip](https://pypi.org/project/opencv-python/)), [Jupyter Notebook](https://jupyter.org/), [numpy](https://www.numpy.org/), [scikit-image](https://scikit-image.org/) e [PyCrypto](https://www.pycryptodome.org/) (em sua implementação atualizada, `pycryptodome`).

## Instalação e execução do ambiente

Utilizando `virtualenv` na raiz do projeto, execute:

```
# Para instalar o virtual environment:
$ virtualenv .venv

# Para entrar no environment:
$ source .venv/bin/activate

# Instalamos todas as dependências
(.venv) $ pip install -r requirements.txt

# E, no ambiente, podemos o notebook:
(.venv) $ jupyter notebook
# ou executar os scripts dos trabalhos:
(.venv) $ cd Trabalho\ 02/
(.venv) $ sh aplicar_limiarizacao.sh
# ou ainda executar os programas diretamente:
(.venv) $ python3 src/main.py
```

Veja o README de cada trabalho para entender a organização dos projetos individualmente.

## Organização do projeto

Cada trabalho será uma pasta diferente, as imagens estarão dentro de cada trabalho, assim como a saída dos programas. Ou seja, cada trabalho será praticamente autocontido.

Os slides e materiais em aulas (`Aulas/`) foram feitos pelo prof. Pedrini. Se houver qualquer problema em mantê-los aqui, as removerei assim que requisitado.
