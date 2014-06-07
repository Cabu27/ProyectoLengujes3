import os
from flask import Flask, render_template, request, redirect, url_for, abort, session,send_from_directory ##Se importan las librerias
from werkzeug import secure_filename
app = Flask("SML") 
app.config['UPLOAD_FOLDER'] = 'Archivos/'
app.config['ALLOWED_EXTENSIONS'] = set(['sml'])
##############################################################
    #Listas globales que se utilizan durante la ejecucion del programa

    #Listas globales que se utilizan durante la ejecucion del programa
ListaVariable=[]#Guardara el tipo, variable y el valor para ser retornado al final de la ejecucion
ListaResultados=[]
ListaOperaciones=["+","-","*","**","/","**"]#Contiene las operaciones que se pueden realizar
lista_para_imprimir=[]
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
    ListaVariable.append(var)#Agrega la variable a la lista de variables
    ListaVariable.append(resultado)#Agrega el resultado a la lista de variables
    ListaVariable.append("Int")
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
    cont=0
    resultado=""
    encontrado= False
    while encontrado != True:
        if ListaVariable[cont]==variable:#Si el valor de la lista = a la variable
            resultado=str(ListaVariable[cont+1])#guarda el valor
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
#Funcion que se encarga de identificar el formato de la variable
#ingresa cada variable y su valor en lista variables
#Llama a la funcion validar para determinar el tipo
def Validar(token):
    largo= len(token)-1
    indice=0
    while indice <= largo:
        if token[indice]=="val"  :#Si la variable tiene la sentencia val
            if token[indice+2]=="=":#Valida si el "=" esta separado de la variable
                Variable(token[indice+1],token[indice+3])#Llama a la funcion variable para determinar el tipo
                ListaVariable.append(token[indice+1])#Agrega la variable
                ListaVariable.append(token[indice+3])#Agrega el valor
            else:#Si = esta junto a la variable
                Variable(token[indice+1],token[indice+2])
                ListaVariable.append(token[indice+1])
                ListaVariable.append(token[indice+2])
            indice=indice+1
            
        elif token[indice].isalpha() and not token[indice+2] in ListaVariable :
            #Valida que si la variable fue declarada de forma normal
            if token[indice+1]=="=":
                Variable(token[indice],token[indice+2])
                ListaVariable.append(token[indice])
                ListaVariable.append(token[indice+2])
            else:
                Variable(token[indice],token[indice+1])
                ListaVariable.append(token[indice])
                ListaVariable.append(token[indice+1])
            indice=indice+1
        else:
            indice=indice+1
   
    print(ListaVariable)
    return ListaVariable
####################################################################################################################################
#Identifica el tipo de la variable segun el valor
#Invoca a diferentes funciones segun el valor
def Variable(variable,valor):
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
        elif valor[0]=="T" or valor[0]=="F":#Valida si es un boolean
            ListaVariable.append("Boolean")#Agrega el tipo
        else:
            ##si no entro a las validaciones anteriores se asume que es una operacion
            nuevoValor= list(valor)#Convierte al valor en la lista
            ListaVariable.append("Int")#Agrega el tipo de la operacion
            listaValor=Pegar(nuevoValor)#Invova a la funcion pegar
            newValor= ["("]+listaValor+[")"]#Concatena parentesis al resultado anterios
            resultado=Operaciones(newValor,variable[0])#Invoca a la funcion operaciones que retorna el resultado de la operacion
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
        elif valor[0]=="T" or valor[0]=="F":#Valida si es un boolean
            ListaVariable.append("Boolean")
        else:
            ##si no entro a las validaciones anteriores se asume que es una operacion
            nuevoValor= list(valor)#Convierte al valor en la lista
            ListaVariable.append("Int")#Agrega el tipo de la operacion
            listaValor=Pegar(nuevoValor)#Invova a la funcion pegar
            newValor= ["("]+listaValor+[")"]#Concatena parentesis al resultado anterior
            resultado=Operaciones(newValor,variable)#Invoca a la funcion operaciones que retorna el resultado de la operacion
            
##################################################################################################################################
    
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
