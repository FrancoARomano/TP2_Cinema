import cv2
from pyzbar.pyzbar import decode
from pyzbar import pyzbar
from PIL import Image
import os


def main() -> None: 
    centinela_1 = True

    centinela_2 = True

    while centinela_1:
        
        decision = input("Si quiere ingresar el id del QR ingrese 0, Si quiere leer el QR con su Webcam ingrese 1: ")

        if decision == "0" or decision == "1":
            centinela_1 = False

    if decision == "0":
        """
        tiene que haber un qr existente para que pueda ser ingresado
        """
        centinela_3 = True
        
        while centinela_3:
            
            id_ingresado = input("Ingrese el id de su QR ")
            
            if os.path.exists(f"ID_{id_ingresado}.png"):
                
                imagen = Image.open(f"ID_{id_ingresado}.png")
                codigo_qr = pyzbar.decode(imagen)[0]
                
                info_del_qr = codigo_qr.data.decode("utf8")
                
                with open("ingresos.txt", "a") as ingresos_txt:
                
                    ingresos_txt.write(info_del_qr + "\n")
                
                ingresos_txt.close()
                
                centinela_3 = False

    elif decision == "1":
        
        cap = cv2.VideoCapture(0)
        
        print("Para salir presione q con la ventana de la cámara")
        
        while centinela_2:
            
            ret, frame = cap.read()
                
            for codes in decode(frame):
                info = codes.data.decode('utf-8')
                
                with open("ingresos.txt", "a") as ingresos_txt:
                
                    ingresos_txt.write(info + "\n")
                    
                with open("ingresos.txt", "r") as archivo:
                    contenido = archivo.read()
                    contenido_lista = contenido.split("\n")
                    
                    for i in contenido_lista:
                        if info == i: centinela_2 = False
                
                ingresos_txt.close()
            
            cv2.imshow("LECTOR DE QR", frame)
                
            t = cv2.waitKey(1)
            
            if t == ord('q'):
                centinela_2 = False

        cv2.destroyAllWindows()
        cap.release()
        
main()