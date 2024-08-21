# Aquí estará el programa principal que usará las funciones del archivo def.pv y los documentos en este repositorio
import funciones as fd
import os

# Configuración de IPs
oip = "192.168.1.10"  # IP de origen
dip = "203.0.113.5"   # IP de destino

# Mensaje de bienvenida
welcome = "     Bienvenido al programa de simulación de errores     "
print(welcome)
print("_" * len(welcome))

# Menú de opciones
print("¿Desea crear un archivo o leer uno?")
op = input("Ingrese opción \n1) Crear Archivo \n2) Seleccionar archivo \nOpción: ")

# Validación de la opción ingresada
while op not in ["1", "2"]:
    op = input("Ingrese opción\n1) Crear Archivo\n2) Seleccionar archivo \nOpción: ")

if op == "1":
    # Crear un archivo nuevo y convertirlo a binario
    name = fd.create_txt()  # Suponiendo que `create_txt` devuelve el nombre del archivo creado
    name_base = os.path.splitext(name)[0]  # Extrae el nombre base sin extensión
    fd.txt_to_bin(name, name_base + ".bin")  # Convierte el archivo de texto a binario
    seg, data = fd.file_size(name_base + ".bin")  # Obtiene tamaño del archivo binario
    g = fd.segment(oip, dip, name_base + ".bin")  # Segmenta el archivo binario
else:
    # Seleccionar un archivo existente y convertirlo a binario
    print("Entró en la opción de seleccionar archivo")
    ruta = fd.seleccionar_archivo()  # Obtiene la ruta del archivo seleccionado
    if ruta:  # Verifica que se haya seleccionado un archivo
        nombre_completo = os.path.basename(ruta)  # Obtiene el nombre completo del archivo
        nombre_base = os.path.splitext(nombre_completo)[0]  # Extrae el nombre base sin extensión
        print(nombre_base)
        fd.txt_to_bin(ruta, nombre_base + ".bin")  # Convierte el archivo de texto a binario
        seg, data = fd.file_size(nombre_base + ".bin")  # Obtiene tamaño del archivo binario
        g = fd.segment(oip, dip, nombre_base + ".bin")  # Segmenta el archivo binario
    else:
        print("No se seleccionó ningún archivo.")




#name = fd.create_txt()
#name = name.split(".")[0]
#fd.txt_to_bin(name+".txt",name+".bin")
#seg,data= fd.file_size(name+".bin")
#g = fd.segment(oip,dip,name+".bin")
#print(g)
#los primeros 232 bits son el header
#for i in g:
#    print(fd.bin_to_str(i[:240]))
