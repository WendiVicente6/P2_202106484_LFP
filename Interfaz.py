from tkinter import END, Entry, Label, Menu, Text, Tk, filedialog, messagebox, ttk,Button,Toplevel,Frame,StringVar
from time import time
import random
from Main import *
   
class VentanaArchivoGLC(Toplevel):
    def __init__(self,master=None):
        super().__init__(master=master)
        
        self.title("CARGAR ARCHIVO AFD")
        self.geometry("500x500")
        inicio=Label(self,text="CARGAR ARCHIVO AFD")
        inicio.pack()
        Frame_AFD2=Frame(self)
        Frame_AFD2.pack()  

        Boton_Cargar_AFD=Button(Frame_AFD2,text="Buscar Archivo",command=lambda:self.AbrirArchivo())
        Boton_Cargar_AFD.pack()
        self.label_file_explorer = Label(Frame_AFD2, text = "File Explorer using Tkinter", width = 100, height = 4, fg = "blue") 
        self.label_file_explorer.pack() 

    def AbrirArchivo(self):
        
        filename = filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes = (("Text files",  "*.glc*"), ("all files", "*.*"))) 
        self.label_file_explorer.configure(text="File Opened:\n "+filename) 
        Cargar_Gramatica(filename)

class VentanaGLC_Arbol(Toplevel):
    def __init__(self,master=None):
        super().__init__(master=master)
        
        self.title("Informacion")
        self.geometry("500x500")
        self.Contenido()
        
    
    def Contenido(self):
        Frame_AFD2=Frame(self)
        Frame_AFD2.pack()   

        combo = ttk.Combobox(Frame_AFD2,state="readonly",values=Mostrar())
        combo.grid(row=6,column=2)

        Boton_GLC=Button(Frame_AFD2,text="Mostrar Información",command=lambda:Arbol_Gramatica(combo.current()))
        Boton_GLC.grid(row=10,column=2)


ventana = Tk()
ventana.title("Proyecto 2 ")
ventana.config(width=400, height=300)
datos=Label(text="Wendi Paulina Vicente Pérez"+"\n"+"Carnet: 202106484")
datos.place(x=100,y=80)
start = time()
 
ventana.after(5000, ventana.destroy)
 
ventana.mainloop()

end = time()



ventana2=Tk()

ventana2.title("Proyecto 2")
ventana2.geometry("700x350")
Datos=Label(text="Wendi Paulina Vicente Pérez"+"\n"+" Carnet: 202106484")
Datos.pack()

notebook=ttk.Notebook(ventana2)
notebook.pack(fill="both",expand="yes")

pes0=ttk.Frame(notebook)
pes1=ttk.Frame(notebook)
notebook.add(pes0,text="Modulo Grámatica Libre de contexto")
notebook.add(pes1,text="Modulo Automatas de pila")
Label(pes0,text="PROYECTO 1 LFP")

Boton=Button(pes0,text="Cargar Archivo",bg="white",width=15,height=5,font="Poppins")
Boton.bind("<Button>",lambda e:VentanaArchivoGLC(pes0))
Boton.grid(row=2,column=0,padx=5,pady=10)
Boton1=Button(pes0,text="Mostrar Información",bg="white",width=15,height=5,font="Poppins")

Boton1.grid(row=2,column=1,padx=5,pady=10)
Boton2=Button(pes0,text="Árbol de derivación",bg="white",width=15,height=5,font="Poppins")
Boton2.bind("<Button>",lambda e:VentanaGLC_Arbol(pes0))
Boton2.grid(row=2,column=2,padx=5,pady=10)


Boton3=Button(pes1,text="Cargar Archivo",bg="white",width=15,height=5,font="Poppins")
Boton3.grid(row=2,column=0,padx=5,pady=10)
Boton4=Button(pes1,text="Mostrar Información",bg="white",width=15,height=5,font="Poppins")
Boton4.grid(row=2,column=1,padx=5,pady=10)
Boton5=Button(pes1,text="Validar Cadena",bg="white",width=15,height=5,font="Poppins")
Boton5.grid(row=2,column=2,padx=5,pady=10)
Boton6=Button(pes1,text="Ruta de Validación",bg="white",width=15,height=5,font="Poppins")
Boton6.grid(row=3,column=0,padx=5,pady=10)
Boton7=Button(pes1,text="Recorrido Paso a Paso",bg="white",width=15,height=5,font="Poppins")
Boton7.grid(row=3,column=1,padx=5,pady=10)
Boton8=Button(pes1,text="De una pasada",bg="white",width=15,height=5,font="Poppins")
Boton8.grid(row=3,column=2,padx=5,pady=10)
ventana2.mainloop()



    
