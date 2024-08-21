import os
import random
import math
import tkinter as tk
from tkinter import filedialog
#Aquí se crearan las funciones para la simulacion de errores y envio de datos al servidor

#Funcion para crear archivos txt con la información del usuario
def create_txt():
  texto = input("Proporcione el texto que quiere enviar: ")
  if len(texto) == 0:
    texto = " "
  name = input("De un nombre para su archivo: ")
  while len(name) == 0:
    print("¡El archivo debe tener nombre!")
    name = input("De un nombre para su archivo: ")
  with open(name, 'w') as file:
        file.write(texto)
  return name

def seleccionar_archivo():
    # Crear la ventana principal (oculta)
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal

    # Abrir el cuadro de diálogo para seleccionar un archivo
    archivo = filedialog.askopenfilename(
        title="Selecciona un archivo",
        filetypes=[("Todos los archivos", "*.*"), ("Archivos de texto", "*.txt")]
    )
    return archivo

#Función que convierte el archivo .txt del usuario a un archivo .bin para poder procesarlo.
#Los archivos .bin son un tipo de archivo que contine informacion en formato binario.
def txt_to_bin(input_txt_path, output_bin_path):
    # Leer el contenido del archivo .txt
    with open(input_txt_path, 'r') as txt_file:
        text_data = txt_file.read()
    
    # Convertir el contenido a binario
    binary_data = text_data.encode('utf-8')
    #print(binary_data)

    # Convierte cada byte a su representación binaria
    binario = ''.join(format(byte, '08b') for byte in binary_data)
    #print(binario)
    
    # Guardar los datos binarios en un nuevo archivo .bin
    with open(output_bin_path, 'w') as bin_file:
        bin_file.write(binario)


#Esta funcion crear un texto a binario, si la opcion es 0 sabra que es una ip y quitara los . del texto recibido
def create_binary(o,dato):
    if o == 0:
       num = dato.split(".")
       num2 = [i.encode('utf-8') for i in num]
       binario = "".join([format(i,"08b") for i in num2])
       return binario
    else:
       binary_data = dato.encode('utf-8')
       binario = ''.join(format(byte, '08b') for byte in binary_data)
       return binario


#Funcion que convierte texto a binario
def str_to_bin(text):
   if type(text) == int:
      text = str(text)
   binary_data = text.encode('utf-8')
   binario = ''.join(format(byte, '08b') for byte in binary_data)
   return binario

#funcion que revierte bits a texto
def bin_to_str(binary_data):
    # Dividimos la cadena binaria en segmentos de 8 bits
    byte_array = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    
    # Convertimos cada segmento de 8 bits a su valor decimal y los unimos en un byte array
    text = ''.join([chr(int(byte, 2)) for byte in byte_array])
    
    return text

#Función que estima el peso de un archivo y define en cuantas tramas se dividirá
def file_size(file_name):
  data_size = os.path.getsize(file_name)/8
  print(data_size)
  segmentos = data_size/1024
  with open(file_name, 'r') as data:
    text_data = data.read()
    data = [text_data[i:i + 8] for i in range(0, len(text_data), 8)]
    return segmentos,data
  


#funcion que permite calcular el checksum del segmento de datos
def calcularChecksum(datos):
   
  #tener en cuenta que la longitud de datos sea par, caso contrario, agregar un byte de padding
  if len(datos) % 2 != 0:
    datos += b'\x00'
  

  suma = 0

  for i in range(0, len(datos), 2):
    #Combinar dos bytes en una palabra de 16 bits
    palabra_16bits = (int(datos[i]) << 8) + int(datos[i + 1])
    suma += palabra_16bits
        
    #Añadir el acarreo si la suma es mayor que 0xFFFF
    suma = (suma & 0xFFFF) + (suma >> 16)

  #se toma el complemento a 1
  checksum = ~suma & 0xFFFF

   # Convertir el checksum a binario de 16 bits
  checksum_binario = str_to_bin(checksum)#format(checksum, '016b')
  #print(checksum_binario)  
  return checksum_binario

# funcion que valida los checksum, el del mensaje y el que se genera
def validar_checksum(datos, checksum_recibido):
    
  #Se calcula el checksum del mensaje
  checksum_calculado = calcularChecksum(datos)
    
  #se compara los checksum y retorna true o false
  return checksum_calculado == checksum_recibido

#Funcion que genera el Header + Trama
def t_header(oip,dip,sec,trama):
   #los datos hay que convertirlos a binario
   sport= create_binary(1,oip)
   dport= create_binary(1,dip)
   check = calcularChecksum(trama)
   sec_bin = str_to_bin(str(sec)) #format(sec,"08b")

   #formato del header 
   header= sport + dport + str(sec_bin) + str(check)
   print(len(header))
   
   return header

#Función que separa el archivo .bin en segmentos más pequeños para poder simular la segmentación del proceso TCP/IP
#Se asume que el dispositivo que se tiene solo puede enviar maximo 1024 bits y se tiene que dividir el archivo en la cantidad
#de segmentos necesarios para satisfacer los requerimientos.

def segment(oip, dip, file_name):
    seg, data = file_size(file_name)
    seg = math.floor(seg) + 1
    info = []

    # Verifica el tamaño de los datos y su estructura
    print(f"Tamaño de los datos: {len(data)}")
    print(f"Número de segmentos calculados: {seg}")
    
    # Si los datos tienen más de 1024 bytes, los segmentamos
    if len(data) > 1024:
        for j in range(0, len(data), 1024):
            if (j + 1024) <= len(data):
                segmento = "".join(data[j:j + 1024])
            else:
                segmento = "".join(data[j:])

            # Generar el encabezado para el segmento
            head = t_header(oip, dip, j // 1024, segmento)
            
            # Verificar el contenido del segmento y el encabezado
            print(f"Segmento {j // 1024}: {segmento}")
            print(f"Encabezado {j // 1024}: {head}")
            
            # Agregar el segmento + encabezado a la lista info
            info.append(head + segmento + str_to_bin(seg))
    
    else:
        segmento = "".join(data)
        head = t_header(oip, dip, 0, segmento)
        
        # Verificar el contenido del único segmento
        print(f"Segmento único: {segmento}")
        print(f"Encabezado único: {head}")
        
        info.append(head + segmento)

    # Verificar el contenido de la lista final
    print(f"Contenido de la lista info (número de elementos): {len(info)}")
    return info

   
#Función que simula un envío fuera de orden, se envía la lista de segmentos
def simularErrorFueraOrden (segmentos):
   return random.shuffle (segmentos)

# Función que simula la pérdida de paquetes aleatoria, donde existe un 10% de probabilidad de que un paquete se pierda.
def simularErrorPerdidaPaquetes (segmentos):
   return [segmento for segmento in segmentos if random.random() > 0.1]

#Función que simula un cambio de bits del mensaje
def simularCambioBit (segmentos):
  for i in range (len(segmentos)):
    prop = 0.001
    #Se da un 10% de posibilidad de que exista uno o varios cambios de bits en un segmento
    if random.random() < prop:
        segmento = bytearray(segmentos[i].encode('utf-8'))

        #Se asume que se pueda realizar un cambio de bit de entre una y cinco veces
        for c in range (random.randint (1, 5)):

          #Se selecciona una posición cualquiera para cambiar un bit
          posicion_cambio_bit = random.randint (0, len(segmento) - 1)

        #Se invierte el bit en la posición dada
        segmento [posicion_cambio_bit] ^= 0xFF

  return segmentos

## alternatva a discutur para el método de segmentos

#def segmentos(file_name, oip, dip):
#   seg, data = file_size(file_name)
#   segmentos = []
#   sec = 0  # Inicializa el número de secuencia
   
#   for i in range(0, len(data), 8):
#       if (i + 8) < len(data):
#           segmento = "".join(data[i:i + 8])
#       else:
#           segmento = "".join(data[i:])
       
       # Calcula el checksum para el segmento
#       checksum = calcularChecksum(segmento.encode('utf-8'))
       
       # Genera el header
#       header = t_header(oip, dip, sec, checksum)
       
       # Combina el header con el segmento
#       segmentos.append(header + segmento)
       
       # Incrementa el número de secuencia
#       sec += 1
   
#   return segmentos
