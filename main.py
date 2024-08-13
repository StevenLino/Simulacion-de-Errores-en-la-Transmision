#Aqui estará el programa principal que usará las funciones del archivo def.pv y los documentos en este repositorio
import funciones as fd
welcome = "     Bienvenido al programa de simulacion de errores     "
print(welcome)
print("_"*len(welcome))
name = fd.create_txt()
name = name.split(".")[0]
fd.txt_to_bin(name+".txt",name+".bin")
d= fd.file_size("hola.bin")
print(d)