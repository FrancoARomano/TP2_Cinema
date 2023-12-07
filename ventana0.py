import tkinter as tk
from PIL import ImageTk, Image
import requests, qrcode,base64,random
from io import BytesIO
from datetime import datetime
import os

class Ventana_inicial:
    
    def __init__(self, ventana0, diccionario_cinema: dict) -> None:
        
        """
        inicializa la primera ventana del programa
        """
        self.ventana0=ventana0
        self.ventana0.geometry("500x500+525+150")
        self.ventana0.config(bg="black")
        self.ventana0.title("Lugares")
        
        self.diccionario_cinema=diccionario_cinema

        self.crear_frames()
    
    def crear_frames(self) -> None:
        
        """
        Crea los frames de la primera ventana 
        """
        self.frame_ventana=tk.Frame(self.ventana0, bg="grey", width=400, height=400)
        self.frame_ventana.place(x=50,y=50)
        
        self.crear_etiquetas()
    
    def ir_ventana_1(self, informacion_local: dict) -> None:
        
        """
        cierra la ventana actual y abre la ventana1 
        """
        
        self.informacion_local=informacion_local
        
        self.ventana0.withdraw()
        
        #Constructor que iria a la ventana numero 1
        ventana_principal = tk.Toplevel()
        
        pantallaPrincipal = Pantalla_principal(ventana_principal,self.informacion_local,self.ventana0)
        
    
    def crear_etiquetas(self) -> None:
        
        """
        crea las etiquetas que al clickear sobre ellas ejecutan la funcion ir_ventana_1
        """
        self.etiqueta=tk.Label(self.frame_ventana, text="Seleccione la localidad deseada:", bd=3, font=["Time new Roman",15],bg="grey")
        self.etiqueta.place(x=20,y=20)
        
        fila=0
        columna=0
        for el in self.diccionario_cinema:
            
            texto=self.diccionario_cinema[el]["location"]
            
            self.lugar_boton=tk.Button(self.frame_ventana, text=texto, font=["Arial",14], 
                bg="black",fg="White", bd=7,relief="raised", cursor="hand2",
                command=lambda x=self.diccionario_cinema[el]: self.ir_ventana_1(x))
            
            self.lugar_boton.place(x=15+220*fila,y=105+70*columna)
            
            fila+=1
            if fila==2:
                columna+=1
                fila=0
