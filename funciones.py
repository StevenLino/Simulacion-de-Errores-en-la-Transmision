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
  with open(name, 'wb') as file:
        file.write(texto)

#Función que convierte el archivo .txt del usuario a un archivo .bin para poder procesarlo.
#Los archivos .bin son un tipo de archivo que contine informacion en formato binario.
def txt_to_bin(input_txt_path, output_bin_path):
    # Leer el contenido del archivo .txt
    with open(input_txt_path, 'r') as txt_file:
        text_data = txt_file.read()
    
    # Convertir el contenido a binario
    binary_data = text_data.encode('utf-8')
    
    # Guardar los datos binarios en un nuevo archivo .bin
    with open(output_bin_path, 'wb') as bin_file:
        bin_file.write(binary_data)

#Función que separa el archivo .bin en segmentos más pequeños para poder simular la segmentación del proceso TCP/IP

