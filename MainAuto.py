from tkinter import END, Frame, Label, Menu, Scrollbar, Tk, filedialog, messagebox,Text, ttk
from Automata import *
from graphviz import Digraph
import os
Lista_Automata=Listar()

def Automata_Pila_Archivo(nombre,alfa,Simbolo_Pila,Estados,estado_ini,estados_aceptacion,transiciones):
    lista_automatas = [] 
    alfabeto=alfa
    estado_inicial=estado_ini
    

    
    alfabeto_ = alfabeto.split(",")
    sim_Pila=Simbolo_Pila.split(",")
    estados_ = Estados.split(",") 
    estados_aceptacion_ = estados_aceptacion.split(",")
    transi=transiciones.replace(" ","")
    transiciones_ = transi.split(";") 

    if(not estado_inicial in estados_ and not estados_aceptacion_ in estados_):
        messagebox.showinfo("Error de archivo","VERIFICAR QUE EL ESTADO INICIAL O ESTADO DE ACEPTACION ESTÉ EN EL CONJUNTO DE ESTADOS");
    
    else:

        for estado in Estados:
            if(estado in alfabeto_):
                messagebox.showinfo("Advertencia"+"El alfabeto no puede ser parte de los estados")
                break
        
        # creacion de transiciones por separado
        transiciones__ = []
        for t in transiciones_:
            t = t.split(",")
            '''if(not t[0] in estados_ or not t[2] in estados_):
                messagebox.showinfo("Advertencia","El origen o el destino de una transicion no esta en el conjunto de estados")
                break'''
            Clase_Transiciones=Transicion(t[0], t[1], t[2],t[3],t[4])
            transiciones__.append(Clase_Transiciones.retor())

        Clase_automata = Automata(nombre, alfabeto_,sim_Pila,estados_, estado_inicial, estados_aceptacion_, transiciones__)
        automata=Clase_automata.retornar()
        Lista_Automata.AgregarFinal(automata)
        lista_automatas.append(automata)
        
        print("Automatas ingresados: ")
        for automata in lista_automatas:
            print(automata)

def GrafoAFD(seleccion):
    Automata=Lista_Automata.Operar(seleccion)
    dot=Digraph(name="Gramatica",encoding='UTF-8',format='pdf',filename='Gramaticas')
    dot.attr(rankdir='LR',layout='dot',shape='circle')
    for ea in Automata[3]:
        if ea in Automata[5]:
            dot.node(name=ea,shape='doublecircle')
        else:
            dot.node(name=ea,shape='circle')
    dot.node('Inicio',shape='plaintext')

    dot.edge('Inicio',''+Automata[4])
    Tran=""
    for es in Automata[6]:
        dot.edge(''+es[0],''+es[4],label=es[1]+','+es[3]+','+es[5])
        Tran=Tran+"\n"+es[0]+","+es[1]+","+es[3]+";"+es[4]+","+es[5]


    Datos="Nombre: "+Automata[0]+"\n"+"Alfabeto de pila: "+",".join(Automata[1])+"\n"+"Estados: "+",".join(Automata[3])+"\n"+"Estado Inicial: "+Automata[4]+"\n"+"Estados de aceptación: "+",".join(Automata[5])+"\n"+"Transiciones:"+Tran

    dot.node(Datos,shape='box')
    dot.render(Automata[0],format='pdf',view=True)

def Cadena(cadena,seleccion):
    Automata=Lista_Automata.Operar(seleccion)
    estado=0
    tran=0
    origenes=[]
    pila=[]
    cant_pila=0
    contar_cadena=0
    for caracter in cadena:
        contar_cadena+=1
        
        if(caracter in Automata[1]):
                if estado==0:
                    if caracter in Automata[6][tran]:
                        if caracter==Automata[6][tran][1]:#Lee entrada
                            if Automata[6][tran][3]!="$":#extraer
                                if len(pila)==0:
                                    print("No se puede extraer nada, por lo tanto no es valido")
                                else:
                                    if pila[cant_pila]==Automata[6][tran][3]:
                                        pila.remove(Automata[6][tran][3])
                                        print("Se extrajo"+Automata[6][tran][3])
                            elif Automata[6][tran][5]!="$":#inserta
                                pila.append(Automata[6][tran][5])
                                cant_pila+=1
                            origenes.insert(0,tran)
                            estado+=1
                            tran=0
                        else:
                            origenes.insert(0,tran)
                            estado+=1
                            tran=0
                        continue
                    elif caracter not in Automata[6][tran]:
                        if Automata[6][tran][1]=="$":
                            if caracter==Automata[6][tran][1]:#Lee entrada
                                if Automata[6][tran][3]!="$":#extraer
                                    if len(pila)==0:
                                        print("No se puede extraer nada, por lo tanto no es valido")
                                    else:
                                        if pila[0]==Automata[6][tran][3]:
                                            pila.remove(Automata[6][tran][3])
                                            print("Se extrajo"+Automata[6][tran][3])
                            elif Automata[6][tran][5]!="$":#inserta
                                if Automata[6][tran][5]==Automata[6][tran][5]:
                                    pila.append(Automata[6][tran][5])
                                    cant_pila+=1
                                    origenes.insert(0,tran)
                                    tran+=1
                                    if caracter==Automata[6][tran][1]:#Lee entrada
                                        if Automata[6][tran][3]!="$":#extraer
                                            if len(pila)==0:
                                                print("No se puede extraer nada, por lo tanto no es valido")
                                            else:
                                                if pila[cant_pila]==Automata[6][tran][3]:
                                                    pila.remove(Automata[6][tran][3])
                                                    print("Se extrajo"+Automata[6][tran][3])
                                        elif Automata[6][tran][5]!="$":#inserta
                                            pila.append(Automata[6][tran][5])
                                            cant_pila+=1
                                        origenes.insert(0,tran)
                                        estado+=1
                                        tran=0
                                    else:
                                        print("No es aceptado")
                                    continue
                                    
                        else:#--------------
                            origenes.insert(0,tran)
                            estado+=1
                            tran=0
                        
                    else:
                        while caracter not in Automata[6][tran] or tran>=len(Automata[6]): #Buscar Transicion
                            tran+=1
                        if Automata[6][tran][0] in Automata[4]:#Estado inicial
                            if caracter==Automata[6][tran][1]:#Lee entrada
                                if Automata[6][tran][3]!="$":#extraer
                                    if len(pila)==0:
                                        print("No se puede extraer nada, por lo tanto no es valido")
                                    else:
                                        if pila[cant_pila]==Automata[6][tran][3]:
                                            pila.remove(Automata[6][tran][3])
                                            print("Se extrajo"+Automata[6][tran][3])
                            elif Automata[6][tran][5]!="$":#inserta
                                pila.append(Automata[6][tran][5])
                                cant_pila+=1
                            origenes.insert(0,tran)
                            estado+=1
                            tran=0
                        else:
                            origenes.insert(0,tran)
                            estado+=1
                            tran=0
                        
                elif estado!=0:
                    
                        while Automata[6][origenes[0]][4]!=Automata[6][tran][0] or not caracter in Automata[6][tran]:#Buscar Transicion
                            tran+=1
                        if caracter==Automata[6][tran][1]:#Lee entrada
                            if Automata[6][tran][3]!="$":#extraer
                                if len(pila)==0:
                                    print("No se puede extraer nada, por lo tanto no es valido")
                                else:
                                    if pila[len(pila)-1]==Automata[6][tran][3]:
                                        pila.remove(Automata[6][tran][3])
                                        print("Se extrajo"+Automata[6][tran][3])
                                       
                            elif Automata[6][tran][5]!="$":#inserta
                                pila.append(Automata[6][tran][5])
                                cant_pila+=1
                            origenes.insert(0,tran)
                            estado+=1
                            tran=0
                            continue 
                        
                            
                else:
                    print("No puede ser aceptado")
                    break
        else:
            messagebox.showinfo("Información","Revisar entrada... un caracter no pertenece al alfabeto")
    if pila[0] in Automata[2] and len(pila)==1:
        try:
            while Automata[6][origenes[0]][4]!=Automata[6][tran][0] or not pila[0] in Automata[6][tran]:#Buscar Transicion
                tran+=1
            if Automata[6][tran][3]!="$":#extraer
                if len(pila)==0:
                    print("No se puede extraer nada, por lo tanto no es valido")
                else:
                    if pila[len(pila)-1]==Automata[6][tran][3]:
                        pila.remove(Automata[6][tran][3])
                        print("Se extrajo"+Automata[6][tran][3])
                        
            elif Automata[6][tran][5]!="$":#inserta
                pila.append(Automata[6][tran][5])
                cant_pila+=1
            origenes.insert(0,tran)
            estado+=1
            tran=0
            messagebox.showinfo("Informacion","Es aceptado")
        
        except:
            messagebox.showinfo("Informacion","No es aceptado")
    else:
            messagebox.showinfo("Información","No es aceptado")
    
def Cadena_Ruta(cadena,seleccion):
    Automata=Lista_Automata.Operar(seleccion)
    estado=0
    tran=0
    origenes=[]
    pila=[]
    Ruta=[]
    cant_pila=0
    contar_cadena=0
    for caracter in cadena:
        contar_cadena+=1
        
        if(caracter in Automata[1]):
                if estado==0:
                    if caracter in Automata[6][tran]:
                        if caracter==Automata[6][tran][1]:#Lee entrada
                            if Automata[6][tran][3]!="$":#extraer
                                if len(pila)==0:
                                    print("No se puede extraer nada, por lo tanto no es valido")
                                else:
                                    if pila[cant_pila]==Automata[6][tran][3]:
                                        pila.remove(Automata[6][tran][3])
                                        Ruta.append(Automata[6][tran][0]+","+(Automata[6][tran][1])+","+(Automata[6][tran][3])+";"+(Automata[6][tran][5])+","+(Automata[6][tran][4]))

                                        print("Se extrajo"+Automata[6][tran][3])
                            elif Automata[6][tran][5]!="$":#inserta
                                pila.append(Automata[6][tran][5])
                                Ruta.append(Automata[6][tran][0]+","+(Automata[6][tran][1])+","+(Automata[6][tran][3])+";"+(Automata[6][tran][5])+","+(Automata[6][tran][4]))

                                cant_pila+=1
                            origenes.insert(0,tran)
                            estado+=1
                            tran=0
                        else:
                            origenes.insert(0,tran)
                            estado+=1
                            tran=0
                        continue
                    elif caracter not in Automata[6][tran]:
                        if Automata[6][tran][1]=="$":
                            if caracter==Automata[6][tran][1]:#Lee entrada
                                if Automata[6][tran][3]!="$":#extraer
                                    if len(pila)==0:
                                        print("No se puede extraer nada, por lo tanto no es valido")
                                    else:
                                        if pila[0]==Automata[6][tran][3]:
                                            pila.remove(Automata[6][tran][3])
                                            Ruta.append(Automata[6][tran][0]+","+(Automata[6][tran][1])+","+(Automata[6][tran][3])+";"+(Automata[6][tran][5])+","+(Automata[6][tran][4]))

                                            print("Se extrajo"+Automata[6][tran][3])

                            elif Automata[6][tran][5]!="$":#inserta
                                if Automata[6][tran][5]==Automata[6][tran][5]:
                                    pila.append(Automata[6][tran][5])
                                    Ruta.append(Automata[6][tran][0]+","+(Automata[6][tran][1])+","+(Automata[6][tran][3])+";"+(Automata[6][tran][5])+","+(Automata[6][tran][4]))
                                    cant_pila+=1
                                    origenes.insert(0,tran)
                                    tran+=1
                                    if caracter==Automata[6][tran][1]:#Lee entrada
                                        if Automata[6][tran][3]!="$":#extraer
                                            if len(pila)==0:
                                                print("No se puede extraer nada, por lo tanto no es valido")
                                            else:
                                                if pila[cant_pila]==Automata[6][tran][3]:
                                                    pila.remove(Automata[6][tran][3])
                                                    Ruta.append(Automata[6][tran][0]+","+(Automata[6][tran][1])+","+(Automata[6][tran][3])+";"+(Automata[6][tran][5])+","+(Automata[6][tran][4]))

                                                    print("Se extrajo"+Automata[6][tran][3])
                                        elif Automata[6][tran][5]!="$":#inserta
                                            pila.append(Automata[6][tran][5])
                                            Ruta.append(Automata[6][tran][0]+","+(Automata[6][tran][1])+","+(Automata[6][tran][3])+";"+(Automata[6][tran][5])+","+(Automata[6][tran][4]))

                                            cant_pila+=1
                                        origenes.insert(0,tran)
                                        estado+=1
                                        tran=0
                                    else:
                                        print("No es aceptado")
                                    continue
                                    
                        else:#--------------
                            origenes.insert(0,tran)
                            estado+=1
                            tran=0
                        
                    else:
                        while caracter not in Automata[6][tran] or tran>=len(Automata[6]): #Buscar Transicion
                            tran+=1
                        if Automata[6][tran][0] in Automata[4]:#Estado inicial
                            if caracter==Automata[6][tran][1]:#Lee entrada
                                if Automata[6][tran][3]!="$":#extraer
                                    if len(pila)==0:
                                        print("No se puede extraer nada, por lo tanto no es valido")
                                    else:
                                        if pila[cant_pila]==Automata[6][tran][3]:
                                            pila.remove(Automata[6][tran][3])
                                            print("Se extrajo"+Automata[6][tran][3])
                                            Ruta.append(Automata[6][tran][0]+","+(Automata[6][tran][1])+","+(Automata[6][tran][3])+";"+(Automata[6][tran][5])+","+(Automata[6][tran][4]))

                            elif Automata[6][tran][5]!="$":#inserta
                                pila.append(Automata[6][tran][5])
                                Ruta.append(Automata[6][tran][0]+","+(Automata[6][tran][1])+","+(Automata[6][tran][3])+";"+(Automata[6][tran][5])+","+(Automata[6][tran][4]))

                                cant_pila+=1
                            origenes.insert(0,tran)
                            estado+=1
                            tran=0
                        else:
                            origenes.insert(0,tran)
                            estado+=1
                            tran=0
                        
                elif estado!=0:
                    
                        while Automata[6][origenes[0]][4]!=Automata[6][tran][0] or not caracter in Automata[6][tran]:#Buscar Transicion
                            tran+=1
                        if caracter==Automata[6][tran][1]:#Lee entrada
                            if Automata[6][tran][3]!="$":#extraer
                                if len(pila)==0:
                                    print("No se puede extraer nada, por lo tanto no es valido")
                                else:
                                    if pila[len(pila)-1]==Automata[6][tran][3]:
                                        pila.remove(Automata[6][tran][3])
                                        Ruta.append(Automata[6][tran][0]+","+(Automata[6][tran][1])+","+(Automata[6][tran][3])+";"+(Automata[6][tran][5])+","+(Automata[6][tran][4]))

                                        print("Se extrajo"+Automata[6][tran][3])
                                       
                            elif Automata[6][tran][5]!="$":#inserta
                                pila.append(Automata[6][tran][5])
                                Ruta.append(Automata[6][tran][0]+","+(Automata[6][tran][1])+","+(Automata[6][tran][3])+";"+(Automata[6][tran][5])+","+(Automata[6][tran][4]))

                                cant_pila+=1
                            origenes.insert(0,tran)
                            estado+=1
                            tran=0
                            continue 
                        
                            
                else:
                    print("No puede ser aceptado")
                    break
        else:
            messagebox.showinfo("Información","Revisar entrada... un caracter no pertenece al alfabeto")
    if pila[0] in Automata[2] and len(pila)==1:
        try:
            while Automata[6][origenes[0]][4]!=Automata[6][tran][0] or not pila[0] in Automata[6][tran]:#Buscar Transicion
                tran+=1
            if Automata[6][tran][3]!="$":#extraer
                if len(pila)==0:
                    print("No se puede extraer nada, por lo tanto no es valido")
                else:
                    if pila[len(pila)-1]==Automata[6][tran][3]:
                        pila.remove(Automata[6][tran][3])
                        Ruta.append(Automata[6][tran][0]+","+(Automata[6][tran][1])+","+(Automata[6][tran][3])+";"+(Automata[6][tran][5])+","+(Automata[6][tran][4]))

                        print("Se extrajo"+Automata[6][tran][3])
                        
            elif Automata[6][tran][5]!="$":#inserta
                pila.append(Automata[6][tran][5])
                Ruta.append(Automata[6][tran][0]+","+(Automata[6][tran][1])+","+(Automata[6][tran][3])+";"+(Automata[6][tran][5])+","+(Automata[6][tran][4]))

                cant_pila+=1
            origenes.insert(0,tran)
            estado+=1
            tran=0
            MensajeRuta="\n".join(Ruta)
            messagebox.showinfo("Ruta",MensajeRuta)
        
        except:
            messagebox.showinfo("Informacion","No es aceptado")
    else:
            messagebox.showinfo("Información","No es aceptado")

def Cadena_Pasada(cadena,seleccion):
    f = open('Pasada.dot','w')
    etiqueta = '''digraph html{ \n abc [shape=none, margin=0,label=<
        <table BORDER="1" CELLBORDER="1" CELLSPACING="0">
        <tr>
            <td>Iteración</td>
            <td>Pila</td>
            <td>Entrada</td>
            <td>Transición</td>
        </tr>'''



        
    Automata=Lista_Automata.Operar(seleccion)
    estado=0
    tran=0
    origenes=[]
    pila=[]
    Ruta=[]
    transicion=0
    cant_pila=0
    contar_cadena=0
    for caracter in cadena:
        contar_cadena+=1
        
        if(caracter in Automata[1]):
                if estado==0:
                    if caracter in Automata[6][tran]:
                        if caracter==Automata[6][tran][1]:#Lee entrada
                            if Automata[6][tran][3]!="$":#extraer
                                if len(pila)==0:
                                    print("No se puede extraer nada, por lo tanto no es valido")
                                else:
                                    if pila[cant_pila]==Automata[6][tran][3]:
                                        pila.remove(Automata[6][tran][3])
                                        Ruta.append(Automata[6][tran][0]+","+(Automata[6][tran][1])+","+(Automata[6][tran][3])+";"+(Automata[6][tran][5])+","+(Automata[6][tran][4]))
                                        transicion+=1
                                        MensajeRuta="\n".join(Ruta)
                                        Pilas="".join(pila)

                                        etiqueta += '<tr><td>' + str(transicion) + '</td><td>' + str(Pilas) + '</td><td>' + str(caracter) + '</td><td>' + str(Automata[6][tran]) + '</td></tr>'

                            elif Automata[6][tran][5]!="$":#inserta
                                pila.append(Automata[6][tran][5])
                                Ruta.append(Automata[6][tran][0]+","+(Automata[6][tran][1])+","+(Automata[6][tran][3])+";"+(Automata[6][tran][5])+","+(Automata[6][tran][4]))
                                transicion+=1
                                MensajeRuta="\n".join(Ruta)
                                Pilas="".join(pila)

                                etiqueta += '<tr><td>' + str(transicion) + '</td><td>' + str(Pilas) + '</td><td>' + str(caracter) + '</td><td>' + str(Automata[6][tran]) + '</td></tr>'

                                cant_pila+=1
                            origenes.insert(0,tran)
                            estado+=1
                            tran=0
                        else:
                            origenes.insert(0,tran)
                            estado+=1
                            tran=0
                            transicion+=1
                            MensajeRuta="\n".join(Ruta)
                            Pilas="".join(pila)

                            etiqueta += '<tr><td>' + str(transicion) + '</td><td>' + str(Pilas) + '</td><td>' + str(caracter) + '</td><td>' + str(Automata[6][tran]) + '</td></tr>'

                        continue
                    elif caracter not in Automata[6][tran]:
                        if Automata[6][tran][1]=="$":
                            if caracter==Automata[6][tran][1]:#Lee entrada
                                if Automata[6][tran][3]!="$":#extraer
                                    if len(pila)==0:
                                        print("No se puede extraer nada, por lo tanto no es valido")
                                    else:
                                        if pila[0]==Automata[6][tran][3]:
                                            pila.remove(Automata[6][tran][3])
                                            Ruta.append(Automata[6][tran][0]+","+(Automata[6][tran][1])+","+(Automata[6][tran][3])+";"+(Automata[6][tran][5])+","+(Automata[6][tran][4]))
                                            transicion+=1
                                            MensajeRuta="\n".join(Ruta)
                                            Pilas="".join(pila)

                                            etiqueta += '<tr><td>' + str(transicion) + '</td><td>' + str(Pilas) + '</td><td>' + str(caracter) + '</td><td>' + str(Automata[6][tran]) + '</td></tr>'

                                            print("Se extrajo"+Automata[6][tran][3])

                            elif Automata[6][tran][5]!="$":#inserta
                                if Automata[6][tran][5]==Automata[6][tran][5]:
                                    pila.append(Automata[6][tran][5])
                                    Ruta.append(Automata[6][tran][0]+","+(Automata[6][tran][1])+","+(Automata[6][tran][3])+";"+(Automata[6][tran][5])+","+(Automata[6][tran][4]))
                                    cant_pila+=1
                                    transicion+=1
                                    MensajeRuta="\n".join(Ruta)
                                    Pilas="".join(pila)

                                    etiqueta += '<tr><td>' + str(transicion) + '</td><td>' + str(Pilas) + '</td><td>' + str("") + '</td><td>' + str(Automata[6][tran]) + '</td></tr>'

                                    origenes.insert(0,tran)
                                    tran+=1
                                    if caracter==Automata[6][tran][1]:#Lee entrada
                                        if Automata[6][tran][3]!="$":#extraer
                                            if len(pila)==0:
                                                print("No se puede extraer nada, por lo tanto no es valido")
                                            else:
                                                if pila[cant_pila]==Automata[6][tran][3]:
                                                    pila.remove(Automata[6][tran][3])
                                                    Ruta.append(Automata[6][tran][0]+","+(Automata[6][tran][1])+","+(Automata[6][tran][3])+";"+(Automata[6][tran][5])+","+(Automata[6][tran][4]))
                                                    transicion+=1
                                                    MensajeRuta="\n".join(Ruta)
                                                    Pilas="".join(pila)

                                                    etiqueta += '<tr><td>' + str(transicion) + '</td><td>' + str(Pilas) + '</td><td>' + str(caracter) + '</td><td>' + str(Automata[6][tran]) + '</td></tr>'

                                                    print("Se extrajo"+Automata[6][tran][3])
                                        elif Automata[6][tran][5]!="$":#inserta
                                            pila.append(Automata[6][tran][5])
                                            Ruta.append(Automata[6][tran][0]+","+(Automata[6][tran][1])+","+(Automata[6][tran][3])+";"+(Automata[6][tran][5])+","+(Automata[6][tran][4]))
                                            transicion+=1
                                            MensajeRuta="\n".join(Ruta)
                                            Pilas="".join(pila)

                                            etiqueta += '<tr><td>' + str(transicion) + '</td><td>' + str(Pilas) + '</td><td>' + str(caracter) + '</td><td>' + str(Automata[6][tran]) + '</td></tr>'

                                            cant_pila+=1
                                        origenes.insert(0,tran)
                                        estado+=1
                                        tran=0
                                    else:
                                        print("No es aceptado")
                                    continue
                                    
                        else:#--------------
                            origenes.insert(0,tran)
                            estado+=1
                            tran=0
                            transicion+=1
                            MensajeRuta="\n".join(Ruta)
                            Pilas="".join(pila)

                            etiqueta += '<tr><td>' + str(transicion) + '</td><td>' + str(Pilas) + '</td><td>' + str(caracter) + '</td><td>' + str(Automata[6][tran]) + '</td></tr>'

                        
                    else:
                        while caracter not in Automata[6][tran] or tran>=len(Automata[6]): #Buscar Transicion
                            tran+=1
                        if Automata[6][tran][0] in Automata[4]:#Estado inicial
                            if caracter==Automata[6][tran][1]:#Lee entrada
                                if Automata[6][tran][3]!="$":#extraer
                                    if len(pila)==0:
                                        print("No se puede extraer nada, por lo tanto no es valido")
                                    else:
                                        if pila[cant_pila]==Automata[6][tran][3]:
                                            pila.remove(Automata[6][tran][3])
                                            print("Se extrajo"+Automata[6][tran][3])
                                            Ruta.append(Automata[6][tran][0]+","+(Automata[6][tran][1])+","+(Automata[6][tran][3])+";"+(Automata[6][tran][5])+","+(Automata[6][tran][4]))
                                            transicion+=1
                                            MensajeRuta="\n".join(Ruta)
                                            Pilas="".join(pila)

                                            etiqueta += '<tr><td>' + str(transicion) + '</td><td>' + str(Pilas) + '</td><td>' + str(caracter) + '</td><td>' + str(Automata[6][tran]) + '</td></tr>'

                            elif Automata[6][tran][5]!="$":#inserta
                                pila.append(Automata[6][tran][5])
                                Ruta.append(Automata[6][tran][0]+","+(Automata[6][tran][1])+","+(Automata[6][tran][3])+";"+(Automata[6][tran][5])+","+(Automata[6][tran][4]))
                                transicion+=1
                                MensajeRuta="\n".join(Ruta)
                                Pilas="".join(pila)

                                etiqueta += '<tr><td>' + str(transicion) + '</td><td>' + str(Pilas) + '</td><td>' + str(caracter) + '</td><td>' + str(Automata[6][tran]) + '</td></tr>'

                                cant_pila+=1
                            origenes.insert(0,tran)
                            estado+=1
                            tran=0
                        else:
                            origenes.insert(0,tran)
                            estado+=1
                            tran=0
                            transicion+=1
                            MensajeRuta="\n".join(Ruta)
                            Pilas="".join(pila)

                            etiqueta += '<tr><td>' + str(transicion) + '</td><td>' + str(Pilas) + '</td><td>' + str(caracter) + '</td><td>' + str(Automata[6][tran]) + '</td></tr>'

                        
                elif estado!=0:
                    
                        while Automata[6][origenes[0]][4]!=Automata[6][tran][0] or not caracter in Automata[6][tran]:#Buscar Transicion
                            tran+=1
                        if caracter==Automata[6][tran][1]:#Lee entrada
                            if Automata[6][tran][3]!="$":#extraer
                                if len(pila)==0:
                                    print("No se puede extraer nada, por lo tanto no es valido")
                                else:
                                    if pila[len(pila)-1]==Automata[6][tran][3]:
                                        pila.remove(Automata[6][tran][3])
                                        Ruta.append(Automata[6][tran][0]+","+(Automata[6][tran][1])+","+(Automata[6][tran][3])+";"+(Automata[6][tran][5])+","+(Automata[6][tran][4]))
                                        transicion+=1
                                        MensajeRuta="\n".join(Ruta)
                                        Pilas="".join(pila)

                                        etiqueta += '<tr><td>' + str(transicion) + '</td><td>' + str(Pilas) + '</td><td>' + str(caracter) + '</td><td>' + str(Automata[6][tran]) + '</td></tr>'

                                        print("Se extrajo"+Automata[6][tran][3])
                                       
                            elif Automata[6][tran][5]!="$":#inserta
                                pila.append(Automata[6][tran][5])
                                Ruta.append(Automata[6][tran][0]+","+(Automata[6][tran][1])+","+(Automata[6][tran][3])+";"+(Automata[6][tran][5])+","+(Automata[6][tran][4]))
                                transicion+=1
                                MensajeRuta="\n".join(Ruta)
                                Pilas="".join(pila)

                                etiqueta += '<tr><td>' + str(transicion) + '</td><td>' + str(Pilas) + '</td><td>' + str(caracter) + '</td><td>' + str(Automata[6][tran]) + '</td></tr>'

                                cant_pila+=1
                            origenes.insert(0,tran)
                            estado+=1
                            tran=0
                            continue 
                        
                            
                else:
                    print("No puede ser aceptado")
                    break
        else:
            messagebox.showinfo("Información","Revisar entrada... un caracter no pertenece al alfabeto")
    if pila[0] in Automata[2] and len(pila)==1:
        try:
            while Automata[6][origenes[0]][4]!=Automata[6][tran][0] or not pila[0] in Automata[6][tran]:#Buscar Transicion
                tran+=1
            if Automata[6][tran][3]!="$":#extraer
                if len(pila)==0:
                    print("No se puede extraer nada, por lo tanto no es valido")
                else:
                    if pila[len(pila)-1]==Automata[6][tran][3]:
                        pila.remove(Automata[6][tran][3])
                        Ruta.append(Automata[6][tran][0]+","+(Automata[6][tran][1])+","+(Automata[6][tran][3])+";"+(Automata[6][tran][5])+","+(Automata[6][tran][4]))
                        transicion+=1
                        MensajeRuta="\n".join(Ruta)
                        Pilas="".join(pila)

                        etiqueta += '<tr><td>' + str(transicion) + '</td><td>' + str(Pilas) + '</td><td>' + str("") + '</td><td>' + str(Automata[6][tran]) + '</td></tr>'

                        print("Se extrajo"+Automata[6][tran][3])
                        
            elif Automata[6][tran][5]!="$":#inserta
                pila.append(Automata[6][tran][5])
                Ruta.append(Automata[6][tran][0]+","+(Automata[6][tran][1])+","+(Automata[6][tran][3])+";"+(Automata[6][tran][5])+","+(Automata[6][tran][4]))
                transicion+=1
                MensajeRuta="\n".join(Ruta)
                Pilas="".join(pila)

                etiqueta += '<tr><td>' + str(transicion) + '</td><td>' + str(Pilas) + '</td><td>' + str("") + '</td><td>' + str(Automata[6][tran]) + '</td></tr>'

                cant_pila+=1
            origenes.insert(0,tran)
            estado+=1
            tran=0
            MensajeRuta="\n".join(Ruta)
        
        except:
            messagebox.showinfo("Informacion","No es aceptado")
    else:
            messagebox.showinfo("Información","No es aceptado")
    etiqueta += '</table>>];}'
    f.write(etiqueta)
    f.close()
    os.system('dot -Tpdf Pasada.dot -o Pasada.pdf')
    os.startfile("Pasada.pdf")
