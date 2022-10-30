# Diretrizes

Este arquivo tem o propósito de explicar a organização do projeto.

# Estrutura de Arquivos

O projeto é dividido em quatro diretórios principais `src`, `docs`, `data` e `images`. `src` contém os arquivos de código-fonte, em Python, `docs` contém este arquivo de diretrizes e uma pasta com um relatório em LaTeX (com um subdiretório para imagens), `data` contém os *datasets* utilizados pelo grupo e `images` as imagens geradas pelo programa principal. Os arquivos do código fonte estão divididos em módulos. Em especial, o módulo `test` contém testes de unidade que podem ser executados usando a biblioteca *pytest*. O módulo `line_sweep` faz uso de uma biblioteca de terceiros (que implementa uma AVL), localizada em seu subdiretório `lib`.

# Práticas de Código

Na medida do possível, o projeto é fortemente tipado. No mais, valem as seguintes práticas:

- Nomes de módulos devem ser em *snake_case* 
- Nomes de classes devem ser em *PascalCase*
- Nomes de funções devem ser em *snake_case*
- Nomes de variáveis devem ser em *snake_case*
