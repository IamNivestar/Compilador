from xmlrpc.client import Boolean
from lexico import AnalisadorLexico
from typing import Match

class Token(object):
    def __init__(self, type, value, line):
        self.type = type
        self.str_type = tokenNames[type]
        self.lexema = value
        self.line = line

    def __str__(self):
   
        return 'Token({type}, {lexema})'.format(
            type= tokenNames[type],
            lexema=self.lexema
        )

    def __repr__(self):
        return self.__str__()

class SymbolTable(object):
    def __init__(self):
        self.symbolTable = {}

    def insertEntry(self, lexema, entry):
        self.symbolTable[lexema] = entry

    def getEntry(self, lexema):
        return self.symbolTable[lexema]

    def buscar(self, lexema): #funcao pra verificar se possui registro
        if(lexema in self.symbolTable):
            return True
        else:
            return False

class TableEntry(object):
    def __init__(self, lexema, tipo, num_linha, ref_valor):
        self.lexema = lexema
        self.tipo = tipo
        self.num_linha = num_linha
        self.ref_valor = ref_valor

    def setTipo(self, tipo):
        self.tipo = tipo

    def setRefValor(self, rv):
        self.ref_valor = rv

    def getRefvalor(self):
        return self.ref_valor

    def getLinha(self):
        return self.num_linha

    def getTipo(self):
        return self.tipo

#Tokens codigos linguagem P
EOF = -1
ID = 0
ATTR = 1
LBRACKET = 2
RBRACKET = 3
PLUS = 4
MINUS = 5
MULT = 6
DIV = 7
PROGRAM = 8
BEGIN = 9
END = 10
VAR = 11
INTEGER = 12
INTEGER_CONST = 13
BOOLEAN = 14
REAL = 15
REAL_CONST = 16
STRING = 17
STRING_LITERAL = 18
IF = 19
THEN = 20
WHILE = 21
DO = 22
READ = 23
PRINT = 24
COLON = 25
TRUE = 26
FALSE = 27
COMMA = 28
PCOMMA = 29
EQ = 30
NE = 31
LT = 32
LE = 33
GT = 34
GE = 35

#Dicionário mapeia os nomes dos tokens aos códigos dos tokens
tokenNames = {}
tokenNames[EOF] = 'EOF'
tokenNames[ID] = 'ID'
tokenNames[LBRACKET] = 'LBRACKET'
tokenNames[RBRACKET] = 'RBRACKET'
tokenNames[PLUS] = 'PLUS'
tokenNames[MINUS] = 'MINUS'
tokenNames[MULT] = 'MULT'
tokenNames[DIV] = 'DIV'
tokenNames[ATTR] = 'ATTR'
tokenNames[PROGRAM] = 'PROGRAM'
tokenNames[IF] = 'IF'
tokenNames[THEN] = 'THEN'
tokenNames[WHILE] = 'WHILE'
tokenNames[DO] = 'DO'
tokenNames[READ] = 'READ'
tokenNames[PRINT] = 'PRINT'
tokenNames[BEGIN] = 'BEGIN'
tokenNames[END] = 'END'
tokenNames[VAR] = 'VAR'
tokenNames[INTEGER] = 'INTEGER'
tokenNames[BOOLEAN] = 'BOOLEAN'
tokenNames[STRING] = 'STRING'
tokenNames[REAL] = 'REAL'
tokenNames[TRUE] = 'TRUE'
tokenNames[FALSE] = 'FALSE'
tokenNames[COMMA] = 'COMMA'
tokenNames[PCOMMA] = 'PCOMMA'
tokenNames[COLON] = 'COLON'
tokenNames[EQ] = 'EQ'
tokenNames[NE] = 'NE'
tokenNames[LT] = 'LT'
tokenNames[LE] = 'LE'
tokenNames[GT] = 'GT'
tokenNames[GE] = 'GE'
tokenNames[INTEGER_CONST] = 'INTEGER_CONST'
tokenNames[REAL_CONST] = 'REAL_CONST'
tokenNames[STRING_LITERAL] = 'STRING_LITERAL'

##

tabelaSimbolos = SymbolTable()
vetorTokensEntrada = [] #vetor de objetos do tipo Token
saida = [] #saida com os erros e tokens reconhecidos 

### leitura e construcao da entrada

def construcao_entrada(entrada): #leitura do codigo criado pelo lexico em uma entrada
    token_lido = entrada[0]
    lexema = entrada[1]
    n_linha = entrada[2]
    acrescentar_token(token_lido, lexema, n_linha)

def leitura(): #para ler entradas salvas que já passaram pelo lexico e foram formatadas por ele em uma lista de tokens
    global saida
    teste_numero = int(input("Digite qual o numero do caso de teste que deseja carregar: (1-8)Corretos, (9-15)Deve apresentar Erros:\n(por padrão são lidos na pasta testes_sintatico_semanticos/)\n->"))
    if teste_numero == 1: arquivo_e = "input/testes_sintatico_semantico/caso1.txt"
    elif teste_numero == 2: arquivo_e = "input/testes_sintatico_semantico/caso2.txt"
    elif teste_numero == 3: arquivo_e = "input/testes_sintatico_semantico/caso3.txt"
    elif teste_numero == 4: arquivo_e = "input/testes_sintatico_semantico/caso4.txt"
    elif teste_numero == 5: arquivo_e = "input/testes_sintatico_semantico/caso5.txt"
    elif teste_numero == 6: arquivo_e = "input/testes_sintatico_semantico/caso6.txt"
    elif teste_numero == 7: arquivo_e = "input/testes_sintatico_semantico/caso7.txt"
    elif teste_numero == 8: arquivo_e = "input/testes_sintatico_semantico/caso8.txt"
    elif teste_numero == 9: arquivo_e = "input/testes_sintatico_semantico/caso9_erro_semantico_declaracao_dupla.txt"
    elif teste_numero == 10: arquivo_e = "input/testes_sintatico_semantico/caso10_erro_semantico_var_altura_nao_declarada.txt"
    elif teste_numero == 11: arquivo_e = "input/testes_sintatico_semantico/caso11_erro_semantico_var_string_recebe_inteiro.txt"
    elif teste_numero == 12: arquivo_e = "input/testes_sintatico_semantico/caso12_erro_sintatico_sem_pontovirgula.txt"
    elif teste_numero == 13: arquivo_e = "input/testes_sintatico_semantico/caso13_erro_sintatico_sem_begin.txt"
    elif teste_numero == 14: arquivo_e = "input/testes_sintatico_semantico/caso14_erro_semantico_divisaoporzero.txt"
    elif teste_numero == 15: arquivo_e = "input/testes_sintatico_semantico/caso15_erro_semantico_compatibilidade_operadores.txt"
    else: exit()
    return arquivo_e

def acrescentar_token(token_lido, lexema, n_linha):
    global vetorTokensEntrada
    for id_token, my_token in tokenNames.items():
        if my_token == token_lido:
            vetorTokensEntrada.append(Token(id_token, lexema, str(n_linha)))

### funcoes de analise sintatica

def imprimeErro():
    global token, i, saida 
    saida.append('Erro sintático.' + token.str_type + ' não esperado na entrada. Linha ' + token.line)
    print('Erro sintático.' + token.str_type + ' não esperado na entrada. Linha ' + token.line)
    error_exit()

def error_exit():
    global saida
    with open('saida_compilador.txt', 'w') as f:
        for item in saida:
            f.write("%s\n" % item)
    exit()

import time
def match(tok):
    time.sleep(TIME/2)
    global token, i, vetorTokensEntrada, saida
    if(token.type == tok):
        saida.append( token.str_type + ' reconhecido na entrada.')
        print(token.str_type+ ' reconhecido na entrada.')
    else:
        imprimeErro()
    i = i + 1
    if (i < len(vetorTokensEntrada)):
        token = vetorTokensEntrada[i]
    print('\nToken atualizado para: ', token.str_type + '\n') ######################################## auxiliar a debugar


##funcoes analise semantica

def variavel_esta_declarada(token): 
    global tabelaSimbolos
    if(tabelaSimbolos.buscar(token.lexema)):
        return True
    else:
        saida.append('Erro semântico, variavel' + token.lexema + ' não declarada. Linha ' + token.line)
        print('Erro semântico, variavel não declarada. Linha ' + token.line)
        error_exit()
        
def declarar_function(): 
    #optei por salvar o main na tabela de simbolos embora n fosse necessario pois não havera multiplas funções
    global tabelaSimbolos, token
    if(token.type == ID):
        entrada = TableEntry(token.lexema, None, token.line, None)
        tabelaSimbolos.insertEntry(token.lexema, entry=entrada)
        entrada.setTipo('main')

def declarar_variavel(variaveis, tipo):
    global saida, token, tabelaSimbolos
    for var in  variaveis:
        if(tabelaSimbolos.buscar(var.lexema)):
            print('Erro semantico variavel redeclarada, variavel '+ var.lexema + ' ja foi declarada na linha: ' + var.line)
            saida.append('Erro semantico variavel redeclarada, variavel '+ var.lexema + ' ja foi declarada na linha: ' + var.line)
            error_exit()
        else:
            entrada = TableEntry(var.lexema, tipo, var.line, None)
            tabelaSimbolos.insertEntry(var.lexema, entry=entrada)
            print('Variavel '+ var.lexema + ' declarada com sucesso')
            saida.append('Variavel '+ var.lexema + ' declarada com sucesso')


def valor_compativel_variavel(variavel_tipo, tok):
    if(tok.type == TRUE or tok.type == FALSE):
        if(variavel_tipo == BOOLEAN):
            return True
    elif(tok.type == INTEGER_CONST):
        if(variavel_tipo == INTEGER or variavel_tipo == REAL):
            return True
    elif(tok.type == REAL_CONST):
        if(variavel_tipo == REAL or variavel_tipo == INTEGER):
            return True
    elif(tok.type == STRING_LITERAL):
        if(variavel_tipo == STRING):
            return True
    return False

def salvando_constante(variavel, valor): #constanste do tipo x = 3.5
    variavel_tipo = encontrar_tipo(variavel)
    if ( valor_compativel_variavel(variavel_tipo, valor) ):
        registrar_valor(variavel, valor.lexema)
    else:
        print('Erro semântico, a variavel '+ variavel.lexema + ' é do tipo ' + tokenNames[variavel_tipo] + ' e não do tipo ' + valor.str_type)
        saida.append('Erro semântico, a variavel '+ variavel.lexema + ' é do tipo ' + tokenNames[variavel_tipo] + ' e não do tipo '+  valor.str_type)
        error_exit()

def registrar_valor(tok, valor):
    global tabelaSimbolos, saida
    if(tok == None or valor == None):
        print('Erro interno no registro de valores, token ou valor nulos')
        error_exit()
    if(tabelaSimbolos.buscar(tok.lexema)):  
        entrada = tabelaSimbolos.getEntry(tok.lexema)
        entrada.setRefValor(valor)
        #print('Debug: Variavel '+ tok.lexema + ' registrou o valor ' + str(valor))  ############################################################
    else:
        print('Erro interno, variavel '+ tok.lexema + ' não encontrada ao registrar valor')
        saida.append('Erro interno, variavel '+ tok.lexema + ' não encontrada ao registrar valor')
        error_exit()

def to_boolean(valor):
    if(valor == "false"):
        return False
    elif(valor == "true"):
        return True
    else:
        print("erro interno conversão boolean valor: " + str(valor))
        error_exit()

def encontrar_valor(tok):
    global tabelaSimbolos, saida
    
    if(tok.type == ID): #é variavel ou constante?
        if(tabelaSimbolos.buscar(tok.lexema)): 
            entrada = tabelaSimbolos.getEntry(tok.lexema)
            valor = entrada.getRefvalor()
            if(valor == None):
                print('Erro semantico, a variavel '+ tok.lexema + ' é NULL,  linha: ' +  tok.line)
                saida.append('Erro semantico, a variavel '+ tok.lexema + ' é NULL,  linha: ' + tok.line)
                error_exit()
            else:
                return valor
        else: 
            print("Erro interno função encontrar valor para o token: " + tok.lexema + "inesperado, variavel não exitente!?")
            error_exit()
    else:
        return tok.lexema

def encontrar_tipo(tok):
    global tabelaSimbolos, saida
    tipo = None 
    if(tok.type == ID): #é variavel ou constante?
        if(tabelaSimbolos.buscar(tok.lexema)):
            entrada = tabelaSimbolos.getEntry(tok.lexema)
            if(entrada.getTipo() == INTEGER):
                tipo = INTEGER
            elif(entrada.getTipo() == REAL):
                tipo = REAL
            elif(entrada.getTipo() == STRING):
                tipo = STRING
            elif(entrada.getTipo() == BOOLEAN):
                tipo = BOOLEAN
            elif(entrada.getTipo() == None):
                print('Erro interno, a variavel '+ tok.lexema + ' nao possui tipo, linha ' + entrada.getLinha())
                saida.append('Erro interno, a variavel '+ tok.lexema + ' nao possui tipo, linha ' + entrada.getLinha())
                error_exit()
        else: 
            print('Erro semantico, a variavel '+ tok.lexema + ' nao foi declarada, linha ' + tok.line)
            saida.append('Erro semantico, a variavel '+ tok.lexema + ' nao foi declarada, linha ' + tok.line)
            error_exit()
    elif(tok.type == INTEGER_CONST):
        tipo = INTEGER
    elif(tok.type == REAL_CONST):
        tipo = REAL
    elif(tok.type == TRUE or tok.type == FALSE):
        tipo = BOOLEAN
    elif(tok.type == STRING_LITERAL):
        tipo = STRING 
    return tipo

def compatibilidade_ope(variavel, op1, op2, operacao, tipo1, tipo2, tipo3):
    global saida
    valor1 = encontrar_valor(op1)
    valor2 = encontrar_valor(op2)
    print("Debug: operacao entre: ",valor1, valor2) #####################################3
    if(tipo1 == INTEGER and tipo2 == INTEGER):
        if(tipo3 == INTEGER):
            if(operacao == PLUS):
                registrar_valor(variavel, int(valor1) + int(valor2))
            elif(operacao == MINUS):
                registrar_valor(variavel, int(valor1) - int(valor2))
            elif(operacao == DIV):
                registrar_valor(variavel, int(valor1) / int(valor2))
            elif(operacao == MULT):
                registrar_valor(variavel, int(valor1) * int(valor2))
            else:
                print('erro interno na compatibilidade de operadores com variavel destino do tipo inteiro!')
                error_exit()
            return variavel
        elif(tipo3 == REAL):
            if(operacao == PLUS):
                registrar_valor(variavel, float(int(valor1) + int(valor2)))
            elif(operacao == MINUS):
                registrar_valor(variavel, float(int(valor1) - int(valor2)))
            elif(operacao == DIV):
                registrar_valor(variavel, float(int(valor1) / int(valor2)))
            elif(operacao == MULT):
                registrar_valor(variavel, float(int(valor1) * int(valor2)))
            else:
                print('erro interno na compatibilidade de operadores com variavel destino do tipo real!')
                error_exit()
            return variavel
        else:
            print('Erro semantico, variável destino ' + variavel.lexema + ' possui tipo ' + tokenNames[tipo3] +' enquanto o esperado era Integer, linha ' + variavel.line)
            saida.append('Erro semantico, variável destino ' + variavel.lexema + ' possui tipo ' + tokenNames[tipo3] +' enquanto o esperado era Integer, linha ' + variavel.line)
            return None
    elif(tipo1 == REAL and tipo2 == REAL):
        if(tipo3 == REAL):
            if(operacao == PLUS):
                registrar_valor(variavel, float(valor1) + float(valor2))
            elif(operacao == MINUS):
                registrar_valor(variavel, float(valor1) - float(valor2))
            elif(operacao == DIV):
                registrar_valor(variavel, float(valor1) / float(valor2))
            elif(operacao == MULT):
                registrar_valor(variavel, float(valor1) * float(valor2))
            else:
                print('erro interno na compatibilidade de operadores com variavel destino do tipo real!')
                error_exit()   
            return variavel
        elif(tipo3 == INTEGER):
            if(operacao == PLUS):
                registrar_valor(variavel, int(float(valor1) + float(valor2)))
            elif(operacao == MINUS):
                registrar_valor(variavel, int(float(valor1) - float(valor2)))
            elif(operacao == DIV):
                registrar_valor(variavel, int(float(valor1) / float(valor2)))
            elif(operacao == MULT):
                registrar_valor(variavel, int(float(valor1) * float(valor2)))
            else:
                print('erro interno na compatibilidade de operadores com variavel destino do tipo inteiro!')
                error_exit()
            return variavel
        else:
            print('Erro semantico, variável destino ' + variavel.lexema + ' possui tipo ' + tokenNames[tipo3] + ' enquanto o esperado era Real, linha ' + variavel.line)
            saida.append('Erro semantico, variável destino ' + variavel.lexema + ' possui tipo ' + tokenNames[tipo3] + ' enquanto o esperado era Real, linha ' + variavel.line)
            error_exit()
    elif(tipo1 == INTEGER and tipo2 == REAL):
        if(tipo3 == REAL):
            if(operacao == PLUS):
                registrar_valor(variavel, float(int(valor1) * float(valor2)))
            elif(operacao == MINUS):
                registrar_valor(variavel, float(int(valor1) * float(valor2)))
            elif(operacao == DIV):
                registrar_valor(variavel, float(int(valor1) * float(valor2)))
            elif(operacao == MULT):
                registrar_valor(variavel, float(int(valor1) * float(valor2)))
            else:
                print('erro interno na compatibilidade de operadores com variavel destino do tipo real!')
                error_exit()
            return variavel
        elif(tipo3 == INTEGER):
            if(operacao == PLUS):
                registrar_valor(variavel, int(int(valor1) + float(valor2)))
            elif(operacao == MINUS):
                registrar_valor(variavel, int(int(valor1) - float(valor2)))
            elif(operacao == DIV):
                registrar_valor(variavel, int(int(valor1) / float(valor2)))
            elif(operacao == MULT):
                registrar_valor(variavel, int(int(valor1) * float(valor2)))
            else:
                print('erro interno na compatibilidade de operadores com variavel destino do tipo inteiro!')
                error_exit()
            return variavel
        else:
            print('Erro semantico, variável destino ' + variavel.lexema + ' possui tipo ' + tokenNames[tipo3] + ' enquanto o esperado era Real, linha ' + variavel.line)
            saida.append('Erro semantico, variável destino ' + variavel.lexema + ' possui tipo ' + tokenNames[tipo3] + ' enquanto o esperado era Real, linha ' + variavel.line)
            error_exit()
    elif(tipo1 == REAL and tipo2 == INTEGER):
        if(tipo3 == REAL):
            if(operacao == PLUS):
                registrar_valor(variavel, float(float(valor1) + int(valor2)))
            elif(operacao == MINUS):
                registrar_valor(variavel, float(float(valor1) - int(valor2)))
            elif(operacao == DIV):
                registrar_valor(variavel, float(float(valor1) / int(valor2)))
            elif(operacao == MULT):
                registrar_valor(variavel, float(float(valor1) * int(valor2)))
            else:
                print('erro interno na compatibilidade de operadores com variavel destino do tipo real!')
                error_exit()
            return variavel
        elif(tipo3 == INTEGER):
            if(operacao == PLUS):
                registrar_valor(variavel, int(float(valor1) + int(valor2)))
            elif(operacao == MINUS):
                registrar_valor(variavel, int(float(valor1) - int(valor2)))
            elif(operacao == DIV):
                registrar_valor(variavel, int(float(valor1) / int(valor2)))
            elif(operacao == MULT):
                registrar_valor(variavel, int(float(valor1) * int(valor2)))
            else:
                print('erro interno na compatibilidade de operadores com variavel destino do tipo inteiro!')
                error_exit()
            return variavel
        else:
            print('Erro semantico, variável destino ' + variavel.lexema + ' possui tipo ' + tokenNames[tipo3] + ' enquanto o esperado era Real, linha ' + variavel.line)
            saida.append('Erro semantico, variável destino ' + variavel.lexema + ' possui tipo ' + tokenNames[tipo3] + ' enquanto o esperado era Real, linha ' + variavel.line)
            error_exit()
    elif(tipo1 == BOOLEAN and tipo2 == BOOLEAN):
        if(tipo3 == BOOLEAN):

            if(operacao == PLUS):
                if( int(to_boolean(valor1) + to_boolean(valor2)) == 0):
                    registrar_valor(variavel, False)
                else:
                    registrar_valor(variavel, True)
            elif(operacao == MINUS):
                if( int(to_boolean(valor1) - to_boolean(valor2)) == 0):
                    registrar_valor(variavel, False)
                else:
                    registrar_valor(variavel, True)
            elif(operacao == DIV):
                if( int(to_boolean(valor1) / to_boolean(valor2)) == 0):
                    registrar_valor(variavel, False)
                else:
                    registrar_valor(variavel, True)
            elif(operacao == MULT):
                if( int(to_boolean(valor1) * to_boolean(valor2)) == 0):
                    registrar_valor(variavel, False)
                else:
                    registrar_valor(variavel, True)
            else:
                print('erro interno na compatibilidade de operadores com variavel destino do tipo booleano!')
                error_exit()
            return variavel
        elif(tipo3 == INTEGER):
            if(operacao == PLUS):
                registrar_valor(variavel, int(to_boolean(valor1) + to_boolean(valor2)))
            elif(operacao == MINUS):
                registrar_valor(variavel, int(to_boolean(valor1) + to_boolean(valor2)))
            elif(operacao == DIV):
                registrar_valor(variavel, int(to_boolean(valor1) + to_boolean(valor2)))
            elif(operacao == MULT):
                registrar_valor(variavel, int(to_boolean(valor1) + to_boolean(valor2)))
            else:
                print('erro interno na compatibilidade de operadores com variavel destino do tipo inteiro!')
                error_exit()
            return variavel
        else:
            print('Erro semantico, variável destino ' + variavel.lexema + ' possui tipo ' + tokenNames[tipo3] + ' enquanto o esperado era Boolean, linha ' + variavel.line)
            saida.append('Erro semantico, variável destino ' + variavel.lexema + ' possui tipo ' + tokenNames[tipo3] + ' enquanto o esperado era Boolean, linha ' + variavel.line)
            error_exit()
    elif(tipo1 == BOOLEAN and tipo2 == INTEGER):
        if(tipo3 == BOOLEAN):
            if(operacao == PLUS):
                if( int(to_boolean(valor1)) + int(valor2) == 0):
                    registrar_valor(variavel, False)
                else:
                    registrar_valor(variavel, True)
            elif(operacao == MINUS):
                if( int(to_boolean(valor1)) - int(valor2) == 0):
                    registrar_valor(variavel, False)
                else:
                    registrar_valor(variavel, True)
            elif(operacao == DIV):
                if( int(to_boolean(valor1)) / int(valor2) == 0):
                    registrar_valor(variavel, False)
                else:
                    registrar_valor(variavel, True)
            elif(operacao == MULT):
                if( int(to_boolean(valor1)) * int(valor2) == 0):
                    registrar_valor(variavel, False)
                else:
                    registrar_valor(variavel, True)
            else:
                print('erro interno na compatibilidade de operadores com variavel destino do tipo booleano!')
                error_exit()
            return variavel
        elif(tipo3 == INTEGER):
            if(operacao == PLUS):
                registrar_valor(variavel, int(to_boolean(valor1) + int(valor2)))
            elif(operacao == MINUS):
                registrar_valor(variavel, int(to_boolean(valor1) - int(valor2)))
            elif(operacao == DIV):
                registrar_valor(variavel, int(to_boolean(valor1) / int(valor2)))
            elif(operacao == MULT):
                registrar_valor(variavel, int(to_boolean(valor1) * int(valor2)))
            else:
                print('erro interno na compatibilidade de operadores com variavel destino do tipo inteiro!')
                error_exit()
            return variavel
        else:
            print('Erro semantico, variável destino ' + variavel.lexema + ' possui tipo ' + tokenNames[tipo3] + ' enquanto o esperado era Boolean, linha ' + variavel.line)
            saida.append('Erro semantico, variável destino ' + variavel.lexema + ' possui tipo ' + tokenNames[tipo3] + ' enquanto o esperado era Boolean, linha ' + variavel.line)
            error_exit()
    elif(tipo2 == BOOLEAN and tipo1 == INTEGER):
        if(tipo3 == BOOLEAN):
            if(operacao == PLUS):
                if(int(int(valor1) + to_boolean(valor2)) == 0):
                    registrar_valor(variavel, False)
                else:
                    registrar_valor(variavel, True)
            elif(operacao == MINUS):
                if( int(int(valor1) - to_boolean(valor2))== 0):
                    registrar_valor(variavel, False)
                else:
                    registrar_valor(variavel, True)
            elif(operacao == DIV):
                if( int(int(valor1) / to_boolean(valor2)) == 0):
                    registrar_valor(variavel, False)
                else:
                    registrar_valor(variavel, True)
            elif(operacao == MULT):
                if( int(int(valor1) * to_boolean(valor2)) == 0):
                    registrar_valor(variavel, False)
                else:
                    registrar_valor(variavel, True)
            else:
                print('erro interno na compatibilidade de operadores com variavel destino do tipo booleano!')
                error_exit()
            return variavel
        elif(tipo3 == INTEGER):
            if(operacao == PLUS):
                registrar_valor(variavel, int(int(valor1) + to_boolean(valor2)))  ##converter string to boolean
            elif(operacao == MINUS):
                registrar_valor(variavel, int(int(valor1) - to_boolean(valor2)))
            elif(operacao == DIV):
                registrar_valor(variavel, int(int(valor1) / to_boolean(valor2)))
            elif(operacao == MULT):
                registrar_valor(variavel, int(int(valor1) * to_boolean(valor2)))
            else:
                print('erro interno na compatibilidade de operadores com variavel destino do tipo inteiro!')
                error_exit()
            return variavel
        else:
            print('Erro semantico, variável destino ' + variavel.lexema + ' possui tipo ' + tokenNames[tipo3] + ' enquanto o esperado era Boolean, linha ' + variavel.line)
            saida.append('Erro semantico, variável destino ' + variavel.lexema + ' possui tipo ' + tokenNames[tipo3] + ' enquanto o esperado era Boolean, linha ' + variavel.line)
            error_exit()
    else: #caso tenha fugido de todos os casos
        print('Erro semantico, tipos incompativeis operador 1 ' + str(valor1) + ' possui tipo ' + tokenNames[tipo1] +
            ' e operador 2 ' + str(valor2) + ' possui tipo ' + tokenNames[tipo2] + ', linha ' + variavel.line)
        saida.append('Erro semantico, tipos incompativeis operador 1 ' + str(valor1) + ' possui tipo ' + tokenNames[tipo1] +
            ' e operador 2 ' + str(valor2) + ' possui tipo ' + tokenNames[tipo2] + ', linha ' + variavel.line)
        error_exit()

def operacao(variavel, op1, op2, operacao):
    global saida
    tipo1 = encontrar_tipo(op1)
    tipo2 = encontrar_tipo(op2)

    if(variavel.type == ID):
        tipo3 = encontrar_tipo(variavel)
    else:
        tipo3 = None

    if(tipo3 == None): #variavel destino não declarada
        print('Erro semantico, variavel destino ' + variavel.type + ' não foi declarada, linha ' + variavel.line)
        saida.append('Erro semantico, variavel destino ' + variavel.type + ' não foi declarada, linha ' + variavel.line)
        error_exit()

    if( (operacao != PLUS) and (tipo1 == STRING or tipo2 == STRING) ): # string só é permitida com string em operacao de soma
        print('Erro semantico, não é permitida a operacao ' + operacao + ' com String, linha ' + op1.line)
        saida.append('Erro semantico, não é permitida a operacao ' + operacao + ' com String, linha ' + op1.line)
        error_exit()

    if(operacao == PLUS):
        if(tipo1 == STRING and tipo2 == STRING):
            if(tipo3 == STRING):
                temp1 = str(encontrar_valor(op1))
                temp2 = str(encontrar_valor(op2))
                temp1 = temp1.replace("\"","")
                temp2 = temp2.replace("\"","")
                registrar_valor(variavel, "\"" + temp1 + temp2 + "\"")
                return variavel
            else:
                print('Erro semantico, variável destino ' + variavel.lexema + ' possui tipo ' + tokenNames[tipo3] + ' enquanto o esperado era String, linha ' + variavel.line)
                saida.append('Erro semantico, variável destino ' + variavel.lexema + ' possui tipo ' + tokenNames[tipo3] + ' enquanto o esperado era String, linha ' + variavel.line)
                error_exit()
        elif(tipo1 == STRING and tipo2 != STRING):
            print('Erro semantico, não é permitida a operacao ' + tokenNames[operacao] + ' com String, linha ' + op1.line)
            saida.append('Erro semantico, não é permitida a operacao ' + tokenNames[operacao]  + ' com String, linha ' + op1.line)
            error_exit()
        return compatibilidade_ope(variavel, op1, op2, PLUS, tipo1, tipo2, tipo3)
        
    elif(operacao == MINUS):
        return compatibilidade_ope(variavel, op1, op2, MINUS, tipo1, tipo2, tipo3)

    elif(operacao == MULT):
        return compatibilidade_ope(variavel, op1, op2, MULT, tipo1, tipo2, tipo3)
        
    elif(operacao == DIV):
        if( encontrar_valor(op2)== 'false' or int( encontrar_valor(op2)) == 0):
            print('Erro semantico, operação de divisão com divisor nulo não permitida, linha ' + variavel.line)
            saida.append('Erro semantico, operação de divisão com divisor nulo não permitida, linha ' + variavel.line)
            error_exit()
        return compatibilidade_ope(variavel, op1, op2, DIV, tipo1, tipo2, tipo3)

######################## Analisador Sintatico (com ações Semânticas) - Metodo descida recursiva ######################

def Program():
    print("Ativação de Program()")
    global token, saida
    if(token.type == PROGRAM):
        match(PROGRAM)
        declarar_function() #registrar ID main
        match(ID) 
        match(PCOMMA)
        Bloco()
        if(token.type == EOF):
            match(EOF)
            saida.append('Fim da análise.')
            print('Fim da análise.')
    else:
        imprimeErro()

def Bloco():
    print("Ativação de Bloco()")
    global token
    if(token.type == VAR or token.type == BEGIN):
        DeclaracaoSeq()
        match(BEGIN)
        ComandoSeq()
        match(END)
    else:
        imprimeErro()

def DeclaracaoSeq():
    print("Ativação de DeclaracaoSeq()")
    global token
    if(token.type == VAR):
        Declaracao()
        DeclaracaoSeq()
    else:
        return

def Declaracao():
    print("Ativação de Declaracao()")
    global token
    if(token.type == VAR): # declaracao de variaveis
        match(VAR)
        variaveis = []
        VarList(variaveis) #coletando lista de variaveis a ser declarada
        match(COLON)
        Type(variaveis) 
        match(PCOMMA)
    else:
        imprimeErro()

def Type(variaveis): # tipo da variavel
    print("Ativação de Type()")
    global token
    if(token.type == BOOLEAN): 
        declarar_variavel(variaveis, BOOLEAN)
        match(BOOLEAN)
    elif(token.type == INTEGER):
        declarar_variavel(variaveis, INTEGER)
        match(INTEGER)
    elif(token.type == REAL):
        declarar_variavel(variaveis, REAL)
        match(REAL)
    elif(token.type == STRING):
        declarar_variavel(variaveis, STRING)
        match(STRING)
    else:
        imprimeErro()

def VarList(variaveis):
    print("Ativação de VarList()")
    global token
    if(token.type == ID):
        variaveis.append(token)
        match(ID)
        VarList2(variaveis)
    else:
        imprimeErro()

def VarList2(variaveis):
    print("Ativação de VarList2()")
    global token
    if(token.type == COMMA):
        match(COMMA)
        variaveis.append(token)
        match(ID)
        VarList2(variaveis)
    else:
        return

def ComandoSeq():
    print("Ativação de ComandoSeq()")
    global token
    if(token.type == ID or token.type == IF or token.type == WHILE or token.type == PRINT or token.type == READ):
        Comando()
        ComandoSeq()
    else:
        return

def Comando():
    print("Ativação de Comando()")
    global token
    if(token.type == ID): #atribuicao de valores
        variavel = token
        match(ID)
        match(ATTR)
        Expr(variavel) 
        match(PCOMMA)
           
    elif(token.type == IF):
        match(IF)
        Expr(None)
        match(THEN)
        ComandoSeq()
        match(END)
    elif(token.type == WHILE):
        match(WHILE)
        Expr(None)
        match(DO)
        ComandoSeq()
        match(END)
    elif(token.type == PRINT):
        match(PRINT)
        Expr(None)
        match(PCOMMA)
    elif(token.type == READ):
        match(READ)
        match(ID)
        match(PCOMMA)
        return None
    else:
        imprimeErro()

def Expr(variavel):  #atribuicao
    print("Ativação de Expr()")
    global token
    if(token.type == ID or token.type == INTEGER_CONST or token.type == REAL_CONST or token.type == TRUE
     or token.type == FALSE or token.type == STRING_LITERAL or token.type == LBRACKET):
        Rel(variavel)
        ExprOpc(variavel)
    else:
        imprimeErro()

def ExprOpc(variavel):
    print("Ativação de ExprOpc()")
    global token
    if(token.type == EQ or token.type == NE):
        OpIgual()
        Rel(variavel)
        ExprOpc(variavel)

    else:
        return None #VAZIO 

def OpIgual():
    print("Ativação de OpIgual()")
    global token      
    if(token.type == EQ):
        match(EQ)
    elif(token.type == NE):
        match(NE)
    else:
        imprimeErro()

def Rel(variavel):
    print("Ativação de Rel()")
    global token
    if(token.type == ID or token.type == INTEGER_CONST or token.type == REAL_CONST or token.type == TRUE
     or token.type == FALSE or token.type == STRING_LITERAL or token.type == LBRACKET):
        valor = Adicao(variavel)
        RelOpc(variavel, valor)
    else:
        imprimeErro()

def RelOpc(variavel, valor):
    print("Ativação de RelOpc()")
    global token
    if(token.type == LT or token.type == LE or token.type == GT or token.type == GE):
        OpRel()
        if(valor and variavel):
            #print("debug: "variavel.lexema, valor.lexema) ################################################
            salvando_constante(variavel,valor)  #### salvando variavel valor
        valor = Adicao(variavel)
        RelOpc(valor, variavel)
    else:
        if(valor and variavel):
            #print("debug: ", variavel.lexema, valor.lexema) ##############################################################333
            salvando_constante(variavel,valor)   #### salvando variavel valor
        return #VAZIO 

def OpRel():
    print("Ativação de OpRel()")
    global token
    if(token.type == LT):
        match(LT)
    elif(token.type == LE):
        match(LE)
    elif(token.type == GT):
        match(GT)
    elif(token.type == GE):
        match(GE)
    else:
        imprimeErro()

def Adicao(variavel):
    print("Ativação de Adicao()")
    if(token.type == ID or token.type == INTEGER_CONST or token.type == REAL_CONST or token.type == TRUE
     or token.type == FALSE or token.type == STRING_LITERAL or token.type == LBRACKET):
        t1 = Termo(variavel)
        return AdicaoOpc(t1, variavel)
    else:
        imprimeErro()

def Termo(variavel): #primeiro op
    print("Ativação de Termo()")
    global token
    if(token.type == ID or token.type == INTEGER_CONST or token.type == REAL_CONST or token.type == TRUE
     or token.type == FALSE or token.type == STRING_LITERAL or token.type == LBRACKET):
        t2 = Fator()
        return TermoOpc(t2, variavel)
    else:
        imprimeErro()

def TermoOpc(op1, variavel): #mult or div
    print("Ativação de TermoOpc()")
    global token
    if(token.type == MULT or token.type == DIV):
        resultado = OpMult(op1, variavel)
        return TermoOpc(resultado, variavel)
    else:
        return op1 #vazio

def AdicaoOpc(op1, variavel): #plus or minus
    print("Ativação de AdicaoOpc()")
    global token
    if(token.type == PLUS or token.type == MINUS): 
        resultado2 = OpAdicao(op1, variavel)
        AdicaoOpc(resultado2, variavel)
    else:
        return op1#vazio

def OpAdicao(ope1, variavel):
    print("Ativação de OpAdicao()")
    global token
    if(token.type == PLUS):
        match(PLUS)
        ope2 = Termo(variavel)
        resultado = operacao(variavel, ope1, ope2, PLUS)
        return resultado
    elif(token.type == MINUS):
        match(MINUS)
        ope2 = Termo(variavel)
        resultado = operacao(variavel, ope1, ope2, MINUS)
        return resultado
    else:
        imprimeErro()

def OpMult(ope1, variavel):
    global token
    print("Ativação de OpMult()")
    if(token.type == MULT):
        match(MULT)
        ope2 = Fator()
        resultado = operacao(variavel, ope1, ope2, MULT)
        return resultado
    elif(token.type == DIV):
        match(DIV)
        ope2 = Fator()
        resultado = operacao(variavel, ope1, ope2, DIV)
        return resultado
    else:
        imprimeErro()

def Fator(): 
    print("Ativação de Fator()")
    global token, tabelaSimbolos
    if(token.type == ID):
        variavel_esta_declarada(token)
        valor = token
        match(ID)
        return valor
    elif(token.type == INTEGER_CONST):
        valor = token
        match(INTEGER_CONST)
        return valor
    elif(token.type == REAL_CONST):
        valor = token
        match(REAL_CONST)
        return valor
    elif(token.type == TRUE):
        valor = token
        match(TRUE)
        return valor
    elif(token.type == FALSE):
        valor = token
        match(FALSE)
        return valor
    elif(token.type == STRING_LITERAL):
        valor = token
        match(STRING_LITERAL)
        return valor
    elif(token.type == LBRACKET):
        match(LBRACKET)
        valor = Expr()
        match(RBRACKET)
        return valor
    else:
        imprimeErro()

#           ***************************** Main *********************************

TIME = 0 #tempo em segundo para delay das mensagens (basta colocar zero caso n queira nenhum)

if __name__ == '__main__':

    print("\n Compilador Linguagem P - desenvolvido por Amaury - Tempo de Delay das mensagens está configurado para " + str(TIME) + " segundo(s)\n")
    time.sleep(TIME)
    lexico = AnalisadorLexico()
    arquivo = leitura()
    lexico.sintatico_leitura(arquivo)
    print("\tIniciando a Análise Lexica para o caso de teste arquivo: "+ str(lexico.arquivo) + " ...\n")
    time.sleep(TIME)
    lexico.analisar()
    print("\tAnálise Lexica concluída:\n")
    lexico.salvando()
    time.sleep(TIME)
    saida.append("Saida do compilador para o caso de teste arquivo: "+ str(lexico.arquivo) + " :\n")
    time.sleep(TIME)
    entrada = lexico.tokens_lista
    for l in entrada:
        #print("Debug: Saida do Analisador Léxico, Tokens:\n") #######
        #print(l)
        construcao_entrada(l)  
    time.sleep(TIME/2)
    
    print("\n\tIniciando o Analisador Sintático - Método de Descida Recursiva (e Ações Semânticas)...\n")
    time.sleep(TIME)
    i = 0
    token = vetorTokensEntrada[i]

    Program() #inciando algoritmo...

    time.sleep(TIME)
    
    with open('output/saida_compilador.txt', 'w') as f:
        for item in saida:
            f.write("%s\n" % item)
    print("Arquivo saida_compilador.txt salvo")

    print("\nDebug: Tabela de Simbolos:")  ###############################################
    lidos = []
    for tok in vetorTokensEntrada:
        if(tok.type == ID and tok.lexema not in lidos):
            entrada = tabelaSimbolos.getEntry(tok.lexema)
            lidos.append(tok.lexema)
            print(tok.lexema + " valor:" + str(entrada.getRefvalor()) + " tipo: " + str(entrada.getTipo())  + " linha: " + str(entrada.getLinha()))

#fim