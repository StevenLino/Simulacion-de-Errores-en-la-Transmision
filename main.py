#Aqui estará el programa principal que usará las funciones del archivo def.pv y los documentos en este repositorio
import funciones as fd

fd.create_txt()
fd.txt_to_bin("hola.txt","hola.bin")
d= fd.file_size("hola.bin")
print(d)