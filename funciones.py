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
  with open(file_name, 'r') as data:
    text_data = data.read()
    data = [text_data[i:i + 8] for i in range(0, len(text_data), 8)]
    size = len(data)
    return size,data

#Función que separa el archivo .bin en segmentos más pequeños para poder simular la segmentación del proceso TCP/IP
#Se asume que el dispositivo que se tiene solo puede enviar maximo 1024 bits y se tiene que dividir el archivo en la cantidad
#de segmentos necesarios para satisfacer los requerimientos.



