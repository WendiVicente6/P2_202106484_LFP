class Automata():
    def __init__(self, nombre, alfabeto, simbolos,estados, estado_inicial, estados_aceptacion, transiciones):
        self.nombre = nombre
        self.simbolos=simbolos
        self.estados = estados
        self.alfabeto = alfabeto
        self.estado_inicial = estado_inicial
        self.estados_aceptacion = estados_aceptacion
        self.transiciones = transiciones
    
    def retornar(self):
        return self.nombre,self.alfabeto,self.simbolos,self.estados,self.estado_inicial,self.estados_aceptacion,self.transiciones
            
class Transicion:
    def __init__(self, origen, simbolo_entrada,simbolo_extrae, destino,simbolo_inserta):
        self.origen = origen
        self.entrada = simbolo_entrada
        self.simbolo_entrada=simbolo_entrada
        self.simbolo_extrae=simbolo_extrae
        self.destino = destino
        self.simbolo_inserta=simbolo_inserta
        
    
    def retor(self):
        return self.origen,self.entrada,self.simbolo_entrada,self.simbolo_extrae,self.destino,self.simbolo_inserta
class Node():
    def __init__ (self,dato=None,sig=None):
        self.dato=dato
        self.sig=sig
class Listar():
    def __init__(self):
        self.head=None

    def AgregarFinal(self,dato):
        if not self.head:
            self.head=Node(dato=dato)
            return
        actual=self.head
        while actual.sig:
            actual=actual.sig 
        actual.sig =Node(dato=dato)
           

    def getAutomata(self,afd):
        tmp=self.head
           
        while tmp is not None:
            if tmp.dato.nombre.strip()==afd:
                tmp2=tmp.dato
            tmp=tmp.sig
        return tmp2
    def Mostrar(self):
        tmp=self.head
        tmp2=[]
        while tmp is not None:
            tmp2.append(tmp.dato[0])
            tmp=tmp.sig
        return tmp2
    
    def Operar(self,nombre):
        tmp=self.head
        while tmp is not None:
            if tmp.dato[0]==nombre:
                tmp2=tmp.dato
            tmp=tmp.sig
        return tmp2
