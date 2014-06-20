import os
from flask import Flask, render_template, request, redirect, url_for, abort, session,send_from_directory ##Se importan las librerias
from werkzeug import secure_filename
app = Flask("SML") 
app.config['UPLOAD_FOLDER'] = 'Archivos/'
app.config['ALLOWED_EXTENSIONS'] = set(['sml'])
##############################################################
    #Listas globales que se utilizan durante la ejecucion del programa

    #Listas globales que se utilizan durante la ejecucion del programa
lista_para_imprimir=[]
ListaExp=["if","then","else","let","in","end"]
ListaVariables=[]
ListaLet=[]
ListaComparar=["!=","<=",">=","<",">","="]
ListaResultados=[]
ListaOperaciones=["+","-","*","**","/","**"]
ListaOperadores=["+","-","*","**","/","**"]
ListaVariable=[]
verdadero="True"
falso="False"
#######################################################################################################
#Funcion que se encarga de concatenar los numeros que se han separado cuando converti el valor en una lista
def Pegar(lista):
    cont=0
    operaciones=0#Numero de operaciones que se tiene que hacer
    nuevaLista=[]#Lista Temporal
    otralista=[]##Lista final a retornar
    valor=""
    while lista != []:
        if lista[cont] in ListaOperaciones :#Valido las operaciones que tiene la lista
            if operaciones !=0:
                otralista=otralista+[nuevaLista[-1]]+[')']#Cierro los parentesis de las operaciones
            else:
                otralista=otralista+[nuevaLista[-1]]#Agrega el numero concatenado a la lista final
            nuevaLista.append(lista[cont])#Agrega el digito deoperacion a la lista temporal
            otralista.append(lista[cont])#Agrega el digito deoperacion a la lista final
            lista=lista[1:]#Corta la lista
            operaciones=operaciones+1
            valor=""
        elif lista[cont]=='(' :#Agraga cuando se abren parentesis
            otralista.append(lista[cont])
            lista=lista[1:]
        else:
            valor= valor+lista[cont]#Camcateba los numeros que se han separado
            lista=lista[1:]
            if ')' in valor:
                nuevaLista.append(valor[:-1])##Quita el cierre del parentesis
                
            else:
                nuevaLista.append(valor)##Agrega el valor a la lisata temporal
    otralista=otralista+[nuevaLista[-1]]##Agrego el ultimo elemento de la temporal a la final
    return otralista
##################################################################################################################
##Funcion que se encarga de reconocer y devolver el resultado de la operacion
def Operaciones(lista,var):
    print(var,"Variable de la operacion")
    parizq = "("    #
    parder = ")"
   #
    su = "+"        #Posibles operaciones que se pueden realizar
    re = "-"
       #  
    mu = "*"
       #
    di = "/"
       #
    ele = "**"      #
    pila=[]##Aqui se manejaran todos lo valores para una operacion
    otraLista=[]#Para las otra operaciones
    for elemento in lista:
        variable=str(elemento)
        if pila == []: #Agraga el valor a 
            pila.append(variable)
        elif variable == parder:
            while pila[-1] != parizq:#mientras no se cierre el parentesis
                otraLista.append(pila[-1])#Agrega los valores a la lista
                pila= pila[:-1]
            pila= pila[:-1]
        elif pila[-1] == ele or pila[-1] == parizq:#reconoce las diferentes operaciones
            if variable == mu or variable == di or variable == su or variable == re or variable == ele or variable == parizq:
                pila.append(variable)
                
            else:
                otraLista.append(variable)
        elif pila[-1]== mu or pila[-1] == di or pila[-1] == su  or pila[-1]== re:#reconoce las operaciones
            if variable == parizq:##Si se cierra el parentesis
                pila.append(variable)
            else:
                if pila[-1]== mu or pila[-1] == di or pila[-1] == su  or pila[-1]== re:
                    if variable== mu or variable == di or variable == su  or variable== re:
                       pila.append(variable)#Si es una operacion lo agrega a la lista
                    else:
                        otraLista.append(variable)
                else:
                    otraLista.append(variable)
    pila1=[]
    num1=0#Nombre de los valores
    num2=0#
    resultado=0
    eva1=""
    while otraLista != []:
        if otraLista[0]== su or otraLista[0]== re or otraLista[0]== mu or otraLista[0]== di or otraLista[0]== ele:#operaciones
##----------------Suma sin variables------------------------------------------------------
            if otraLista[0] == su and  Hay_letra(pila1) == False:#Si es suma y no hay variables
                otraLista=otraLista[1:]#Quita la operacion de la lista
                num2= int(pila1[-1])#Agarra el ultimo elemento de la lista el cual segundo en la operacion
                pila1=pila1[:-1]#Quita el numero de la lista
                num1= int(pila1[-1])#Agarra el ultimo elemento de la lista el cual primero en la operacion
                pila1=pila1[:-1]#Quita el numero de la lista
                resultado= num1 + num2 #Hace la operacion
                pila1.append(resultado)#Anade el resultado a la lista
##---------------Suma con variables----------------------------------------------------------
            elif otraLista[0] == su:#si en la suma alguno de los dos valores son variables
                otraLista=otraLista[1:]#Quita la operacion de la lista
                if pila1[-1] in ListaVariable:#Reconoce si la variable esta en la lista de variables
                    print(pila1[-1],"Variable que quiere buscar")
                    num2= int(buscar(pila1[-1]))#invoca a buscar que retorna el valor de la variable
                else:#Si no
                    num2= int(pila1[-1])#Toma el valor que recibio
                pila1=pila1[:-1]#elima el ultimo elemento
                if pila1[-1] in ListaVariable:#Reconoce si la variable esta en la lista de variables
                    num1= int(buscar(pila1[-1]))#invoca a buscar que retorna el valor de la variable
                else:#Si no
                    num1= int(pila1[-1])#Toma el valor que recibio
                pila1=pila1[:-1]#elima el ultimo elemento
                resultado= num1 + num2#Hace la operacion
                pila1.append(resultado)#Anade el resultado a la lista
##-----------------Multiplicacion sin variables-------------------------------------------
            elif otraLista[0] == mu and  Hay_letra(pila1) == False: #
                otraLista=otraLista[1:]                             #Mismo procedimiento de la suma sin variables, lo
                num2= int(pila1[-1])                                #que varia es la operacion a realiza                                  #
                pila1=pila1[:-1]                                    #
                num1= int(pila1[-1])
                pila1=pila1[:-1]
                resultado= num1 * num2#Hace la operacion
                pila1.append(resultado)
##----------------Multiplicacion con variables-----------------------------------------------
            elif otraLista[0] == mu:                #
                otraLista=otraLista[1:]             #Mismo procedimiento de la suma con variables, lo
                if pila1[-1] in ListaVariable:      #que varia es la operacion a realizar
                    num2= int(buscar(pila1[-1]))    #
                else:                               #
                    num2= int(pila1[-1])
                pila1=pila1[:-1]
                if pila1[-1] in ListaVariable:
                    num1= int(buscar(pila1[-1]))
                else:
                    num1= int(pila1[-1])
                print(pila1)
                pila1=pila1[:-1]
                resultado= num1 * num2
                pila1.append(resultado)
##-----------------Resta sin variables-------------------------------------------
            elif otraLista[0] == re and  Hay_letra(pila1) == False:
                otraLista=otraLista[1:]
                num2= int(pila1[-1])
                pila1=pila1[:-1]                #Mismo procedimiento de la suma sin variables, lo
                num1= int(pila1[-1])            #que varia es la operacion a realizar
                pila1=pila1[:-1]
                resultado= num1 - num2
                pila1.append(resultado)
##----------------Resta con variables-------------------------------------------------
            elif otraLista[0] == re:
                otraLista=otraLista[1:]
                if pila1[-1] in ListaVariable:
                    num2= int(buscar(pila1[-1]))            #Mismo procedimiento de la suma con variables, lo
                else:                                       #que varia es la operacion a realizar
                    num2= int(pila1[-1])
                pila1=pila1[:-1]
                if pila1[-1] in ListaVariable:
                    num1= int(buscar(pila1[-1]))
                else:
                    num1= int(pila1[-1])
                pila1=pila1[:-1]
                resultado= num1 - num2
                pila1.append(resultado)
##------------------Dividir sin variables----------------------------------------------    
            elif otraLista[0] == di and  Hay_letra(pila1) == False:
                otraLista=otraLista[1:]
                num2= int(pila1[-1])            #Mismo procedimiento de la suma sin variables, lo
                pila1=pila1[:-1]                #que varia es la operacion a realizar
                num1= int(pila1[-1])
                pila1=pila1[:-1]
                resultado= num1 / num2
                pila1.append(resultado)
##-----------------Dividir con variables----------------------------------------------------
            elif otraLista[0] == di:
                otraLista=otraLista[1:]
                if pila1[-1] in ListaVariable:
                    num2= int(buscar(pila1[-1]))        #Mismo procedimiento de la suma con variables, lo
                else:                                   #que varia es la operacion a realizar         
                    num2= int(pila1[-1])
                pila1=pila1[:-1]
                if pila1[-1] in ListaVariable:
                    num1= int(buscar(pila1[-1]))
                else:
                    num1= int(pila1[-1])
                pila1=pila1[:-1]
                resultado= num1 / num2
                pila1.append(resultado)
##-----------------Elevar sin variables----------------------------------------------------
            elif otraLista[0] == ele and Hay_letra(pila1) == False:
                otraLista=otraLista[1:]
                num2= int(pila1[-1])
                pila1=pila1[:-1]
                num1= int(pila1[-1])            #Mismo procedimiento de la suma sin variables, lo
                cont=1                          #que varia es la operacion a realizar    
                base= num1
                while cont < num2:
                    cont=cont=1
                    num1= num1*base
                resultado= num1
                if num2== 0:
                    resultado=1
                print(resultado)
                pila1.append(resultado)
##--------------Elevar con variables -----------------------------------------------------------
            elif otraLista[0] == ele :
                otraLista=otraLista[1:]
                num2= int(pila1[-1])
                pila1=pila1[:-1]
                num1= int(pila1[-1])                #Mismo procedimiento de la suma con variables, lo
                cont=1                              #que varia es la operacion a realizar
                base= num1
                while cont < num2:
                    cont=cont=1
                    num1= num1*base
                resultado= num1
                if num2== 0:
                    resultado=1
                print(resultado)
                pila1.append(resultado)
##--------------------Terminan las operaciones---------------
        else:
            pila1.append(otraLista[0])
            otraLista=otraLista[1:]
    #ListaVariable.append(var)#Agrega la variable a la lista de variables
    #ListaVariable.append(resultado)#Agrega el resultado a la lista de variables
    return resultado
###############################################################################################
#verifica si hay letras en una lista
def Hay_letra(lista):
    for elemento in lista:
        if str(elemento).isalpha():#identifica el tipo
            return True
    return False

#################################################################################################
#Busca el valor en la lista de variables, la variable que a sido ingresada
def buscar(variable):
    print(variable,"Variable que busca")
    cont=0
    resultado=""
    encontrado= False
    while encontrado != True:
        if ListaVariable[cont]==variable:#Si el valor de la lista = a la variable
            resultado=str(ListaVariable[cont+1])#guarda el valor
            encontrado=True
        cont=cont+1
    return resultado
def buscar2(variable):
    print(variable,"Variable que busca")
    cont=0
    resultado=""
    encontrado= False
    while encontrado != True:
        if ListaVariables[cont]==variable:#Si el valor de la lista = a la variable
            resultado=str(ListaVariables[cont+2])#guarda el valor
            encontrado=True
        cont=cont+1
    return resultado
####################################################################################################
##Valida la tupla que es ingresada,retorna el tipo de la
##tupla dependiendo del cado
def ValidarTupla(valor):
    tipo=""#variable a retornar
    if valor[1].isdigit() and valor[3].isdigit():##Valida que sean entereos
        tipo="Int*Int"
        return tipo
    if valor[1].isdigit() and valor[3] == "T" or valor[3] == "F":
        ##Valida que sea boolean y un entero
        tipo="Int*Boolean"
        return tipo
    elif valor[1] == "T" or valor[1] == "F":
        #Valida que sean booleans
        if valor[3].isdigit():
            ##Valida que los dos sean de tipo boolean
            tipo= "Boolean*Int"
            return tipo
        else:
            #Valida que al menos uno sea boolean
            tipo= "Boolean*Boolean"
            return tipo

    elif valor[1] == "[":
        #Valida si la tupla tiene una lista y lo manda a validar Lista
        valor.split(",")
        val=ValidarLista(valor[1:])
        return  val  + "List"
    else:
        val=ValidarTupla(valor[1:])
        return val 
############################################################################
##Valida los diferentes tipo de listas y retorna el tipo
##dependiendo del caso
def ValidarLista(valores):
    valor=list(valores)##Convierte en lista
    tipo=""
    if valor[1].isdigit():##Comprueba que sean enteros
        tipo="Int List"
        return tipo
    elif valor[1] == "T" or valor[1].lower == "F":
        ##Comprueban que sean booleans
        tipo= "Boolean List"
        return tipo
    elif valor[1] == "(":
        ##Valida si la lista contiene tuplas, llama a validar tupla
        return ValidarTupla(valor)
    else:
        return ValidarLista(valor[1:])+" "+ "List"
###########################################################################
##Retorna un valor booleano si tiene el formato de una tupla
def Es_Tupla(valor):
    coma=","
    for elemento in valor:
        if elemento == coma:#Busca la coma
            return True##Si es True es una tupla
    return False
##########################################################################


####################################################################################################################################
#Identifica el tipo de la variable segun el valor
#Invoca a diferentes dunciones segun el valor
def Variable(variable,valor):
    print('Entra variable')
    newValor=0
    if len(variable) > 1:##Valida todos los que tienen el igual concatenado
        if valor.isdigit():#Valida que sea un entero
            Tipo="Int"
            ListaVariable.append(Tipo)#Agrega el tipo
        elif valor[0]=='[': #identifica si es una lista
            tipo= ValidarLista(valor)#Invoca a validar lista con el valor
            ListaVariable.append(tipo)#Agrega el tipo
        elif valor[0]=='('  and Es_Tupla(valor):
            tipo=ValidarTupla(valor)#Valida que sea una tupla
            ListaVariable.append(tipo)#Agrega el tipo
        elif valor==verdadero or valor==falso:#Valida si es un boolean
            ListaVariable.append("Boolean")#Agrega el tipo
    else:#Valida los que NO tienen el igual concatenado
        if valor.isdigit():#Valida que sea un entero
            Tipo="Int"
            ListaVariable.append("Int")
        elif valor[0]=='[':#identifica si es una lista
            tipo=ValidarLista(valor)
            ListaVariable.append(tipo)
        elif valor[0]=='(' and Es_Tupla(valor):#Valida que sea una tupla
            tipo=ValidarTupla(valor)
            ListaVariable.append(tipo)
        elif valor==verdadero or valor==falso:#Valida si es un boolean
            ListaVariable.append("Boolean")
            
def Variable2(variable,valor):
    print('Entra variable')
    newValor=0
    if len(variable) > 1:##Valida todos los que tienen el igual concatenado
        if valor.isdigit():#Valida que sea un entero
            return False
        elif valor[0]=='[': #identifica si es una lista
            return False
        elif valor[0]=='('  and Es_Tupla(valor):
            return False
        elif valor==verdadero or valor==falso:#Valida si es un boolean
            return False
        else:    
            return True
    else:#Valida los que NO tienen el igual concatenado
        if valor.isdigit():#Valida que sea un entero
            return False
        elif valor[0]=='[':#identifica si es una lista
            return False
        elif valor[0]=='(' and Es_Tupla(valor):#Valida que sea una tupla
            return False
        elif valor==verdadero or valor==falso:#Valida si es un boolean
            return False
        else:
            return True
            
##################################################################################################################################
#Funcion que se encarga de identificar el formato de la variable
#ingresa cada variable y su valor en lista variables
#Llama a la funcion validar para determinar el tipo
def Validar2(token):
    largo= len(token)-1
    indice=0
    while indice <= largo:
        if token[indice]=="val"  :#Si la variable tiene la sentencia val
            if token[indice+2]=="=":#Valida si el "=" esta separado de la variable
                if Variable2(token[indice+1],token[indice+3]):
                    nuevoValor= list(token[indice+3])#Convierte al valor en la lista
                    ListaVariable.append("Int")#Agrega el tipo de la operacion
                    listaValor=Pegar(nuevoValor)#Invova a la funcion pegar
                    newValor= ["("]+listaValor+[")"]#Concatena parentesis al resultado anterior
                    resultado=Operaciones(newValor,token[indice])
                    ListaVariable.append(token[indice+1])
                    ListaVariable.append(resultado)
                else:
                    Variable(token[indice+1],token[indice+3])#Llama a la funcion variable para determinar el tipo
                    ListaVariable.append(token[indice+1])#Agrega la variable
                    ListaVariable.append(token[indice+3])#Agrega el valor
            else:#Si = esta junto a la variable
                if Variable2(token[indice+1],token[indice+2]):
                    nuevoValor= list(token[indice+2])#Convierte al valor en la lista
                    ListaVariable.append("Int")#Agrega el tipo de la operacion
                    listaValor=Pegar(nuevoValor)#Invova a la funcion pegar
                    newValor= ["("]+listaValor+[")"]#Concatena parentesis al resultado anterior
                    resultado=Operaciones(newValor,token[indice])
                    ListaVariable.append(token[indice+1])
                    ListaVariable.append(resultado)
                else:
                    Variable(token[indice+1],token[indice+2])
                    ListaVariable.append(token[indice+1])
                    ListaVariable.append(token[indice+2])
            indice=indice+1
        elif token[indice].isalpha(): #and not token[indice+2] in ListaVariable :
             print ('Entra elif de Validar2')
            #Valida que si la variable fue declarada de forma normal
             if token[indice+1]=="=":
                 if Variable2(token[indice],token[indice+2]):
                     nuevoValor= list(token[indice+2])#Convierte al valor en la lista
                     ListaVariable.append("Int")#Agrega el tipo de la operacion
                     listaValor=Pegar(nuevoValor)#Invova a la funcion pegar
                     newValor= ["("]+listaValor+[")"]#Concatena parentesis al resultado anterior
                     resultado=Operaciones(newValor,token[indice])
                     ListaVariable.append(token[indice])
                     ListaVariable.append(resultado)
                 else:
                     print ('Entra = al = de Validar2', token[indice],token[indice+2] )
                     Variable(token[indice],token[indice+2])
                     ListaVariable.append(token[indice])
                     ListaVariable.append(token[indice+2])
             else:
                 if Variable2(token[indice],token[indice+1]):
                     nuevoValor= list(token[indice+1])#Convierte al valor en la lista
                     ListaVariable.append("Int")#Agrega el tipo de la operacion
                     listaValor=Pegar(nuevoValor)#Invova a la funcion pegar
                     newValor= ["("]+listaValor+[")"]#Concatena parentesis al resultado anterior
                     resultado=Operaciones(newValor,token[indice])
                     ListaVariable.append(token[indice])
                     ListaVariable.append(resultado)
                 else:
                     Variable(token[indice],token[indice+1])
                     ListaVariable.append(token[indice])
                     ListaVariable.append(token[indice+1])
             indice=indice+1
        else:
            indice=indice+1
   
    print'Imprime',ListaVariable
    return ListaVariable

    

##Leer_Archivo()
     

def Esta_Expresion(valor):
    for i in ListaExp:
        if i == valor:
            return True
    return False
def Esta_Operador(valor):
    for i in ListaOperadores:
        if i in valor:
            print "oper",True
            return True
    return False

def Validar(token):

    largo= len(token)-1
    print(largo)
    indice=0
    while indice <= largo:
        if token[indice]=="val":
            if token[indice+2]=="=":
                if not Esta_Expresion(token[indice+3]):
                    print token[indice+3]
                    if token[indice+3].isalpha():
                        print 'entra indice isalpha'
                        cont=0
                        for i in ListaVariables:
                            if i == token[indice+3]:
                                ListaVariables.append(token[indice+1])
                                ListaVariables.append(token[indice+2])
                                ListaVariables.append(ListaVariables[cont+2])
                            cont+=1
                    if token[indice+3].isdigit():
                        ListaVariables.append(token[indice+1])
                        ListaVariables.append(token[indice+2])
                        ListaVariables.append(token[indice+3])
                    else:
                        print 'entra else'
                        ListaVariables.append(token[indice+1])
                        ListaVariables.append(token[indice+2])
                        ListaVariables.append(token[indice+3])
                elif token[indice+3] == "if":
                    i = indice+4
                    Evalua=""
                    while token[i] != "then":
                        Evalua+=token[i]
                        i+=1
                    print('i ', i, token[i])
                    print Evalua
                    if Evaluar_if(Evalua,False):
                        cont=i+1
                        print('cont ', cont, token[cont])
                        Evalua=""
                        if token[cont]=="if":
                            Evalua=""
                            contElse=0
                            while contElse!=2:
                                while token[cont] != "else":
                                    Evalua+=token[cont]
                                    print Evalua
                                    cont+=1
                                    print('cont ', cont, token[cont])
                                contElse+=1
                                if contElse==2:
                                    break
                                Evalua+=token[cont]
                                print Evalua
                                cont+=1
                                print contElse, "cont", cont, token[cont]
                            print(Evalua)
                            ListaVariables.append(token[indice+1])
                            ListaVariables.append(token[indice+2])
                            ListaVariables.append(Evaluar_then(Evalua))
                            print ListaVariables
                        else:
                            while token[cont] != "else":
                                Evalua+=token[cont]
                                cont+=1
                            print(Evalua)
                            ListaVariables.append(token[indice+1])
                            ListaVariables.append(token[indice+2])
                            ListaVariables.append(Evaluar_then(Evalua))
                            print ListaVariables
                    else:
                        cont=i+1
                        while token[cont] != "else":
                            cont+=1
                        Evalua=""
                        cont+=1
                        while token[cont] != "val":
                            Evalua+=token[cont]
                            cont+=1
                        ListaVariables.append(token[indice+1])
                        ListaVariables.append(token[indice+2])
                        ListaVariables.append(Evaluar_then(Evalua))
                        print ListaVariables
                elif token[indice+3] == "let":
                    print 'Entra a Let'
                    i = indice+4
                    print('i ', i, token[i])
                    Evalua=""
                    while token[i] != "in":
                        Evalua+=token[i]
                        Evalua+=" "
                        i+=1
                    print 'antes del in ',Evalua
                    ValidarLet(Evalua)
                    Evalua=""
                    i+=1
                    while token[i] != "end":
                        Evalua+=token[i]
                        Evalua+=" "
                        i+=1
                    Evalua=Evalua.split()
                    print 'antes del end ',Evalua
                    if Evalua[0]=="if":
                        j = 1
                        tokens=Evalua
                        Evalua=""
                        while tokens[j] != "then":
                            Evalua+=tokens[j]
                            j+=1
                        print('j ', j, tokens[j])
                        print Evalua
                        if Evaluar_if(Evalua,True):
                            cont=j+1
                            print('cont ', cont, tokens[cont])
                            Evalua=""
                            if tokens[cont]=="if":
                                Evalua=""
                                contElse=0
                                while contElse!=2:
                                    while tokens[cont] != "else":
                                        Evalua+=tokens[cont]
                                        print Evalua
                                        cont+=1
                                        print('cont ', cont, tokens[cont])
                                    contElse+=1
                                    if contElse==2:
                                        break
                                    Evalua+=tokens[cont]
                                    print Evalua
                                    cont+=1
                                    print contElse, "cont", cont, tokens[cont]
                                print(Evalua)
                                ListaVariables.append(token[indice+1])
                                ListaVariables.append(token[indice+2])
                                ListaVariables.append(Evaluar_thenLet(Evalua))
                                print ListaVariables
                            else:
                                while tokens[cont] != "else":
                                    Evalua+=tokens[cont]
                                    cont+=1
                                print(Evalua)
                                print 'indice',indice,token[indice]
                                ListaVariables.append(token[indice+1])
                                ListaVariables.append(token[indice+2])
                                ListaVariables.append(Evaluar_thenLet(Evalua))
                                print ListaVariables
                        else:
                            print 'Evalua j',j
                            cont=j+1
                            print'cont',cont,'token',tokens[cont]
                            while tokens[cont] != "else":
                                cont+=1
                            Evalua=""
                            cont+=1
                            print'cont2',cont,'tok',tokens[cont]
                            while tokens[cont] != tokens[-1]:
                                Evalua+=tokens[cont]
                                cont+=1
                            Evalua+=tokens[-1]
                            print 'indice',Evalua
                            ListaVariables.append(token[indice+1])
                            ListaVariables.append(token[indice+2])
                            ListaVariables.append(Evaluar_thenLet(Evalua))
                            print ListaVariables
                    indice = i+1    
            else:
                if not Esta_Expresion(token[indice+2]):
                    Variable(token[indice+1],token[indice+2])
            indice=indice+1
        else:
            indice=indice+1
    print ("Si funciona")
    print (ListaVariables)
    print('Algo despues de print LV')
    Validar2(ListaVariables)

def ValidarLet(token):
    print "entra Let", token
    token=token.split()
    print token
    largo= len(token)-1
    print(largo)
    indice=0
    while indice <= largo:
        if token[indice]=="val":
            if token[indice+2]=="=":
                if not Esta_Expresion(token[indice+3]):
                    if token[indice+3].isalpha():
                        print'entra indice let alpha'
                        if token[indice+3] in ListaLet:
                            print'entra en listalet'
                            cont=0
                            for i in ListaVariables:
                                if i == token[indice+3]:
                                    ListaLet.append(token[indice+1])
                                    ListaLet.append(token[indice+2])
                                    ListaLet.append(ListaLet[cont+2])
                                cont+=1
                        elif token[indice+3] in ListaVariables:
                            print'entra en listaVariables'
                            cont=0
                            for i in ListaVariables:
                                if i == token[indice+3]:
                                    ListaLet.append(token[indice+1])
                                    ListaLet.append(token[indice+2])
                                    ListaLet.append(ListaVariables[cont+2])
                                cont+=1
                    else:
                        ListaLet.append(token[indice+1])
                        ListaLet.append(token[indice+2])
                        ListaLet.append(token[indice+3])
                    print "ListaLet ",ListaLet
                elif token[indice+3] == "if":
                    i = indice+4
                    Evalua=""
                    while token[i] != "then":
                        Evalua+=token[i]
                        i+=1
                    print('i ', i, token[i])
                    print Evalua
                    if Evaluar_if(Evalua,True):
                        cont=i+1
                        print('cont ', cont, token[cont])
                        Evalua=""
                        if token[cont]=="if":
                            Evalua=""
                            contElse=0
                            while contElse!=2:
                                while token[cont] != "else":
                                    Evalua+=token[cont]
                                    print Evalua
                                    cont+=1
                                    print('cont ', cont, token[cont])
                                contElse+=1
                                if contElse==2:
                                    break
                                Evalua+=token[cont]
                                print Evalua
                                cont+=1
                                print contElse, "cont", cont, token[cont]
                            print(Evalua)
                            ListaLet.append(token[indice+1])
                            ListaLet.append(token[indice+2])
                            ListaLet.append(Evaluar_then(Evalua))
                            print ListaLet
                        else:
                            while token[cont] != "else":
                                Evalua+=token[cont]
                                cont+=1
                            print(Evalua)
                            ListaLet.append(token[indice+1])
                            ListaLet.append(token[indice+2])
                            ListaLet.append(Evaluar_then(Evalua))
                            print ListaLet
                    else:
                        cont=i+1
                        while token[cont] != "else":
                            cont+=1
                        Evalua=""
                        cont+=1
                        while token[cont] != "val":
                            Evalua+=token[cont]
                            cont+=1
                        ListaLet.append(token[indice+1])
                        ListaLet.append(token[indice+2])
                        ListaLet.append(Evaluar_then(Evalua))
                        print ListaLet
                elif token[indice+3] == "let":
                    i = indice+4
                    Evalua=""
                    while token[i] != "in":
                        Evalua+=token[i]
                        i+=1
                    ValidarLet(Evalua)
            else:
                if not Esta_Expresion(token[indice+2]):
                    Variable(token[indice+1],token[indice+2])
            indice=indice+1
        else:
            indice=indice+1
    print ("Si funciona")
    print (ListaLet)


def Variablexxx(variable,valor):
    if len(variable) > 1:
        print(variable[0],variable[1],valor)
    else:
        print(variable,"=",valor)
     
def Evaluar_if (cadena,let):
    print cadena
    And_Or=[]
    Evaluacion = cadena
    if "andalso" in cadena or "orelse" in cadena:
        print "Entra and or"
        Evaluacion=Evaluacion.replace("(","")
        Evaluacion=Evaluacion.replace(")","")
        Evaluacion=Evaluacion.replace(" ","")
        print Evaluacion
        for i in Evaluacion:
            if "andalso" in Evaluacion:
                print 'entra y agrega and a lista'
                Evaluacion= Evaluacion.split("andalso")
                And_Or.append("andalso")
            Eval=[]
            for j in Evaluacion:
                if "orelse" in j:
                    print 'entra and y agrega OR a lista'
                    Eval.append(j.split("orelse"))
                    print Eval
                    if not "orelse" in And_Or:
                        print 'entra elif not y agrega OR a lista'
                        And_Or.append("orelse")
            if Eval != []:
                Evaluacion=Eval
        for j in Evaluacion:
            if "orelse" in Evaluacion:
                print 'entra y agrega OR a lista'
                Evaluacion= j.split("orelse")
                And_Or.append("orelse")
        print Evaluacion
        print And_Or
        if len(And_Or)>1:
            while And_Or != []:
                print And_Or
                if And_Or[-1]=="orelse":
                    cont=0
                    for i in Evaluacion:
                        for j in i:
                            if Evaluar(j,let):
                                Evaluacion[cont]=True
                                break
                        if Evaluacion[cont]!=True:
                            Evaluacion[cont]=False
                        cont+=1
                else:
                    cont=0
                    for i in Evaluacion:
                        print 'i and',i
                        if i:
                            cont+=1
                    if cont==len(Evaluacion):
                        return True
                And_Or=And_Or[:-1]
            return False
        else:
            print 'entra else despues de len And_Or'
            if And_Or[0] == "orelse":
                for i in Evaluacion:
                    if Evaluar(i,let):
                        return True
                return False
            else:
                print 'entra else despues del else por And'
                cont=0
                for i in Evaluacion:
                    if Evaluar(i,let):
                        cont+=1
                if cont==len(Evaluacion):
                    return True
                else:
                    return False
    print 'Evaluacion',Evaluacion
    return Evaluar(Evaluacion,let)

def Evaluar(cadena,let):
    if '#' in cadena:
        print "Entra evaluar hay tupla #"
        if let:
            return Evaluar_tuplaLet(cadena)
        else:
            return Evaluar_tupla(cadena)
    elif cadena.isalpha():
        if let:
            if cadena in ListaLet:
                Valor=BuscarLet(cadena)
            elif cadena in ListaVariables:
                Valor=buscar2(cadena)
        else:
            Valor=buscar2(cadena)
        if Valor == 'True':
            return True
        else:
            return False
        return 'Es lista'
    else:
        for i in ListaComparar:
            if i in cadena:
                valores=cadena.split(i)
                print valores
                for j in ListaOperadores:
                    if j in valores[0] and j in valores[1]:
                        print("Son operaciones")
                        nuevoValor= list(valores[0])#Convierte al valor en la lista
                        listaValor=Pegar(nuevoValor)#Invova a la funcion pegar
                        newValor= ["("]+listaValor+[")"]
                        valores[0]=str(operacionIL(newValor,let))
                        nuevoValor1= list(valores[1])#Convierte al valor en la lista
                        listaValor1=Pegar(nuevoValor1)#Invova a la funcion pegar
                        newValor1= ["("]+listaValor1+[")"]
                        valores[1]=str(operacionIL(newValor1,let))
                        #return Comparar(Val1,Val2,i)
                    elif j in valores[0]:
                        print("La primera es operacion")
                        nuevoValor= list(valores[0])#Convierte al valor en la lista
                        listaValor=Pegar(nuevoValor)#Invova a la funcion pegar
                        newValor= ["("]+listaValor+[")"]
                        valores[0]=str(operacionIL(newValor,let))
                        #return Comparar(Val1,valores[1],i)
                    elif j in valores[1]:
                        print("La segunda es operacion")
                        nuevoValor= list(valores[1])#Convierte al valor en la lista
                        listaValor=Pegar(nuevoValor)#Invova a la funcion pegar
                        newValor= ["("]+listaValor+[")"]
                        valores[1]=str(operacionIL(newValor,let))
                        #return Comparar(valores[0],Val2,i)
                if valores[0].isdigit() and valores[1].isdigit():
                    print "valor1 num val2 num"
                    return Comparar(valores[0],valores[1],i)
                elif valores[0].isalpha() or valores[1].isalpha():
                    print "valor1 o val2 alpha"
                    if let:
                        print('entra alpha let')
                        return Evaluar_variablesLet(valores,i)
                    else:
                        return Evaluar_variables(valores,i)
                    
            
def Comparar(valor1, valor2, comparador):
    Val1=int(valor1)
    Val2=int(valor2)
    if comparador == "=":
        print "entra ="
        if Val1 == Val2:
            print "entra =="
            return True
        else:
            return False
    elif comparador == "!=":
        print "entra !="
        if Val1 != Val2:
            return True
        else:
            return False
    elif comparador == "<":
        print "entra <"
        if Val1 < Val2:
            print "Es True"
            return True
        else:
            return False
    elif comparador == "<=":
        print "entra <="
        if Val1 <= Val2:
            return True
        else:
            return False
    elif comparador == ">":
        print "entra >"
        if Val1 > Val2:
            print "Es True"
            return True
        else:
            return False
    elif comparador >= ">=":
        print "entra >="
        if Val1 == Val2:
            return True
        else:
            return False
    
def Evaluar_variables(valores,comparador):
    if valores[0].isalpha() and valores[1].isalpha():
        print"2 alpha"
        cont=0
        for i in ListaVariables:
            if i == valores[0]:
                Val1 = ListaVariables[cont+2]
            elif i==valores[1]:
                Val2 = ListaVariables[cont+2]
            cont+=1
        return Comparar(Val1, Val2, comparador)
    if valores[0].isalpha():
        print"1 es alpha"
        cont=0
        for i in ListaVariables:
            if i == valores[0]:
                Val1 = ListaVariables[cont+2]
            cont+=1
        Val2=valores[1]
        print Val1, Val2, comparador
        return Comparar(Val1, Val2, comparador)
    elif valores[1].isalpha():
        print "2 es alpha"
        cont=0
        for i in ListaVariables:
            if i == valores[1]:
                Val2 = ListaVariables[cont+2]
            cont+=1
        Val1=valores[0]
        print Val1, Val2, comparador
        return Comparar(Val1, Val2, comparador)
        
def Evaluar_variablesLet(valores,comparador):
    if valores[0].isalpha() and valores[1].isalpha():
        print"2 alpha"
        cont=0
        if valores[0] in ListaLet:
            cont=0
            for i in ListaLet:
                if i == valores[0]:
                    Val1 = ListaLet[cont+2]
                    break
                cont+=1
        elif valores[0] in ListaVariables:
            cont=0
            for i in ListaVariables:
                if i == valores[0]:
                    Val1 = ListaVariables[cont+2]
                    break
                cont+=1
        if valores[1] in ListaLet:
            cont=0
            for i in ListaLet:
                if i==valores[1]:
                    Val2 = ListaLet[cont+2]
                    break
                cont+=1
        elif valores[1] in ListaVariables:
            for i in ListaVariables:
                if i==valores[1]:
                    Val2 = ListaVariables[cont+2]
                    break
                cont+=1
        print 'vals ',Val1,Val2
        return Comparar(Val1, Val2, comparador)
    if valores[0].isalpha():
        print"1 es alpha"
        if valores[0] in ListaLet or valores[0] in ListaVariables:
            cont=0
            bandera=True
            for i in ListaLet:
                if i == valores[0]:
                    Val1 = ListaLet[cont+2]
                    bandera=False
                    break
                cont+=1
            if bandera:
                for i in ListaVariables:
                    if i == valores[0]:
                        Val1 = ListaVariables[cont+2]
                        break
                    cont+=1
        Val2=valores[1]
        print Val1, Val2, comparador
        return Comparar(Val1, Val2, comparador)
    elif valores[1].isalpha():
        print "2 es alpha"
        if valores[1] in ListaLet or valores[1] in ListaVariables:
            ccont=0
            badera=True
            for i in ListaLet:
                if i==valores[1]:
                    Val2 = ListaLet[cont+2]
                    badera=False
                    break
                cont+=1
            if bandera:
                for i in ListaLet:
                    if i==valores[1]:
                        Val2 = ListaVariables[cont+2]
                        break
                    cont+=1
        Val1=valores[0]
        print Val1, Val2, comparador
        return Comparar(Val1, Val2, comparador)


def Evaluar_tupla(cadena):
    for i in ListaComparar:
        if i in cadena:
            Valores=cadena.split(i)
            if "#" == Valores[0][0] and "#" == Valores[1][0]:
                print('# = #')
                cont = 0
                for j in ListaVariables:
                    if Valores[0][2:len(Valores[0])] == j:
                        tupla = ListaVariables[cont+2]
                        tupla=tupla.replace('(','')
                        tupla=tupla.replace(')','')
                        tupla=tupla.split(',')
                        if Valores[0][1]=='1':
                            Val1=tupla[0]
                        else:
                            Val1=tupla[1]
                    if Valores[1][2:len(Valores[1])] == j:
                        tupla = ListaVariables[cont+2]
                        tupla=tupla.replace('(','')
                        tupla=tupla.replace(')','')
                        tupla=tupla.split(',')
                        if Valores[1][1]=='1':
                            Val2=tupla[0]
                        else:
                            Val2=tupla[1]
                    cont+=1    
                print Valores, Val1, Val2
                return Comparar(Val1, Val2, i)
            if "#" == Valores[0][0] and Valores[1].isdigit():
                print('# = 7')
                cont = 0
                for j in ListaVariables:
                    if Valores[0][2:len(Valores[0])] == j:
                        tupla = ListaVariables[cont+2]
                        tupla=tupla.replace('(','')
                        tupla=tupla.replace(')','')
                        tupla=tupla.split(',')
                        if Valores[0][1]=='1':
                            Val1=tupla[0]
                        else:
                            Val1=tupla[1]
                    cont+=1
                Val2=Valores[1]
                return Comparar(Val1, Val2, i)
            if Valores[0].isdigit() and "#" == Valores[1][0]:
                print('7 = #')
                cont = 0
                print Valores[1][2:len(Valores[1])]
                for j in ListaVariables:
                    if Valores[1][2:len(Valores[1])] == j:
                        tupla = ListaVariables[cont+2]
                        tupla=tupla.replace('(','')
                        tupla=tupla.replace(')','')
                        tupla=tupla.split(',')
                        if Valores[1][1]=='1':
                            Val2=tupla[0]
                        else:
                            Val2=tupla[1]
                    cont+=1
                Val1=Valores[0]
                return Comparar(Val1, Val2, i)
            if "#" == Valores[0][0] and Valores[1].isalpha():
                print('# = n')
                cont = 0
                print Valores[0][2:len(Valores[0])]
                for j in ListaVariables:
                    if Valores[0][2:len(Valores[0])] == j:
                        tupla = ListaVariables[cont+2]
                        tupla=tupla.replace('(','')
                        tupla=tupla.replace(')','')
                        tupla=tupla.split(',')
                        if Valores[0][1]=='1':
                            Val1=tupla[0]
                        else:
                            Val1=tupla[1]
                    if Valores[1] == j:
                        Val2=ListaVariables[cont+2]
                    cont+=1
                print Val1, Val2
                return Comparar(Val1, Val2, i)
            if Valores[0].isalpha() and "#" == Valores[1][0]:
                print('n = #')
                cont = 0
                print Valores[1][2:len(Valores[1])]
                for j in ListaVariables:
                    if Valores[1][2:len(Valores[1])] == j:
                        tupla = ListaVariables[cont+2]
                        tupla=tupla.replace('(','')
                        tupla=tupla.replace(')','')
                        tupla=tupla.split(',')
                        if Valores[1][1]=='1':
                            Val2=tupla[0]
                        else:
                            Val2=tupla[1]
                    if Valores[0] == j:
                        print ('val2', ListaVariables[cont+2])
                        Val1=ListaVariables[cont+2]
                    cont+=1
                print Val1, i, Val2
                print Comparar(Val1, Val2, i)
                return Comparar(Val1, Val2, i)
            else:
                if '#' == Valores[0][0]:
                    print('# = ope')
                    cont = 0
                    for j in ListaVariables:
                        if Valores[0][2:len(Valores[0])] == j:
                            tupla = ListaVariables[cont+2]
                            tupla=tupla.replace('(','')
                            tupla=tupla.replace(')','')
                            tupla=tupla.split(',')
                            if Valores[0][1]=='1':
                                Val1=tupla[0]
                            else:
                                Val1=tupla[1]
                        cont+=1
                    nuevoValor= list(Valores[1])#Convierte al valor en la lista
                    listaValor=Pegar(nuevoValor)#Invova a la funcion pegar
                    newValor= ["("]+listaValor+[")"]
                    Val2=str(operacionIL(newValor,False))
                    return Comparar(Val1, Val2, i)
                else:
                    print('# = ope')
                    cont = 0
                    for j in ListaVariables:
                        if Valores[1][2:len(Valores[1])] == j:
                            tupla = ListaVariables[cont+2]
                            tupla=tupla.replace('(','')
                            tupla=tupla.replace(')','')
                            tupla=tupla.split(',')
                            if Valores[1][1]=='1':
                                Val2=tupla[0]
                            else:
                                Val2=tupla[1]
                        cont+=1
                    nuevoValor= list(Valores[0])#Convierte al valor en la lista
                    listaValor=Pegar(nuevoValor)#Invova a la funcion pegar
                    newValor= ["("]+listaValor+[")"]
                    Val1=str(operacionIL(newValor,False))
                    return Comparar(Val1, Val2, i)

    print cadena[2:len(cadena)]
    cont=0
    for i in ListaVariables:
        if cadena[2:len(cadena)] == i:
            tupla = ListaVariables[cont+2]
            tupla=tupla.replace('(','')
            tupla=tupla.replace(')','')
            tupla=tupla.split(',')
            if cadena[1]=='1':
                if 'true' in tupla[0]:
                    return True
                else:
                    return False
            else:
                if 'true' in tupla[1]:
                    return True
                else:
                    return False
        cont+=1

def Evaluar_tuplaLet(cadena):
    print 'Evalua tupla let', cadena
    for i in ListaComparar:
        if i in cadena:
            Valores=cadena.split(i)
            print Valores
            if "#" == Valores[0][0] and "#" == Valores[1][0]:
                print('# = #')
                cont = 0
                if Valores[0][2:len(Valores[0])] in ListaLet or Valores[1][2:len(Valores[1])] in ListaLet:
                    for j in ListaLet:
                        if Valores[0][2:len(Valores[0])] == j:
                            tupla = ListaLet[cont+2]
                            tupla=tupla.replace('(','')
                            tupla=tupla.replace(')','')
                            tupla=tupla.split(',')
                            if Valores[0][1]=='1':
                                Val1=tupla[0]
                            else:
                                Val1=tupla[1]
                        if Valores[1][2:len(Valores[1])] == j:
                            tupla = ListaLet[cont+2]
                            tupla=tupla.replace('(','')
                            tupla=tupla.replace(')','')
                            tupla=tupla.split(',')
                            if Valores[1][1]=='1':
                                Val2=tupla[0]
                            else:
                                Val2=tupla[1]
                        cont+=1    
                else:
                    for j in ListaVariables:
                        if Valores[0][2:len(Valores[0])] == j:
                            tupla = ListaVariables[cont+2]
                            tupla=tupla.replace('(','')
                            tupla=tupla.replace(')','')
                            tupla=tupla.split(',')
                            if Valores[0][1]=='1':
                                Val1=tupla[0]
                            else:
                                Val1=tupla[1]
                        if Valores[1][2:len(Valores[1])] == j:
                            tupla = ListaVariables[cont+2]
                            tupla=tupla.replace('(','')
                            tupla=tupla.replace(')','')
                            tupla=tupla.split(',')
                            if Valores[1][1]=='1':
                                Val2=tupla[0]
                            else:
                                Val2=tupla[1]
                        cont+=1        
                print Valores, Val1, Val2
                return Comparar(Val1, Val2, i)
            if "#" == Valores[0][0] and Valores[1].isdigit():
                print('# = 7')
                cont = 0
                if Valores[0][2:len(Valores[0])] in ListaLet:
                    for j in ListaLet:
                        if Valores[0][2:len(Valores[0])] == j:
                            tupla = ListaLet[cont+2]
                            tupla=tupla.replace('(','')
                            tupla=tupla.replace(')','')
                            tupla=tupla.split(',')
                            if Valores[0][1]=='1':
                                Val1=tupla[0]
                            else:
                                Val1=tupla[1]
                else:
                    for j in ListaVariables:
                        if Valores[0][2:len(Valores[0])] == j:
                            tupla = ListaVariables[cont+2]
                            tupla=tupla.replace('(','')
                            tupla=tupla.replace(')','')
                            tupla=tupla.split(',')
                            if Valores[0][1]=='1':
                                Val1=tupla[0]
                            else:
                                Val1=tupla[1]
                        cont+=1
                Val2=Valores[1]
                return Comparar(Val1, Val2, i)
            if Valores[0].isdigit() and "#" == Valores[1][0]:
                print('7 = #')
                cont = 0
                print Valores[1][2:len(Valores[1])]
                if Valores[1][2:len(Valores[1])] in ListaLet:
                    for j in ListaLet:
                        if Valores[1][2:len(Valores[1])] == j:
                            tupla = ListaLet[cont+2]
                            tupla=tupla.replace('(','')
                            tupla=tupla.replace(')','')
                            tupla=tupla.split(',')
                            if Valores[1][1]=='1':
                                Val2=tupla[0]
                            else:
                                Val2=tupla[1]
                        cont+=1
                else:
                     for j in ListaVariables:
                        if Valores[1][2:len(Valores[1])] == j:
                            tupla = ListaVariables[cont+2]
                            tupla=tupla.replace('(','')
                            tupla=tupla.replace(')','')
                            tupla=tupla.split(',')
                            if Valores[1][1]=='1':
                                Val2=tupla[0]
                            else:
                                Val2=tupla[1]
                        cont+=1
                Val1=Valores[0]
                return Comparar(Val1, Val2, i)
            if "#" == Valores[0][0] and Valores[1].isalpha():
                print('# = n')
                cont = 0
                print Valores[0][2:len(Valores[0])]
                if Valores[0][2:len(Valores[0])] in ListaLet:
                    for j in ListaLet:
                        if Valores[0][2:len(Valores[0])] == j:
                            tupla = ListaLet[cont+2]
                            tupla=tupla.replace('(','')
                            tupla=tupla.replace(')','')
                            tupla=tupla.split(',')
                            if Valores[0][1]=='1':
                                Val1=tupla[0]
                            else:
                                Val1=tupla[1]
                        if Valores[1] == j:
                            Val2=ListaLet[cont+2]
                        cont+=1
                else:
                    for j in ListaVariables:
                        if Valores[0][2:len(Valores[0])] == j:
                            tupla = ListaVariables[cont+2]
                            tupla=tupla.replace('(','')
                            tupla=tupla.replace(')','')
                            tupla=tupla.split(',')
                            if Valores[0][1]=='1':
                                Val1=tupla[0]
                            else:
                                Val1=tupla[1]
                        if Valores[1] == j:
                            Val2=ListaVariables[cont+2]
                        cont+=1
                print Val1, Val2
                return Comparar(Val1, Val2, i)
            if Valores[0].isalpha() and "#" == Valores[1][0]:
                print('n = #')
                cont = 0
                print Valores[1][2:len(Valores[1])]
                if Valores[1][2:len(Valores[0])] in ListaLet:
                    for j in ListaLet:
                        if Valores[1][2:len(Valores[1])] == j:
                            tupla = ListaLet[cont+2]
                            tupla=tupla.replace('(','')
                            tupla=tupla.replace(')','')
                            tupla=tupla.split(',')
                            if Valores[1][1]=='1':
                                Val2=tupla[0]
                            else:
                                Val2=tupla[1]
                        if Valores[0] == j:
                            Val1=ListaLet[cont+2]
                        cont+=1
                else:
                    for j in ListaVariables:
                        if Valores[1][2:len(Valores[1])] == j:
                            tupla = ListaVariables[cont+2]
                            tupla=tupla.replace('(','')
                            tupla=tupla.replace(')','')
                            tupla=tupla.split(',')
                            if Valores[1][1]=='1':
                                Val2=tupla[0]
                            else:
                                Val2=tupla[1]
                        if Valores[0] == j:
                            print ('val2', ListaVariables[cont+2])
                            Val1=ListaVariables[cont+2]
                        cont+=1
                print Val1, i, Val2
                print Comparar(Val1, Val2, i)
                return Comparar(Val1, Val2, i)
            else:
                if '#' == Valores[0][0]:
                    print('# = ope')
                    cont = 0
                    if Valores[0][2:len(Valores[0])] in ListaLet:
                        for j in ListaLet:
                            if Valores[0][2:len(Valores[0])] == j:
                                tupla = ListaLet[cont+2]
                                tupla=tupla.replace('(','')
                                tupla=tupla.replace(')','')
                                tupla=tupla.split(',')
                                if Valores[0][1]=='1':
                                    Val1=tupla[0]
                                else:
                                    Val1=tupla[1]
                    else:
                        for j in ListaVariables:
                            if Valores[0][2:len(Valores[0])] == j:
                                tupla = ListaVariables[cont+2]
                                tupla=tupla.replace('(','')
                                tupla=tupla.replace(')','')
                                tupla=tupla.split(',')
                                if Valores[0][1]=='1':
                                    Val1=tupla[0]
                                else:
                                    Val1=tupla[1]
                            cont+=1
                    nuevoValor= list(Valores[1])#Convierte al valor en la lista
                    listaValor=Pegar(nuevoValor)#Invova a la funcion pegar
                    newValor= ["("]+listaValor+[")"]
                    Val2=str(operacionIL(newValor,True))
                    return Comparar(Val1, Val2, i)
                else:
                    print('# = ope')
                    cont = 0
                    if Valores[1][2:len(Valores[1])] in ListaLet:
                        for j in ListaLet:
                            if Valores[1][2:len(Valores[1])] == j:
                                tupla = ListaLet[cont+2]
                                tupla=tupla.replace('(','')
                                tupla=tupla.replace(')','')
                                tupla=tupla.split(',')
                                if Valores[1][1]=='1':
                                    Val2=tupla[0]
                                else:
                                    Val2=tupla[1]
                    else:
                        for j in ListaVariables:
                            if Valores[1][2:len(Valores[1])] == j:
                                tupla = ListaVariables[cont+2]
                                tupla=tupla.replace('(','')
                                tupla=tupla.replace(')','')
                                tupla=tupla.split(',')
                                if Valores[1][1]=='1':
                                    Val2=tupla[0]
                                else:
                                    Val2=tupla[1]
                            cont+=1
                    nuevoValor= list(Valores[0])#Convierte al valor en la lista
                    listaValor=Pegar(nuevoValor)#Invova a la funcion pegar
                    newValor= ["("]+listaValor+[")"]
                    Val1=str(operacionIL(newValor,True))
                    return Comparar(Val1, Val2, i)

    print cadena[2:len(cadena)]
    cont = 0
    if cadena[2:len(cadena)] in ListaLet:
        for i in ListaLet:
            if cadena[2:len(cadena)] == i:
                tupla = ListaLet[cont+2]
                tupla=tupla.replace('(','')
                tupla=tupla.replace(')','')
                tupla=tupla.split(',')
                if cadena[1]=='1':
                    if 'true' in tupla[0]:
                        return True
                    else:
                        return False
                else:
                    if 'true' in tupla[1]:
                        return True
                    else:
                        return False
            cont+=1
    else:
        for i in ListaVariables:
            if cadena[2:len(cadena)] == i:
                tupla = ListaVariables[cont+2]
                tupla=tupla.replace('(','')
                tupla=tupla.replace(')','')
                tupla=tupla.split(',')
                if cadena[1]=='1':
                    if 'true' in tupla[0]:
                        return True
                    else:
                        return False
                else:
                    if 'true' in tupla[1]:
                        return True
                    else:
                        return False
            cont+=1


def Evaluar_then(cadena):
    print cadena
    if '#' in cadena:
        for i in ListaComparar:
            if i in cadena:
                print('hay una comparacion')
                Evaluar_Tupla(cadena)
        print cadena[2:len(cadena)]
        cont = 0
        for i in ListaVariables:
            if cadena[2:len(cadena)] == i:
                tupla = ListaVariables[cont+2]
                tupla=tupla.replace('(','')
                tupla=tupla.replace(')','')
                tupla=tupla.split(',')
                if cadena[1]=='1':
                    return tupla[0]
                else:
                    return tupla[1]
            cont+=1
    elif cadena.isdigit():
        return cadena
    elif cadena.isalpha():
        print "entra is alpha"
        cont=0
        for i in ListaVariables:
            if i == cadena:
                print i
                return ListaVariables[cont+2]
            cont+=1
    elif cadena[0:2] == "if":
        Evalua=cadena[2:len(cadena)]
        Evalua=Evalua.split("then")
        print Evalua
        if Evaluar_if(Evalua[0],False):
            print(Evalua)
            Evalua=Evalua[1].split('else')
            return Evaluar_then(Evalua[0])
        else:
            Evalua=Evalua[1].split('else')
            return Evaluar_then(Evalua[1])
    elif cadena[0:3] == 'let':
        print 'es un let'
    else:
        return cadena
        
    


def Evaluar_thenLet(cadena):
    print cadena
    if '#' in cadena:
        for i in ListaComparar:
            if i in cadena:
                print('hay una comparacion')
                Evaluar_Tupla(cadena)
        print cadena[2:len(cadena)]
        if cadena[2:len(cadena)] in ListaLet:
            cont = 0
            for i in ListaVariables:
                if cadena[2:len(cadena)] == i:
                    tupla = ListaLet[cont+2]
                    tupla=tupla.replace('(','')
                    tupla=tupla.replace(')','')
                    tupla=tupla.split(',')
                    if cadena[1]=='1':
                        return tupla[0]
                    else:
                        return tupla[1]
                cont+=1
        if cadena[2:len(cadena)] in ListaVariables:
            cont = 0
            for i in ListaVariables:
                if cadena[2:len(cadena)] == i:
                    tupla = ListaVariables[cont+2]
                    tupla=tupla.replace('(','')
                    tupla=tupla.replace(')','')
                    tupla=tupla.split(',')
                    if cadena[1]=='1':
                        return tupla[0]
                    else:
                        return tupla[1]
                cont+=1
    elif cadena.isdigit():
        return cadena
    elif cadena.isalpha():
        print "entra is alpha"
        if cadena in ListaLet:
            cont=0
            for i in ListaLet:
                if i == cadena:
                    print i
                    return ListaLet[cont+2]
                cont+=1
        elif cadena in ListaVariables:
            cont=0
            for i in ListaVariables:
                if i == cadena:
                    print i
                    return ListaVariables[cont+2]
                cont+=1
    elif cadena[0:2] == "if":
        print 'entra if de evaluaLet'
        Evalua=cadena[2:len(cadena)]
        #Evalua=""
        Evalua=Evalua.split("then")
        print Evalua
        #print('i ', i, token[i])
        if Evaluar_if(Evalua[0],True):
            print(Evalua)
            Evalua=Evalua[1].split('else')
            return Evaluar_thenLet(Evalua[0])
        else:
            Evalua=Evalua[1].split('else')
            return Evaluar_thenLet(Evalua[0])

def buscarIL(variable):
    print(variable,"Variable que busca")
    cont=0
    resultado=""
    encontrado= False
    while encontrado != True:
        if ListaVariables[cont]==variable:#Si el valor de la lista = a la variable
            resultado=str(ListaVariables[cont+1])#guarda el valor
            encontrado=True
        cont=cont+1
    return resultado

def buscarILet(variable):
    print(variable,"Variable que busca")
    cont=0
    resultado=""
    encontrado= False
    while encontrado != True:
        if ListaLet[cont]==variable:#Si el valor de la lista = a la variable
            resultado=str(ListaLet[cont+2])#guarda el valor
            encontrado=True
        cont=cont+1
    return resultado

def operacionIL(lista, let):
    parizq = "("    #
    parder = ")"
   #
    su = "+"        #Posibles operaciones que se pueden realizar
    re = "-"
       #  
    mu = "*"
       #
    di = "/"
       #
    ele = "**"      #
    pila=[]##Aqui se manejaran todos lo valores para una operacion
    otraLista=[]#Para las otra operaciones
    for elemento in lista:
        variable=str(elemento)
        if pila == []: #Agraga el valor a 
            pila.append(variable)
        elif variable == parder:
            while pila[-1] != parizq:#mientras no se cierre el parentesis
                otraLista.append(pila[-1])#Agrega los valores a la lista
                pila= pila[:-1]
            pila= pila[:-1]
        elif pila[-1] == ele or pila[-1] == parizq:#reconoce las diferentes operaciones
            if variable == mu or variable == di or variable == su or variable == re or variable == ele or variable == parizq:
                pila.append(variable)
                
            else:
                otraLista.append(variable)
        elif pila[-1]== mu or pila[-1] == di or pila[-1] == su  or pila[-1]== re:#reconoce las operaciones
            if variable == parizq:##Si se cierra el parentesis
                pila.append(variable)
            else:
                if pila[-1]== mu or pila[-1] == di or pila[-1] == su  or pila[-1]== re:
                    if variable== mu or variable == di or variable == su  or variable== re:
                       pila.append(variable)#Si es una operacion lo agrega a la lista
                    else:
                        otraLista.append(variable)
                else:
                    otraLista.append(variable)
    pila1=[]
    num1=0#Nombre de los valores
    num2=0#
    resultado=0
    eva1=""
    while otraLista != []:
        if let:
            if otraLista[0]== su or otraLista[0]== re or otraLista[0]== mu or otraLista[0]== di or otraLista[0]== ele:#operaciones
##----------------Suma sin variables------------------------------------------------------
                if otraLista[0] == su and  Hay_letra(pila1) == False:#Si es suma y no hay variables
                    otraLista=otraLista[1:]#Quita la operacion de la lista
                    num2= int(pila1[-1])#Agarra el ultimo elemento de la lista el cual segundo en la operacion
                    pila1=pila1[:-1]#Quita el numero de la lista
                    num1= int(pila1[-1])#Agarra el ultimo elemento de la lista el cual primero en la operacion
                    pila1=pila1[:-1]#Quita el numero de la lista
                    resultado= num1 + num2 #Hace la operacion
                    pila1.append(resultado)#Anade el resultado a la lista
##---------------Suma con variables----------------------------------------------------------
                elif otraLista[0] == su:#si en la suma alguno de los dos valores son variables
                    otraLista=otraLista[1:]#Quita la operacion de la lista
                    if pila1[-1] in ListaLet:#Reconoce si la variable esta en la lista de variables
                        print(pila1[-1],"Variable que quiere buscar")
                        num2= int(buscarILet(pila1[-1]))#invoca a buscar que retorna el valor de la variable
                    elif pila1[-1] in ListaVariable:#Reconoce si la variable esta en la lista de variables
                        print(pila1[-1],"Variable que quiere buscar")
                        num2= int(buscarIL(pila1[-1]))#invoca a buscar que retorna el valor de la variable
                    else:#Si no
                        num2= int(pila1[-1])#Toma el valor que recibio
                    pila1=pila1[:-1]#elima el ultimo elemento
                    if pila1[-1] in ListaLet:#Reconoce si la variable esta en la lista de variables
                        num1= int(buscarILet(pila1[-1]))#invoca a buscar que retorna el valor de la variable
                    elif pila1[-1] in ListaVariable:#Reconoce si la variable esta en la lista de variables
                        num1= int(buscarIL(pila1[-1]))#invoca a buscar que retorna el valor de la variable
                    else:#Si no
                        num1= int(pila1[-1])#Toma el valor que recibio
                    pila1=pila1[:-1]#elima el ultimo elemento
                    resultado= num1 + num2#Hace la operacion
                    pila1.append(resultado)#Anade el resultado a la lista
##-----------------Multiplicacion sin variables-------------------------------------------
                elif otraLista[0] == mu and  Hay_letra(pila1) == False: #
                    otraLista=otraLista[1:]                             #Mismo procedimiento de la suma sin variables, lo
                    num2= int(pila1[-1])                                #que varia es la operacion a realiza                                  #
                    pila1=pila1[:-1]                                    #
                    num1= int(pila1[-1])
                    pila1=pila1[:-1]
                    resultado= num1 * num2#Hace la operacion
                    pila1.append(resultado)
##----------------Multiplicacion con variables-----------------------------------------------
                elif otraLista[0] == mu:                #
                    otraLista=otraLista[1:]             #Mismo procedimiento de la suma con variables, lo
                    if pila1[-1] in Listalet:      #que varia es la operacion a realizar
                        num2= int(buscarILet(pila1[-1])) 
                    elif pila1[-1] in ListaVariable:      
                        num2= int(buscarIL(pila1[-1]))    #
                    else:                               #
                        num2= int(pila1[-1])
                    pila1=pila1[:-1]
                    if pila1[-1] in Listalet:      
                        num1= int(buscarILet(pila1[-1]))
                    elif pila1[-1] in ListaVariable:
                        num1= int(buscarIL(pila1[-1]))
                    else:
                        num1= int(pila1[-1])
                    print(pila1)
                    pila1=pila1[:-1]
                    resultado= num1 * num2
                    pila1.append(resultado)
##-----------------Resta sin variables-------------------------------------------
                elif otraLista[0] == re and  Hay_letra(pila1) == False:
                    otraLista=otraLista[1:]
                    num2= int(pila1[-1])
                    pila1=pila1[:-1]                #Mismo procedimiento de la suma sin variables, lo
                    num1= int(pila1[-1])            #que varia es la operacion a realizar
                    pila1=pila1[:-1]
                    resultado= num1 - num2
                    pila1.append(resultado)
##----------------Resta con variables-------------------------------------------------
                elif otraLista[0] == re:
                    otraLista=otraLista[1:]
                    if pila1[-1] in Listalet:      
                        num2= int(buscarILet(pila1[-1]))
                    elif pila1[-1] in ListaVariable:
                        num2= int(buscarIL(pila1[-1]))            #Mismo procedimiento de la suma con variables, lo
                    else:                                       #que varia es la operacion a realizar
                        num2= int(pila1[-1])
                    pila1=pila1[:-1]
                    if pila1[-1] in Listalet:      
                        num1= int(buscarILet(pila1[-1]))
                    elif pila1[-1] in ListaVariable:
                        num1= int(buscarIL(pila1[-1]))
                    else:
                        num1= int(pila1[-1])
                    pila1=pila1[:-1]
                    resultado= num1 - num2
                    pila1.append(resultado)
##------------------Dividir sin variables----------------------------------------------    
                elif otraLista[0] == di and  Hay_letra(pila1) == False:
                    otraLista=otraLista[1:]
                    num2= int(pila1[-1])            #Mismo procedimiento de la suma sin variables, lo
                    pila1=pila1[:-1]                #que varia es la operacion a realizar
                    num1= int(pila1[-1])
                    pila1=pila1[:-1]
                    resultado= num1 / num2
                    pila1.append(resultado)
##-----------------Dividir con variables----------------------------------------------------
                elif otraLista[0] == di:
                    otraLista=otraLista[1:]
                    if pila1[-1] in Listalet:      
                        num2= int(buscarILet(pila1[-1]))
                    elif pila1[-1] in ListaVariable:
                        num2= int(buscarIL(pila1[-1]))        #Mismo procedimiento de la suma con variables, lo
                    else:                                   #que varia es la operacion a realizar         
                        num2= int(pila1[-1])
                    pila1=pila1[:-1]
                    if pila1[-1] in Listalet:      
                        num1= int(buscarILet(pila1[-1]))
                    elif pila1[-1] in ListaVariable:
                        num1= int(buscarIL(pila1[-1]))
                    else:
                        num1= int(pila1[-1])
                    pila1=pila1[:-1]
                    resultado= num1 / num2
                    pila1.append(resultado)
##-----------------Elevar sin variables----------------------------------------------------
                elif otraLista[0] == ele and Hay_letra(pila1) == False:
                    otraLista=otraLista[1:]
                    num2= int(pila1[-1])
                    pila1=pila1[:-1]
                    num1= int(pila1[-1])            #Mismo procedimiento de la suma sin variables, lo
                    cont=1                          #que varia es la operacion a realizar    
                    base= num1
                    while cont < num2:
                        cont=cont=1
                        num1= num1*base
                    resultado= num1
                    if num2== 0:
                        resultado=1
                    print(resultado)
                    pila1.append(resultado)
##--------------Elevar con variables -----------------------------------------------------------
                elif otraLista[0] == ele :
                    otraLista=otraLista[1:]
                    num2= int(pila1[-1])
                    pila1=pila1[:-1]
                    num1= int(pila1[-1])                #Mismo procedimiento de la suma con variables, lo
                    cont=1                              #que varia es la operacion a realizar
                    base= num1
                    while cont < num2:
                        cont=cont=1
                        num1= num1*base
                    resultado= num1
                    if num2== 0:
                        resultado=1
                    print(resultado)
                    pila1.append(resultado)
##--------------------Terminan las operaciones---------------
            else:
                pila1.append(otraLista[0])
                otraLista=otraLista[1:]

        else:
            if otraLista[0]== su or otraLista[0]== re or otraLista[0]== mu or otraLista[0]== di or otraLista[0]== ele:#operaciones
##----------------Suma sin variables------------------------------------------------------
                if otraLista[0] == su and  Hay_letra(pila1) == False:#Si es suma y no hay variables
                    otraLista=otraLista[1:]#Quita la operacion de la lista
                    num2= int(pila1[-1])#Agarra el ultimo elemento de la lista el cual segundo en la operacion
                    pila1=pila1[:-1]#Quita el numero de la lista
                    num1= int(pila1[-1])#Agarra el ultimo elemento de la lista el cual primero en la operacion
                    pila1=pila1[:-1]#Quita el numero de la lista
                    resultado= num1 + num2 #Hace la operacion
                    pila1.append(resultado)#Anade el resultado a la lista
##---------------Suma con variables----------------------------------------------------------
                elif otraLista[0] == su:#si en la suma alguno de los dos valores son variables
                    otraLista=otraLista[1:]#Quita la operacion de la lista
                    if pila1[-1] in ListaVariable:#Reconoce si la variable esta en la lista de variables
                        print(pila1[-1],"Variable que quiere buscar")
                        num2= int(buscarIL(pila1[-1]))#invoca a buscar que retorna el valor de la variable
                    else:#Si no
                        num2= int(pila1[-1])#Toma el valor que recibio
                    pila1=pila1[:-1]#elima el ultimo elemento
                    if pila1[-1] in ListaVariable:#Reconoce si la variable esta en la lista de variables
                        num1= int(buscarIL(pila1[-1]))#invoca a buscar que retorna el valor de la variable
                    else:#Si no
                        num1= int(pila1[-1])#Toma el valor que recibio
                    pila1=pila1[:-1]#elima el ultimo elemento
                    resultado= num1 + num2#Hace la operacion
                    pila1.append(resultado)#Anade el resultado a la lista
##-----------------Multiplicacion sin variables-------------------------------------------
                elif otraLista[0] == mu and  Hay_letra(pila1) == False: #
                    otraLista=otraLista[1:]                             #Mismo procedimiento de la suma sin variables, lo
                    num2= int(pila1[-1])                                #que varia es la operacion a realiza                                  #
                    pila1=pila1[:-1]                                    #
                    num1= int(pila1[-1])
                    pila1=pila1[:-1]
                    resultado= num1 * num2#Hace la operacion
                    pila1.append(resultado)
##----------------Multiplicacion con variables-----------------------------------------------
                elif otraLista[0] == mu:                #
                    otraLista=otraLista[1:]             #Mismo procedimiento de la suma con variables, lo
                    if pila1[-1] in ListaVariable:      #que varia es la operacion a realizar
                        num2= int(buscarIL(pila1[-1]))    #
                    else:                               #
                        num2= int(pila1[-1])
                    pila1=pila1[:-1]
                    if pila1[-1] in ListaVariable:
                        num1= int(buscarIL(pila1[-1]))
                    else:
                        num1= int(pila1[-1])
                    print(pila1)
                    pila1=pila1[:-1]
                    resultado= num1 * num2
                    pila1.append(resultado)
##-----------------Resta sin variables-------------------------------------------
                elif otraLista[0] == re and  Hay_letra(pila1) == False:
                    otraLista=otraLista[1:]
                    num2= int(pila1[-1])
                    pila1=pila1[:-1]                #Mismo procedimiento de la suma sin variables, lo
                    num1= int(pila1[-1])            #que varia es la operacion a realizar
                    pila1=pila1[:-1]
                    resultado= num1 - num2
                    pila1.append(resultado)
##----------------Resta con variables-------------------------------------------------
                elif otraLista[0] == re:
                    otraLista=otraLista[1:]
                    if pila1[-1] in ListaVariable:
                        num2= int(buscarIL(pila1[-1]))            #Mismo procedimiento de la suma con variables, lo
                    else:                                       #que varia es la operacion a realizar
                        num2= int(pila1[-1])
                    pila1=pila1[:-1]
                    if pila1[-1] in ListaVariable:
                        num1= int(buscarIL(pila1[-1]))
                    else:
                        num1= int(pila1[-1])
                    pila1=pila1[:-1]
                    resultado= num1 - num2
                    pila1.append(resultado)
##------------------Dividir sin variables----------------------------------------------    
                elif otraLista[0] == di and  Hay_letra(pila1) == False:
                    otraLista=otraLista[1:]
                    num2= int(pila1[-1])            #Mismo procedimiento de la suma sin variables, lo
                    pila1=pila1[:-1]                #que varia es la operacion a realizar
                    num1= int(pila1[-1])
                    pila1=pila1[:-1]
                    resultado= num1 / num2
                    pila1.append(resultado)
##-----------------Dividir con variables----------------------------------------------------
                elif otraLista[0] == di:
                    otraLista=otraLista[1:]
                    if pila1[-1] in ListaVariable:
                        num2= int(buscarIL(pila1[-1]))        #Mismo procedimiento de la suma con variables, lo
                    else:                                   #que varia es la operacion a realizar         
                        num2= int(pila1[-1])
                    pila1=pila1[:-1]
                    if pila1[-1] in ListaVariable:
                        num1= int(buscarIL(pila1[-1]))
                    else:
                        num1= int(pila1[-1])
                    pila1=pila1[:-1]
                    resultado= num1 / num2
                    pila1.append(resultado)
##-----------------Elevar sin variables----------------------------------------------------
                elif otraLista[0] == ele and Hay_letra(pila1) == False:
                    otraLista=otraLista[1:]
                    num2= int(pila1[-1])
                    pila1=pila1[:-1]
                    num1= int(pila1[-1])            #Mismo procedimiento de la suma sin variables, lo
                    cont=1                          #que varia es la operacion a realizar    
                    base= num1
                    while cont < num2:
                        cont=cont=1
                        num1= num1*base
                    resultado= num1
                    if num2== 0:
                        resultado=1
                    print(resultado)
                    pila1.append(resultado)
##--------------Elevar con variables -----------------------------------------------------------
                elif otraLista[0] == ele :
                    otraLista=otraLista[1:]
                    num2= int(pila1[-1])
                    pila1=pila1[:-1]
                    num1= int(pila1[-1])                #Mismo procedimiento de la suma con variables, lo
                    cont=1                              #que varia es la operacion a realizar
                    base= num1
                    while cont < num2:
                        cont=cont=1
                        num1= num1*base
                    resultado= num1
                    if num2== 0:
                        resultado=1
                    print(resultado)
                    pila1.append(resultado)
##--------------------Terminan las operaciones---------------
            else:
                pila1.append(otraLista[0])
                otraLista=otraLista[1:]
            
        
    return resultado
###############################################################################################

    
def aceptar_archivo(archivo):
    print(archivo)
    return '.' in archivo and \
           archivo.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('Inicio.html')

############################################################
def lista_imprimir(Lista):
	lista_aux = []
	if Lista == []:
		print("Lista lista")
        else:
		lista_aux.append(Lista[0])
		lista_aux.append(",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,")
		lista_aux.append(Lista[1])
		lista_aux.append(",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,")	
		lista_aux.append(Lista[2])
		Lista = Lista[3:] 	
		lista_para_imprimir.append(lista_aux)
		lista_aux = []
		lista_imprimir(Lista)
	
		
############################################################
@app.route('/Leer', methods=['POST'])
def Leer_Archivo():
    #Obtiene el nombre del archivo cargado
    file = request.files['file']
    if file and aceptar_archivo(file.filename):
        
        filename = secure_filename(file.filename)
        # Mueve el archivo a la carpeta temporal
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        Tokens=[]
    	fo = open("Archivos/"+file.filename, "r+")
    	str = fo.readline()
    	while str !='':
        	Tokens+= str.split()
        	str = fo.readline()
    	print(Tokens)
    	Validar(Tokens)
    	fo.close()
	lista_imprimir(ListaVariable)
	
	return render_template('Vacia.html',lista_para_imprimir=lista_para_imprimir)  


if __name__ == '__main__':
    app.run()
