from os import system, name
import sys
from tkinter import END, Frame, Label, Menu, Scrollbar, Tk, filedialog, messagebox,Text, ttk

from Gramaticas import Gramatica, Producciones
lista_nombres_Gramatica = []
lista_Gramaticas = []
lista_Automatas = []


error = '''**** ALGO HA SALIDO MAL, INTENTALO DE NUEVO ****'''


selecciona_una_opcion = '''Selecciona una opcion para continuar'''

operacion = '''**** OPERACION REALIZADA CON EXITO ****'''


def Cargar_Gramatica(nom):
    try:
        from itertools import groupby as eliminar_repetidos
        File = open(nom, 'r')
        x = 1
        lista_producciones = []
        lista_terminales = []
        lista_no_terminales = []
        lctxt = False
        for file in File:
            file = file.rstrip('\n')
            if x==1:
                nombre = file
                if (nombre in lista_nombres_Gramatica):
                    messagebox.showerror('Alerta',f'La Gramatica *** {nombre} *** sera saltada debido a que ya existe ...\n')
                    x = '%'
                else:
                    lista_nombres_Gramatica.append(nombre)

            if x==2:
                file = file.replace(' ','')
                le = file.split(",")
                for l in le:
                    lista_no_terminales.append(l)
                
            if x==3:
                la = file.split(',')
                la.sort()
                l = list(lista for lista, _ in eliminar_repetidos(la))
                for listae in lista_no_terminales:
                    for listaa in lista_terminales:
                        if listaa == listae:
                            messagebox.showerror('\nERROR',' No fue posible crear el automata debido a que el alfabeto de entrada contiene simbolos no terminales\n')
                            lista_nombres_Gramatica.remove(nombre)
                            x = '%'
            
            if x==4:
                einic = file
                recorrer = False
                for ee in lista_no_terminales:
                    if einic == ee:
                        recorrer = True
                if recorrer == False:
                    messagebox.showerror('\nERROR','No fue posible crear el automata debido a que el estado inicial no es un no terminal\n')
                    lista_nombres_Gramatica.remove(nombre)
                    x = '%'

                else:
                    einicial = False
                
            if x != '%':
                if x>=5 and file != '%':
                    files = file.split('>')
                    files2 = files[1].split()
                    if len(files2) >= 3:
                        lctxt = True

                    if ((files[0] in lista_no_terminales) and (files[1] in lista_no_terminales)):
                        lctxt = True
                    
                    if (files[0] in lista_terminales) and (files[1] in lista_terminales):
                        lctxt = True

                    if len(files2) == 1 and files2[0] in lista_no_terminales:
                        lctxt = True
                    
                    lista_producciones.append(Producciones(files[0], files2))
            
            if file == '%' and x!="%":
                if lctxt == True:
                    lista_Gramaticas.append(Gramatica(nombre, lista_no_terminales, lista_terminales, einic, lista_producciones))
                    lista_producciones = []
                    lista_terminales = []
                    lista_no_terminales = []
                    x = 0
                    lctxt = False
                else:
                    messagebox.showerror('ERROR',' No fue posible crear una gramatica debido a que la gramatica no es libre de contexto\n')
                    lista_nombres_Gramatica.remove(nombre)
                    lista_producciones = []
                    lista_terminales = []
                    lista_no_terminales = []
                    x = 0

            if file == '%':
                lista_producciones = []
                lista_terminales = []
                lista_no_terminales = []
                x = 0

            if x!='%':
                x+=1
        print(operacion)
        messagebox.showinfo('Información',f'\nLa Gramatica *** {nombre} *** fue cargada con exito ...\n')

    except Exception:
        e = sys.exc_info()[1]
        print(e.args[0])
        messagebox.showerror(error)


def Mostrar():
    lista=[]
    for x in lista_nombres_Gramatica:
        lista.append(x)
    return lista

def Arbol_Gramatica(resp):
    z = False
    while not z:

            if resp in lista_nombres_Gramatica:
                j = lista_nombres_Gramatica(resp)
                resp = j+1
            if resp !='-1' and int(resp)>=0:
                from graphviz import Graph

                dot = Graph(name='GramaticaLC', encoding='utf-8', format='png')

                dot.attr(rankdir='TB', layout='dot', shape='none')

                numero = -1
                listaP = []
                indice = 0
                aux = 0
                lista_Nodos = []
                r_2 = int(resp)-1
                for nodo in lista_Gramaticas[r_2].producciones:
                    aux = 0
                    if lista_Nodos[:] != []:
                        for x in lista_Nodos:
                            if nodo.origen == x:
                                indice = aux
                            aux+=1
                    else:
                        numero+=1
                        dot.node(name='nodo'+str(numero), label=nodo.origen, shape='none')
                        lista_Nodos.append(nodo.origen)
                    
                    for y in nodo.destinos:
                        numero +=1
                        dot.node(name='nodo'+str(numero), label=y, shape='none')
                        listaP.append(numero)
                        lista_Nodos.append(y)
                    for z in listaP:
                        dot.edge('nodo'+str(indice), 'nodo'+str(z))
                    listaP = []
                    aux = 0
                dot.render('GramaticasLC/'+lista_Gramaticas[r_2].nombre, format='png' ,view=True)

            else:
                z = True

def MostrarInformacion(resp):
    z = False
    while not z:

        if resp in lista_nombres_Gramatica:
            j = lista_nombres_Gramatica(resp)
            resp = j+1
        if resp !='-1' and int(resp)>=0:
            linea=''
            c=('Nombre: '+lista_Gramaticas[int(resp)-1].nombre)
            c+='\nNo Terminales'
            for a in lista_Gramaticas[int(resp)-1].no_terminales:
                linea=linea+''.join(a)+','
            linea=linea[:-1]    
            c+=linea
            c+='\nTerminales'
            linea=''
            for a in lista_Gramaticas[int(resp)-1].terminales:
                linea=linea+''.join(a)+','
            linea=linea[:-1]
            c+=linea
            c+='\nNo terminal inicial'
            linea=''
            linea=lista_Gramaticas[int(resp)-1].nti
            c+=linea+'\n'
            c+='Producciones'
            gramatica=lista_Gramaticas[int(resp)-1].nti
            entrar=True
            gram1=''
            gram2=''
            for a in lista_Gramaticas[int(resp)-1].no_terminales:
                if a == gramatica:
                    for b in lista_Gramaticas[int(resp)-1].producciones:
                        if a ==b.origen:      
                            destinos=""
                            for d in b.destinos:
                                destinos=destinos+"".join(d)+""
                            if entrar==True:

                                gram1=gram2+''+a+'>'+str(destinos)
                                entrar=False            
                            else:
                                gram1=gram1+'\n'+'|'+str(destinos)
                    entrar=True
                else:
                    for b in lista_Gramaticas[int(resp)-1].producciones:
                        if a==b.origen:
                            destinos=""
                            for d in b.destinos:
                                destinos=destinos+"".join(d)+""
                            if entrar==True:
                                gram2=gram2+''+b.origen+'>'+str(destinos)+'\n'
                                entrar=False
                            else:
                                gram2=gram2+'|'+str(destinos)+'\n'
                    entrar=True
            c=c+'\n'+gram1+'\n'+gram2
            return c
        else:
            z=True



