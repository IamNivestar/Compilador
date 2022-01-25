
'''Analisador Lexico Linguagem P (Pascal Small)'''
from tabulate import tabulate
import re

from tokens_p import tokens

class AnalisadorLexico():
    buffer = [] # Buffer do lexema
    estado = 0 # Estado  do automato (inicia no estado 0)
    contador = 1
    tokens_lista = [] #lista que salva os tokens que serao identificados

    def leitura(self):
        teste_numero = int(input("Digite qual o numero do caso de teste que deseja carregar: (1-8)corretos ou (9-10) com erros\n (por padrão são lidos na pasta input/teste_lexico/)\n->"))
        if(teste_numero == 1): arquivo_e = "input/teste_lexico/code1.txt"
        elif teste_numero == 2: arquivo_e = "input/teste_lexico/code2.txt"
        elif teste_numero == 3: arquivo_e = "input/teste_lexico/code3.txt"
        elif teste_numero == 4: arquivo_e = "input/teste_lexico/code4.txt"
        elif teste_numero == 5: arquivo_e = "input/teste_lexico/code5.txt" 
        elif teste_numero == 6: arquivo_e = "input/teste_lexico/code6.txt"
        elif teste_numero == 7: arquivo_e = "input/teste_lexico/code7.txt"
        elif teste_numero == 8: arquivo_e = "input/teste_lexico/code8.txt"
        elif teste_numero == 9: arquivo_e = "input/teste_lexico/code1_witherrors.txt"
        elif teste_numero == 10: arquivo_e = "input/teste_lexico/code5_witherrors.txt"
        else: exit()
        print("\nSaida do compilador para o caso de teste arquivo: "+ str(arquivo_e) + " :\n")
        self.arquivo = arquivo_e    
        self.entrada = open(arquivo_e, "r") 

    def sintatico_leitura(self, arquivo_e):
        print("\nSaida do compilador para o caso de teste arquivo: "+ str(arquivo_e) + " :\n")
        self.arquivo = arquivo_e    
        self.entrada = open(arquivo_e, "r") 

    def estado_inicial(self, char):

        if char.isalpha():
            self.estado = 1
            self.buffer.append(char)
        elif char.isnumeric():
            self.estado = 2
            self.buffer.append(char)
        elif char == '<':
            self.estado = 5
            self.buffer.append(char)
        elif char == '>':
            self.estado = 6
            self.buffer.append(char)
        elif char == '=':
            self.estado = 13
            self.buffer.append(char)
        elif char == '!':
            self.estado = 15
            self.buffer.append(char)
        elif char == ':':
            self.estado = 16
            self.buffer.append(char)
        elif char == '\"':
            self.estado = 17
            self.buffer.append(char)
        elif char == ' ' or char == '\t':
            pass
        else:
            self.buffer.append(char)
            lexema = ''.join(self.buffer)
            self.tokens_lista.append([tokens[lexema], lexema, self.contador]) # Adiciona o token à lista de tokens identificados
            self.buffer = [] # Limpa o buffer

    #tipos unicos: ; + - / * , ( ) 
    #lembrando q existem as palavras reservadas

    def estado1(self, char): #possivelmente id ou palavra reservada
        if re.match('^[a-zA-Z0-9_]*$', char):
            self.buffer.append(char)
        else: 
            lexema = ''.join(self.buffer)
            self.num_char -= 1
            self.estado = 0 #voltei pro estado inicial
            self.tokens_lista.append([tokens[lexema] if lexema in tokens else "ID", lexema, self.contador]) 
            self.buffer = []

    def estado2(self, char): #numero real ou inteiro?
        if char.isnumeric(): #enquanto for numero continuarei nesse estado salvando os numeros
            self.buffer.append(char)
        elif char == '.': #passou pro estado de verificacao de real
            self.estado = 3
            self.buffer.append(char)
        else: #algo diferente de outro numero ou ponto? salvarei como inteiro e voltarei o char
            self.num_char -= 1
            self.estado = 0
            lexema = ''.join(self.buffer)
            self.tokens_lista.append(['INTEGER_CONST', lexema, self.contador]) 
            self.buffer = [] 
        
    def estado3(self, char): #verificar real
        if char.isnumeric(): #real
            self.estado = 4
            self.buffer.append(char)
        else:
            print(f'Erro léxico! Esperava um real, porém não há um valor numérico após o ponto na linha {self.contador}')
            exit()

    def estado4(self, char): #leitura de todos os numeros apos o ponto
        if char.isnumeric():
            self.buffer.append(char)
        else: #acabou o numero salvarei e retornarei um char
            self.num_char -= 1
            self.estado = 0
            lexema = ''.join(self.buffer)
            self.tokens_lista.append(['REAL_CONST', lexema, self.contador]) # Adiciona o token à lista de tokens identificados
            self.buffer = [] # Limpa o buffer

    def estado5e6(self, char): #LE ou LT? GE ou GT? a logico pros do== é a msm nesta implementacao
        if char == "=":    
            self.buffer.append(char)
            self.estado = 0
            lexema = ''.join(self.buffer)
            self.tokens_lista.append([tokens[lexema], lexema, self.contador]) 
            self.buffer = [] 
        else:
            self.num_char -= 1 #retorno a leitura pra n perder o char, po== nao é um LE nem um GE
            self.estado = 0
            lexema = ''.join(self.buffer)
            self.tokens_lista.append([tokens[lexema], lexema, self.contador]) 
            self.buffer = [] 

    def estado13(self, char): #verificar de EQ
        if (char == '='):
            self.estado = 0
            self.buffer.append(char)
            lexema = ''.join(self.buffer)
            self.tokens_lista.append([tokens[lexema], lexema, self.contador]) 
            self.buffer = [] 
        else:
            print(f'Erro léxico! O caractere = não é reconhecido, talvez tenha faltado acrescentar o \"=\" na linha {self.contador}')
            exit()

    def estado15(self, char): #verificar possivel NE
        if (char == '='):
            self.estado = 0
            self.buffer.append(char)
            lexema = ''.join(self.buffer)
            self.tokens_lista.append([tokens[lexema], lexema, self.contador]) 
            self.buffer = [] 
        else:
            print(f'Erro léxico! O caractere ! não é reconhecido, talvez tenha faltado acrescentar o \"=\" na linha {self.contador}')
            exit()
            
    def estado16(self, char): # ATTR ou collon (:)?
        if (char == '='):
            self.estado = 0
            self.buffer.append(char)
            lexema = ''.join(self.buffer)
            self.tokens_lista.append([tokens[lexema], lexema, self.contador]) 
            self.buffer = [] 
        else:
            self.num_char -= 1
            self.estado = 0
            lexema = ''.join(self.buffer)
            self.tokens_lista.append([tokens[lexema], lexema, self.contador]) 
            self.buffer = [] 

    def estado17(self, char):
        if (char == '"'):
            self.estado = 0
            self.buffer.append(char)
            lexema = ''.join(self.buffer)
            self.tokens_lista.append(['STRING_LITERAL', lexema, self.contador])  #se for encontrado palavra reservada ele registra com o o token, caso contrario ID
            self.buffer = [] 
        else:
            self.buffer.append(char)
    
    def analisar(self):
        
        for linha in self.entrada: # Percorrendolinhas
            self.num_char = 0
            linha = linha.rstrip('\n')

            while (self.num_char < len(linha)): # Percorrendo cada caractere da linha
                
                char = linha[self.num_char] #pegando caractere a ser analisado
                
                if self.estado == 0:
                    self.estado_inicial(char)
                elif self.estado == 1:  
                    self.estado1(char)
                elif self.estado == 2:  
                    self.estado2(char)
                elif self.estado == 3:  
                    self.estado3(char)
                elif self.estado == 4:  
                    self.estado4(char)
                elif self.estado == 5 or self.estado == 6:  
                    self.estado5e6(char)
                elif self.estado == 13:  
                    self.estado13(char)
                elif self.estado == 15:  
                    self.estado15(char)
                elif self.estado == 16:  
                    self.estado16(char)
                elif self.estado == 17:  
                    self.estado17(char)
            
                self.num_char += 1
            self.contador += 1

        #token fim do arquivo
        self.tokens_lista.append(['EOF', 'eof', 0])

    def salvando(self):
        self.entrada.close()
        # Escreve no arquivo de saida os tokens identificados na produção
        with open('output/saida_lexemas.txt', 'w') as f:
            f.write("\nSaida do compilador para o caso de teste arquivo: "+ self.arquivo + " :\n")
            f.write(tabulate(self.tokens_lista, headers=['Token', 'Lexema', 'Linha'])) #escrevendo tokens
        print("--------Resultados salvos----------")            

if __name__ == '__main__':
    #iniciando Analisador
    analisador_lexico = AnalisadorLexico()
    #Realizando analise
    analisador_lexico.leitura()
    analisador_lexico.analisar()
    analisador_lexico.salvando()
    print("--------Analise Lexica Finalizada----------")

