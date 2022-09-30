# Diretrizes

Este arquivo tem o propósito de explicar a organização do projeto.

# Estrutura de Arquivos

O projeto é dividido em dois diretórios principais `src` e `docs`. `src` contém os arquivos de código-fonte, em Python, e `docs` contém este arquivo de diretrizes e uma pasta com um relatório em LaTeX Os arquivos do código fonte estão divididos em módulos. Em especial, o módulo `test` contém testes de unidade que podem ser executados usando a biblioteca *pytest*. Além disso, `src` possui um diretório especial `demo` que contém *notebooks* com demonstrações de alguns módulos.

# Práticas de Código

Na medida do possível, o projeto é fortemente tipado. No mais, valem as seguintes práticas:

- Nomes de módulos devem ser em *snake_case* 
- Nomes de classes devem ser em *PascalCase*
- Nomes de funções devem ser em *snake_case*
- Nomes de variáveis devem ser em *snake_case*
