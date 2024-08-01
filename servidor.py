import socket
import threading

host = '127.0.0.1'
puerto = 65123

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((host, puerto))
servidor.listen()

print(f"Servidor en línea en {host}:{puerto}")

clientes = []
nombres_usuarios = []

def transmitir(mensaje, _cliente):
    for cliente in clientes:
        if cliente != _cliente:
            cliente.send(mensaje)

def manejar_mensajes(cliente):
    while True:
        try:
            mensaje = cliente.recv(1024)
            transmitir(mensaje, cliente)
        except:
            indice = clientes.index(cliente)
            nombre_usuario = nombres_usuarios[indice]
            transmitir(f"Servidor: {nombre_usuario} se ha desconectado.".encode('utf-8'), cliente)
            clientes.remove(cliente)
            nombres_usuarios.remove(nombre_usuario)
            cliente.close()
            break

def aceptar_conexiones():
    while True:
        cliente, direccion = servidor.accept()
        
        cliente.send("@nombre_usuario".encode("utf-8"))
        nombre_usuario = cliente.recv(1024).decode("utf-8")

        clientes.append(cliente)
        nombres_usuarios.append(nombre_usuario)

        print(f"{nombre_usuario} está conectado desde {str(direccion)}")
        mensaje = f"Servidor: {nombre_usuario} se ha unido al chat.".encode("utf-8")
        transmitir(mensaje, cliente)
        cliente.send("Conectado al servidor.".encode("utf-8"))

        hilo = threading.Thread(target=manejar_mensajes, args=(cliente,))
        hilo.start()

aceptar_conexiones()
