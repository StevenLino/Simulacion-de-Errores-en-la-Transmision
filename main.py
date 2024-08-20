#Aqui estará el programa principal que usará las funciones del archivo def.pv y los documentos en este repositorio
import funciones as fd
oip= "192.168.1.10" #IP d origen
dip= "203.0.113.5"
welcome = "     Bienvenido al programa de simulacion de errores     "
print(welcome)
print("_"*len(welcome))
name = fd.create_txt()
name = name.split(".")[0]
fd.txt_to_bin(name+".txt",name+".bin")
#seg,data= fd.file_size(name+".bin")
g = fd.segment(oip,dip,name+".bin")
print(g)
for i in g:
    print(fd.bin_to_str(i[:240]))
