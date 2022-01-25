# Compilador
Trabalho da disciplina de Compiladores que consiste em desenvolver um compilador. 

Este trabalho foi realizado durante a disciplina de compiladores, o compilador foi desenvolvido para uma linguagem denominada "P" que é similar a linguagem pascal
porém simplificada. O objetivo é ligar a teoria com a prática. 

Devido a curto tempo no semestre o compilador apresentou alguns bugs na entrega final, no entando, durante as férias realizei a correção. Assim o compilador, construído 
a partir de uma gramática dada pelo professor (consultar arquivo documeancao.pdf neste repositório) realizar a análise léxica, sintática e algumas ações semânticas. 

Neste repositório também estão imagens de representação do AFD (automato finito determinístico) que criei a partir da gramática pedida e dos casos de teste, sendo:
  10 casos para testagem do analisador léxico (sendo 2 casos que devem apresentar erros propositais).
  14 casos de teste do analisador sintático e semântica (sendo 6 casos com erros pré-definidos).

É possível executar o analisador léxico separadamente (lexico.py) , ou executar o arquivo compilador_p.py que realiza todo o processo usando a classe do analisador léxico
e, a partir dele, realizar as ações semânticas e analises sintáticas. 
