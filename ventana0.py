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

class Pantalla_principal:
    
    def __init__(self, master,informacion_local: dict,ventana0) -> None:
        
        """
        se abre una la ventana1, que sería la cartelera
        """
        self.master = master
        self.master.geometry("900x900")
        self.master.title("Pantalla Principal")
        self.master.config(bg = "light gray")
        self.master.resizable(False, False)
        
        self.ventana0=ventana0
        
        self.informacion_local=informacion_local
        
        self.lista_id_imagenes = self.funcion_id_imagenes(self.informacion_local)
        
        self.creador_marcos(self.informacion_local)
        self.buscador_con_boton(self.informacion_local, self.lista_id_imagenes)
        self.creacion_botones(self.lista_id_imagenes)
    
    def creador_marcos(self, informacion_local: dict):
        
        """
        se crean los frames para luego crear canvas dentro de algunos de ellos
        """
        lista_contenedores = []
        
        fila = 0
        columna = 0
        
        for _ in range(9):
                
            self.contenedores = tk.Frame(self.master, bg = "light gray", width = 300, height = 260)
            
            self.contenedores.grid(row = fila, column = columna)
            
            lista_contenedores.append(self.contenedores)
            
            columna += 1
            
            if fila == 0 and columna == 3:
                
                fila = 1
                columna = 0
            
            elif fila == 1 and columna == 3:
                
                fila = 2 
                columna = 0
            
        self.creador_canvas_imagenes(lista_contenedores, informacion_local)
        
    def funcion_id_imagenes(self, informacion_local: dict) -> list:
        
        """
        toma el diccionario con la informacion y crea una lista que contiene los id de las imagenes
        """
        self.id_cine = int(informacion_local["cinema_id"])
        
        self.url_api_1 = f'http://vps-3701198-x.dattaweb.com:4000/cinemas/{self.id_cine}/movies'
        self.token_1 = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU'
        self.headers_1 = {'Authorization': f'Bearer {self.token_1}'}
        self.id_ubicacion = requests.get(self.url_api_1, headers=self.headers_1)
        
        lista_id_peliculas = self.id_ubicacion.json()[0]["has_movies"]
        
        lista_id_imagenes = [lista_id_peliculas[0], lista_id_peliculas[1], lista_id_peliculas[2], 
                        lista_id_peliculas[3], lista_id_peliculas[4], lista_id_peliculas[5]]
        
        return lista_id_imagenes

    def volver_pantalla_inicial_boton(self) -> None:
        
        """
        vuelve a la pantalla anterior
        """
        self.master.withdraw()
        
        self.ventana0.deiconify()

    def creacion_botones(self, lista_id_imagenes: list) -> None:
        
        """
        crea los botones que tienen la funcion de llevar a la ventana2 y el boton de volver
        """
        posicion_y = 200
        
        iterar_imagenes = 0
        
        for n in range(1,7):
            
            posicion_x = 100
            
            if n % 2 == 0: posicion_x = 700
            
            if n == 3: posicion_y = 460
            
            elif n == 5: posicion_y = 720
            
            if n == 1: n = 0
            
            url_info_pelis_botones_ver = "http://vps-3701198-x.dattaweb.com:4000/movies/" + f"{lista_id_imagenes[iterar_imagenes]}"
            
            iterar_imagenes += 1
        
            token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU"
            headers= {"Authorization": f"Bearer {token}"} 
        
            info_pelis_botones_ver = requests.get(url_info_pelis_botones_ver, headers = headers)
                
            self.botones = tk.Button(self.master, text = "Ver", width = 10, height = 1, bd = "7",
                command = lambda dict_boton_ver = info_pelis_botones_ver.json():self.ir_pagina_secundaria(dict_boton_ver))
            
            self.botones.place(x = posicion_x, y = posicion_y)   
        
        boton_volver=tk.Button(self.master, text="<-- Volver", bg="Black",fg="White",bd=5,cursor="hand2",
                            command=lambda: self.volver_pantalla_inicial_boton())
        boton_volver.place(x=420,y=30)     
        
        
    def ir_pagina_secundaria(self, dict_info_peliculas: dict) -> None:
        
        """
        cierra la ventana actual y abre la ventana2
        """
        self.master.withdraw()
        
        ventana_2 = tk.Toplevel()
        
        pantalla_secundaria = Ventana2(ventana_2,dict_info_peliculas,self.master,self.informacion_local)
        #IR A VENTANA 2
        
        
    def verificar_pelicula(self, ingreso_del_usuario: str, lista_id_imagenes: list) -> None: 
        
        """
        toma lo que ingresó el usuario y busca en las peliculas disponibles, si está entre ellas lo redirige a la ventana2
        """
        for i in range(len(lista_id_imagenes)):
            
            url_info_pelis = "http://vps-3701198-x.dattaweb.com:4000/movies/" + f"{lista_id_imagenes[i]}"
            
            token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU"
            headers= {"Authorization": f"Bearer {token}"}
            
            self.info_pelis = requests.get(url_info_pelis, headers = headers)
            
            self.nombres_pelis = (self.info_pelis.json()["name"])
            
            self.nombres_pelis_minusculas = self.nombres_pelis.lower()
            
            if self.nombres_pelis_minusculas == ingreso_del_usuario:
            
                self.ir_pagina_secundaria(self.info_pelis.json())
            
    def buscador_con_boton(self, informacion_local: dict, lista_id_imagenes: list) -> None:
        
        """
        crea una entrada de texto , un label con la ubicacion actual y un boton que te redirige a la ventana2 si ingresaste una pelicula
        """
        ubicacion = informacion_local["location"]
        
        ingreso_del_usuario = tk.StringVar(self.master)
        
        self.entrada_de_texto = tk.Entry(self.master, width = 37,  fg = "White", bg = "black", justify = "center", textvariable = ingreso_del_usuario)
        self.entrada_de_texto.place(x = 340, y = 300)
        
        
        self.boton_buscar = tk.Button(self.master, text = "Buscar Película",
                                    width = 15, command = lambda: self.verificar_pelicula(ingreso_del_usuario.get(), lista_id_imagenes))
        self.boton_buscar.place(x = 395, y = 350)
        
        self.etiqueta_ubicacion = tk.Label(self.master, text = f"Usted está en el cine de {ubicacion}", bg = "light gray",
                                        justify = "center").place(x = 355, y = 730)
        

    def creador_canvas_imagenes(self, lista_contenedores: list, informacion_local: dict):
        
        """
        crea los canvas dentro de los frames con sus respectivas imagenes, a las cuales se las decodifica por base64 para poder mostrarlas
        """
        self.id_cine = int(informacion_local["cinema_id"])
        
        self.url_api_1 = f'http://vps-3701198-x.dattaweb.com:4000/cinemas/{self.id_cine}/movies'
        self.token_1 = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU'
        self.headers_1 = {'Authorization': f'Bearer {self.token_1}'}
        self.id_ubicacion = requests.get(self.url_api_1, headers=self.headers_1)
        
        lista_id_peliculas = self.id_ubicacion.json()[0]["has_movies"]
        
        lista_id_imagenes_frames = [lista_id_peliculas[0], 0, lista_id_peliculas[1], lista_id_peliculas[2], 0,
                        lista_id_peliculas[3], lista_id_peliculas[4], 0, lista_id_peliculas[5]]
        
        lista_imagenes = []
        
        for i in lista_id_imagenes_frames:
            
            if i == 0: 
                lista_imagenes.append(0)
                continue
            
            self.url_api = 'http://vps-3701198-x.dattaweb.com:4000/posters/' + f"{i}"
            self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU'
            self.headers = {'Authorization': f'Bearer {self.token}'}
            self.response = requests.get(self.url_api, headers=self.headers)
            
            # Tomar la parte después de la coma
            self.codigo_base64 = self.response.content.decode("utf-8").split(",", 1)[-1] 
            
            # Decodificar la cadena Base64 modificada
            self.imagen_bytes = base64.b64decode(self.codigo_base64)
            
            # Agregar los bytes de la imagen a una lista
            lista_imagenes.append(self.imagen_bytes)
            
        for i in range(len(lista_imagenes)):
            
            if lista_imagenes[i] == 0: 
                continue
            
            canvas_general = tk.Canvas(lista_contenedores[i], bg = "black", height = 260, width = 300, borderwidth = 0, highlightthickness = 0)
            canvas_general.grid(row = 0, column = 0, sticky = "nesw", padx = 0, pady = 0)
            
            imagen_en_canvas = Image.open(BytesIO(lista_imagenes[i]))
            canvas_general.image = ImageTk.PhotoImage(imagen_en_canvas.resize((135, 192), Image.LANCZOS))
            canvas_general.create_image((300 - 135) / 2, (200 - 192) / 2, image = canvas_general.image, anchor = 'nw')
            
class Ventana2:
    
    def __init__(self, ventana, dict_info_peliculas: dict, ventana1, informacion_local:dict) -> None:
        
        """
        crea la ventana2, que muestra la información de la pelicula
        """
        
        self.ventana_2 = ventana
        self.ventana_2.geometry("800x500+200+100")
        self.ventana_2.config(bg= "black")
        self.ventana_2.title("Demostración")
        self.ventana_2.resizable(False,False)
        
        self.informacion_local=informacion_local
        
        self.informacion=dict_info_peliculas
        
        self.id=self.informacion["id"]
        
        self.crear_frames(ventana1)
        print(self.informacion_local)
    
    def crear_frames(self,ventana1) -> None:
        
        """
        crea los frames dentro de la ventana2
        """
        self.pantalla_ventana_2_num1 = tk.Frame(self.ventana_2, bg= "gray", width=400, height=400, relief= "groove", bd= 4)
        self.pantalla_ventana_2_num1.place(x= 0, y= 100)

        self.pantalla_ventana_2_num2 = tk.Frame(self.ventana_2, bg= "gray", width=400, height=430, relief= "groove", bd= 4)
        self.pantalla_ventana_2_num2.place(x=400, y= 0)
    
        self.crear_etiquetas(ventana1)    
    
    def crear_texto_informativo(self, posicion: int) -> str:
        
        """
        crea la información de la película para luego mostrarla
        """
        self.url= "http://vps-3701198-x.dattaweb.com:4000/movies/" + self.id

        self.token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU"

        self.headers = {"Authorization":f"Bearer {self.token}"}

        self.response= requests.get(self.url, headers=self.headers)

        self.dict_poster = self.response.json()
    
        self.claves_texto = ["name", "synopsis", "gender", "duration", "actors", "directors", "rating"]
        self.reemplazo_claves_texto = ["Titulo: ", "Sinopsis: ", "Género: ", "Duración: ","Actores: ", "Directores: ", "Rating: " ]
        self.texto_completo = f"{self.reemplazo_claves_texto[posicion]}{self.dict_poster[self.claves_texto[posicion]]}" 

        return self.texto_completo
    
    def crear_imagen(self) -> any:
        
        """
        obtiene las imagenes y las muestra despues de decodificarlas
        """
        self.url_api = 'http://vps-3701198-x.dattaweb.com:4000/posters/'+ f"{self.id}"
        self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU'
        self.headers = {'Authorization': f'Bearer {self.token}'}
        self.response = requests.get(self.url_api, headers=self.headers)
        
        self.codigo_base64 = self.response.content.decode("utf-8")
        self.codigo_base64 = self.codigo_base64.split(",", 1)[1]
        
        self.longitud_requerida = len(self.codigo_base64) + (4 - len(self.codigo_base64) % 4) % 4
        self.codigo_base64_padded = self.codigo_base64.ljust(self.longitud_requerida, "=")
        
        self.imagen_bytes = base64.b64decode(self.codigo_base64_padded)
        self.imagen_pillow = Image.open(BytesIO(self.imagen_bytes))
        self.imagen_pillow = self.imagen_pillow.resize((387,387))
        self.tk_imagen = ImageTk.PhotoImage(self.imagen_pillow)
        
        return self.tk_imagen
        
    def crear_etiquetas(self, ventana1) -> None:
        
        """
        crea el canvas en el que iría la imagen
        """
        self.etiqueta_imagen = tk.Label(self.pantalla_ventana_2_num1, image= self.crear_imagen())
        
        self.etiqueta_imagen.pack()
        
        for i in range(7):
            self.descripcion= tk.Label(self.pantalla_ventana_2_num2,text= self.crear_texto_informativo(i),width=45,height=1, font= ["Arial", 10], anchor= "w")
            if i == 1:
                self.descripcion = tk.Text(self.pantalla_ventana_2_num2, wrap=tk.WORD, width=52, height=16, font=["Arial", 10])
                self.descripcion.insert(tk.END, self.crear_texto_informativo(i))
                self.descripcion.config(state=tk.DISABLED)
                self.descripcion.place(x=12,y=30)
            elif i == 0:
                self.descripcion.place(x=12,y=5)
            else:
                self.descripcion.place(x=12,y=245 + 25*i)
        
        self.crear_botones(ventana1)
    
    def ir_ventana3(self) -> None:
        
        """
        cierra la ventana2 y abre la ventana3
        """
        self.ventana_2.withdraw() 
        
        #CONSTRUCTOR A VENTANA 3
        ventana3=tk.Tk()
        
        url="http://vps-3701198-x.dattaweb.com:4000"+"/snacks" 
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU"
        headers = {"Authorization": f"Bearer {token}"}    
        conseguir_url = requests.get(url, headers=headers)
        
        pantalla_reserva=Ventana_3(ventana3,conseguir_url,self.informacion,self.informacion_local)
        
        pantalla_reserva.ventana3.mainloop()
        
    
    def volver_ventana1(self,ventana1) -> None:
        
        """
        vuelve a la ventana1, cerrando la ventana2
        """
        self.ventana_2.withdraw() 
        ventana1.deiconify()
    
    def crear_botones(self,ventana1) -> None:
        
        """
        crea los botones que llevan a la ventana3 y a la ventana1 respectivamente
        """
        self.boton0_ir_a_pantalla_3= tk.Button(self.ventana_2, bg= "gray", text= "boton compra (dirige a pantalla 3)", 
                                            fg= "black", font= ("Arial", 15), relief= "groove", bd = 15, cursor="hand2",
                                            command=lambda: self.ir_ventana3())
        self.boton0_ir_a_pantalla_3.place(x=433, y=432)
        
        self.boton1_ir_a_pantalla_1 = tk.Button(self.ventana_2, bg= "gray", text= "<= Volver", fg= "black", font= ("Arial", 15), 
                                                relief= "groove", bd= 15, cursor= "hand2",
                                                command=lambda: self.volver_ventana1(ventana1))
        self.boton1_ir_a_pantalla_1.place(x= 30, y= 15)
