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

#Función que convierte el archivo .txt del usuario a un archivo .bin para poder procesarlo.
#Los archivos .bin son un tipo de archivo que contine informacion en formato binario.
def txt_to_bin(input_txt_path, output_bin_path):
    # Leer el contenido del archivo .txt
    with open(input_txt_path, 'r') as txt_file:
        text_data = txt_file.read()
    
    # Convertir el contenido a binario
    binary_data = text_data.encode('utf-8')
    print(binary_data)

    # Convierte cada byte a su representación binaria
    binario = ''.join(format(byte, '08b') for byte in binary_data)
    print(binario)
    
    # Guardar los datos binarios en un nuevo archivo .bin
    with open(output_bin_path, 'w') as bin_file:
        bin_file.write(binario)

#Funcion que convierte texto a binario
def str_to_bin(text):
   binary_data = text.encode('utf-8')
   binario = ''.join(format(byte, '08b') for byte in binary_data)
   return binario

#Función que estima el peso de un archivo y define en cuantas tramas se dividirá
def file_size(file_name):
  data_size = file_size = os.path.getsize(file_name)
  segmentos = data_size/1024
  with open(file_name, 'r') as data:
    text_data = data.read()
    data = [text_data[i:i + 8] for i in range(0, len(text_data), 8)]
    return segmentos,data


#Función que separa el archivo .bin en segmentos más pequeños para poder simular la segmentación del proceso TCP/IP
#Se asume que el dispositivo que se tiene solo puede enviar maximo 1024 bits y se tiene que dividir el archivo en la cantidad
#de segmentos necesarios para satisfacer los requerimientos.

def segmentos(file_name):
   seg,data= file_size(file_name)
   i = 0
   while i < len(data):
      if (i+8) < len(data):
        segmento = "".join(data[i:i+8])
        i += 9
      else:
        segmento = "".join(data[i:])
   head = "" #aqui se deberia llamar a la funcion que genera el header
   segmento = head + segmento
   return segmento

#funcion que permite calcular el checksum del segmento de datos
def calcularChecksum(datos):
   
  #tener en cuenta que la longitud de datos sea par, caso contrario, agregar un byte de padding
  if len(datos) % 2 != 0:
    datos += b'\x00'
  

  suma = 0

  for i in range(0, len(datos), 2):
    #Combinar dos bytes en una palabra de 16 bits
    palabra_16bits = (datos[i] << 8) + datos[i + 1]
    suma += palabra_16bits
        
    #Añadir el acarreo si la suma es mayor que 0xFFFF
    suma = (suma & 0xFFFF) + (suma >> 16)

  #se toma el complemento a 1
  checksum = ~suma & 0xFFFF
    
  return checksum

# funcion que valida los checksum, el del mensaje y el que se genera
def validar_checksum(datos, checksum_recibido):
    
  #Se calcula el checksum del mensaje
  checksum_calculado = calcularChecksum(datos)
    
  #se compara los checksum y retorna true o false
  return checksum_calculado == checksum_recibido