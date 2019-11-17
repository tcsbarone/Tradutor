import re
from pprint import pprint

plv_reservadas = ['auto','scanf','main','break','case','char','const','continue','default','do','double','else','enum','extern','float','for','goto','if','int','long','register','return','short','signed','sizeof','static','struct','switch','typedef','union','unsigned','void','volatile','while','print','printf']
simbolos_especiais = ['.',';',',','(',')',':','+','-','*','%','=','"','{','}','[',']','#']
simbolos_compostos = ['<','>','<=','>=','==','!=','&&','||']
numeros = ['0','1','2','3','4','5','6','7','8','9','0']

def separaToken():
    linha = 0
    token = []
    atribuir = ''

    #ler arquivo TXT
    with open("teste PO.txt") as file:
        var = file.readlines()
        for line in var:
            line = line.replace("\t","")
            line = line.replace("\n","")
            if (len(line) > 0):
                linha += 1

                palavras = line.split()

                for plv in palavras:
                    if (re.search('\\#include', str(plv))):
                        include = plv

                for plv in palavras:
                    if(plv in plv_reservadas):
                        #Palavra Reservada
                        token.append(plv)

                    if (re.search('\\&', str(plv))):
                        if(plv != '&&'):
                            atribuir = plv
                            b = re.sub('&','',plv)
                            token.append(b)
                                    
                    if((plv not in plv_reservadas) and
                     (plv not in simbolos_especiais) and
                     (plv not in simbolos_compostos) and
                     (plv not in numeros) and
                     (plv != '%d') and
                     (plv != include) and
                     (plv != atribuir)):
                        #Variável
                        token.append(plv)

                    if(plv in numeros):
                        token.append(plv)
                
                    elif(plv in simbolos_especiais):
                        #Símbolos Especiais
                        token.append(plv)

                    elif(plv in simbolos_compostos):
                        token.append(plv)

                    elif(plv in simbolos_compostos):
                        #Simbolos Compostos
                        token.append(plv)
            
    return (token)


def main():
    a = 1
    nt = 0
    tradutor = []
    tok = separaToken()
    quantidade_variavel = 0
    variavel = []
    chave = []

    for index, i in enumerate(tok):
        if(tok[index] == '{'):
            chave.append('L' +str(a))
            tradutor.append(chave[-1])
            a = a + 1
        elif(tok[index] == '}'):
            if(len(chave) > 0):
                tradutor.append(chave[-1])
                chave.pop()
        
        if(i == 'main'):
            tradutor.append('INPP')
            
        elif(i == 'int' or i == 'float' or i == 'double' or i == 'char'):
            index = index + 1
            while(tok[index] != ';'):
                if(tok[index] != ','):
                    quantidade_variavel = quantidade_variavel + 1
                    variavel.append(tok[index])
                index = index + 1
            tradutor.append("AMEM "+ str(quantidade_variavel))
        elif(tok[index] == 'scanf'):
            tradutor.append('LEIT')
            tradutor.append('ARMZ ' +tok[index + 5])

        elif(tok[index] == 'while'):
            if(tok[index+2] in numeros):
                tradutor.append('CRCT ' +tok[index + 2])
            else:
                tradutor.append('CRVL ' +tok[index + 2])

            if(tok[index+4] in numeros):
                tradutor.append('CRCT ' +tok[index + 4])
            else:
                tradutor.append('CRVL ' +tok[index + 4])

            if(tok[index+3] in simbolos_compostos):
                if(tok[index+3] == '<='):
                    tradutor.append('CMEG')
                elif(tok[index+3] == '>='):
                    tradutor.append('CMAG')
                elif(tok[index+3] == '<'):
                    tradutor.append('CMME')
                elif(tok[index+3] == '>'):
                    tradutor.append('CMMA')
                elif(tok[index+3] == '=='):
                    tradutor.append('CMIG')
                elif(tok[index+3] == '!='):
                    tradutor.append('CMDG')
                elif(tok[index+3] == '&&'):
                    tradutor.append('CONJ')
                elif(tok[index+3] == '||'):
                    tradutor.append('DISJ')

        elif(tok[index] == 'if'):
            if(tok[index+2] in numeros):
                tradutor.append('CRCT ' +tok[index + 2])
            else:
                tradutor.append('CRVL ' +tok[index + 2])

            if(tok[index+4] in numeros):
                tradutor.append('CRCT ' +tok[index + 4])
            else:
                tradutor.append('CRVL ' +tok[index + 4])

            if(tok[index+3] in simbolos_compostos):
                if(tok[index+3] == '<='):
                    tradutor.append('CMEG')
                elif(tok[index+3] == '>='):
                    tradutor.append('CMAG')
                elif(tok[index+3] == '<'):
                    tradutor.append('CMME')
                elif(tok[index+3] == '>'):
                    tradutor.append('CMMA')
                elif(tok[index+3] == '=='):
                    tradutor.append('CMIG')
                elif(tok[index+3] == '!='):
                    tradutor.append('CMDG')
                elif(tok[index+3] == '&&'):
                    tradutor.append('CONJ')
                elif(tok[index+3] == '||'):
                    tradutor.append('DISJ')
            
        elif(tok[index] == '='):
            if(tok[index+1] in numeros):
                tradutor.append('CRCT ' +tok[index + 1])
            else:
                tradutor.append('CRVL ' +tok[index + 1])
                
            if(tok[index + 2] == ';'):
                tradutor.append('ARMZ ' +tok[index - 1])
            elif(tok[index+3] in numeros):
                tradutor.append('CRCT ' +tok[index + 3])
                if(tok[index+2] == '+'):
                    tradutor.append('SOMA')
                    tradutor.append('ARMZ '+tok[index-1])
                elif(tok[index+2] == '-'):
                    tradutor.append('SUBT')
                    tradutor.append('ARMZ '+tok[index-1])
                elif(tok[index+2] == '/'):
                    tradutor.append('DIVI')
                    tradutor.append('ARMZ '+tok[index-1])
                elif(tok[index+2] == '*'):
                    tradutor.append('MULT')
                    tradutor.append('ARMZ '+tok[index-1])
            else:
                tradutor.append('CRVL ' +tok[index + 3])
                if(tok[index+2] == '+'):
                    tradutor.append('SOMA')
                    tradutor.append('ARMZ '+tok[index-1])
                elif(tok[index+2] == '-'):
                    tradutor.append('SUBT')
                    tradutor.append('ARMZ '+tok[index-1])
                elif(tok[index+2] == '/'):
                    tradutor.append('DIVI')
                    tradutor.append('ARMZ '+tok[index-1])
                elif(tok[index+2] == '*'):
                    tradutor.append('MULT')
                    tradutor.append('ARMZ '+tok[index-1])

        if(tok[index] == 'printf'):
            while(tok[index] != ';'):
                if(tok[index] in variavel):
                    tradutor.append('CRVL '+tok[index])
                    tradutor.append('IMPR')
                    index = index + 1
                    nt = nt + 1
                index = index + 1
            if(nt == 0):
                tradutor.append('IMPR')

        if(not chave):        
            tradutor.insert(-1, 'DMEM ' +str(quantidade_variavel))

    pprint(tradutor)

if __name__ == "__main__":
    main()
