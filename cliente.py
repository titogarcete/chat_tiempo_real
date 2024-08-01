import socket
import threading

nombre_usuario = input("Ingrese su nombre de usuario: ")

host = '127.0.0.1'
puerto = 65123

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((host, puerto))

def recibir_mensajes():
    while True:
        try:
            mensaje = cliente.recv(1024).decode("utf-8")
            if mensaje == "@nombre_usuario":
                cliente.send(nombre_usuario.encode("utf-8"))
            else:
                print(mensaje)
        except:
            print("Ha ocurrido un error y se ha cerrado la conexión.")
            cliente.close()
            break

def enviar_mensajes():
    while True:
        mensaje = f"{nombre_usuario}: {input('')}"
        cliente.send(mensaje.encode("utf-8"))

hilo_recibir = threading.Thread(target=recibir_mensajes)
hilo_recibir.start()

hilo_enviar = threading.Thread(target=enviar_mensajes)
hilo_enviar.start()
