import socket
import threading

ip = "localhost"
port = 8432

srv_clogin = socket.socket()
srv_clogin.bind((ip, port))
srv_clogin.listen(100)
socket_id_clientes = []
nombre_clientes = []

def recibir_mensajes(conection, addr):
    while True:
        try:
            missatge = conection.recv(1024)
            if missatge:
                missatge_val = missatge.decode()
                if "+" in missatge_val:
                    index_eliminar_client = missatge_val.index("+")
                    eliminar_client(missatge_val[index_eliminar_client+1:])
                else:
                    enviar_mensajes(missatge)  
        except:
            pass

def eliminar_client(nom):
    global nombre_clientes
    global socket_id_clientes
    index_si = nombre_clientes.index(nom)
    socket_id_clientes.pop(index_si)
    print("{} a marxat del xat".format(nom))
    nombre_clientes.pop(index_si)

def client_fallido_inici_sessio(conn):
    global socket_id_clientes
    global nombre_clientes
    while True:
        try:
            missatge = conn.recv(1024)
            if missatge:
                if "$" in missatge.decode():
                    nom_client_inici_sessio_fallat = missatge.decode()
                    index_mes_fallat = nom_client_inici_sessio_fallat.index("$")
                    index_dos_punts_fallat = nom_client_inici_sessio_fallat.index("¿")
                    nom_client_registrar_fallat = missatge[index_mes_fallat+1:index_dos_punts_fallat]
                    contrasenya_registre_usuari_fallat = missatge[index_dos_punts_fallat+1:]

                    verificar_nom_registre_existent_fallat = open("basedades.txt", "r")
                    llegir_verificar_nom_registre_existent_fallat = verificar_nom_registre_existent_fallat.read()
                    llista_verificar_nom_registre_existent_fallat = llegir_verificar_nom_registre_existent_fallat.split(",")
                    verificar_nom_registre_existent_fallat.close()
                    if "{}:{}".format(nom_client_registrar_fallat,contrasenya_registre_usuari_fallat) in llista_verificar_nom_registre_existent_fallat:
                        conn.send("Error".encode())
                    else:
                        base_dades_fallat = open("basedades.txt", "a")
                        base_dades_fallat.write(",{}:{}".format(nom_client_registrar_fallat,contrasenya_registre_usuari_fallat))
                        print("S'ha registrar l'usuari {}".format(nom_client_registrar_fallat))
                        base_dades_fallat.close()
                        conn.send("Correct".encode())
                else :
                    base_dades_inici_error = open("basedades.txt", "r")
                    llegir_base_dades_inici_error = base_dades_inici_error.read()
                    llista_verificadora_usuari_error = llegir_base_dades_inici_error.split(",")
                    nom_verifer_inici_sessio_error = missatge.decode()
                    index_protocol_inici_sessio_error = nom_verifer_inici_sessio_error.index("&")
                    nom_usuari_inci_sessio_error = nom_verifer_inici_sessio_error[0:index_protocol_inici_sessio_error]
                    contrasenya_inici_sessio_error = nom_verifer_inici_sessio_error[index_protocol_inici_sessio_error+1:]
                    base_dades_inici_error.close()
                    print("{}:{}".format(nom_usuari_inci_sessio_error, contrasenya_inici_sessio_error))
                    if "{}:{}".format(nom_usuari_inci_sessio_error,contrasenya_inici_sessio_error) in llista_verificadora_usuari_error and nom_verifer_inici_sessio_error not in nombre_clientes:
                    #if nom_client.decode() not in nombre_clientes:
                        socket_id_clientes.append(conn)
                        nombre_clientes.append(nom_usuari_inci_sessio_error)
                        print("S'ha connectat l'usuari {} amb la IP --> {}".format(nom_usuari_inci_sessio_error, "ip"))
                        conn.send("Correct".encode())  
                        ejecutar_funcio2 = threading.Thread(target=recibir_mensajes, args=(conn, "ip"))
                        ejecutar_funcio2.daemon = True
                        ejecutar_funcio2.start()
                        break
                    else:
                        conn.send("Error".encode())
        except:
            pass

def client_fallido_registre_sessio(connnn):
    while True:
        try:
            missatge_registre_fallido = connnn.recv(1024)
            if missatge_registre_fallido:
                if "&" in missatge_registre_fallido.decode():
                    base_dades_inici_fallido = open("basedades.txt", "r")
                    llegir_base_dades_inici_fallido = base_dades_inici_fallido.read()
                    llista_verificadora_usuari_fallido = llegir_base_dades_inici_fallido.split(",")
                    nom_verifer_inici_sessio_fallido = missatge_registre_fallido.decode()
                    index_protocol_inici_sessio_fallido = nom_verifer_inici_sessio_fallido.index("&")
                    nom_usuari_inci_sessio_fallido = nom_verifer_inici_sessio_fallido[0:index_protocol_inici_sessio_fallido]
                    contrasenya_inici_sessio_fallido = nom_verifer_inici_sessio_fallido[index_protocol_inici_sessio_fallido+1:]
                    base_dades_inici_fallido.close()
                    print("{}:{}".format(nom_usuari_inci_sessio_fallido, contrasenya_inici_sessio_fallido))
                    if "{}:{}".format(nom_usuari_inci_sessio_fallido,contrasenya_inici_sessio_fallido) in llista_verificadora_usuari_fallido and nom_verifer_inici_sessio_fallido not in nombre_clientes:
                    #if nom_client.decode() not in nombre_clientes:
                        socket_id_clientes.append(connnn)
                        nombre_clientes.append(nom_usuari_inci_sessio_fallido)
                        print("S'ha connectat l'usuari {} amb la IP --> {}".format(nom_usuari_inci_sessio_fallido, "ip"))
                        connnn.send("Correct".encode())  
                        ejecutar_funcio2 = threading.Thread(target=recibir_mensajes, args=(connnn, "ip"))
                        ejecutar_funcio2.daemon = True
                        ejecutar_funcio2.start()
                        break
                    else:
                        connnn.send("Error".encode())
                else:
                    nombre_usuario_fallido = missatge_registre_fallido.decode()
                    index_mes_fallido = nombre_usuario_fallido.index("$")
                    index_dos_punts_fallido = nombre_usuario_fallido.index("¿")
                    nom_client_registrar_fallido = nombre_usuario_fallido[index_mes_fallido+1:index_dos_punts_fallido]
                    contrasenya_registre_usuari_fallido = nombre_usuario_fallido[index_dos_punts_fallido+1:]

                    verificar_nom_registre_existent_fallido = open("basedades.txt", "r")
                    llegir_verificar_nom_registre_existent_fallido = verificar_nom_registre_existent_fallido.read()
                    llista_verificar_nom_registre_existent_fallido = llegir_verificar_nom_registre_existent_fallido.split(",")
                    verificar_nom_registre_existent_fallido.close()
                    if "{}:{}".format(nom_client_registrar_fallido,contrasenya_registre_usuari_fallido) in llista_verificar_nom_registre_existent_fallido:
                        connnn.send("Error".encode())
                    else:
                        base_dades = open("basedades.txt", "a")
                        base_dades.write(",{}:{}".format(nom_client_registrar_fallido,contrasenya_registre_usuari_fallido))
                        print("S'ha registrar l'usuari {}".format(nom_client_registrar_fallido))
                        base_dades.close()
                        connnn.send("Correct".encode()) 
        except:
            pass

def enviar_mensajes(mss):
    mss = mss.decode()
    index_nom_a_enviar = mss.index("-")
    nom_a_enviar = mss[0:index_nom_a_enviar]
    index_nom_verificacio_user = mss.index("_")
    nom_verificacio_user = mss[index_nom_verificacio_user+1:]
    missatge_enviar = mss[index_nom_a_enviar+1:index_nom_verificacio_user]
    indice_nombre_cliente = nombre_clientes.index(nom_a_enviar)
    connexion_enviar_mensaje = socket_id_clientes[indice_nombre_cliente]
    try:
        connexion_enviar_mensaje.send("{},{}".format(nom_verificacio_user,missatge_enviar).encode())
    except:
        pass 
        
while True:
    connexio, address = srv_clogin.accept()
    nom_client = connexio.recv(1024)
    if "$" in nom_client.decode():
        missatge_registre = nom_client.decode()
        index_mes = missatge_registre.index("$")
        index_dos_punts = missatge_registre.index("¿")
        nom_client_registrar = missatge_registre[index_mes+1:index_dos_punts]
        contrasenya_registre_usuari = missatge_registre[index_dos_punts+1:]

        verificar_nom_registre_existent = open("basedades.txt", "r")
        llegir_verificar_nom_registre_existent = verificar_nom_registre_existent.read()
        llista_verificar_nom_registre_existent = llegir_verificar_nom_registre_existent.split(",")
        verificar_nom_registre_existent.close()
        if "{}:{}".format(nom_client_registrar,contrasenya_registre_usuari) in llista_verificar_nom_registre_existent:
            connexio.send("Error".encode())
            print("L'usuari ja existeix")
            ejecutar_funcio_client_en_espera_registre = threading.Thread(target=client_fallido_registre_sessio, args=(connexio,))
            ejecutar_funcio_client_en_espera_registre.daemon = True
            ejecutar_funcio_client_en_espera_registre.start()
        else:
            base_dades = open("basedades.txt", "a")
            base_dades.write(",{}:{}".format(nom_client_registrar,contrasenya_registre_usuari))
            print("S'ha registrar l'usuari {}".format(nom_client_registrar))
            base_dades.close()
            connexio.send("Correct".encode())
            ejecutar_funcio_client_en_espera4 = threading.Thread(target=client_fallido_registre_sessio, args=(connexio,))
            ejecutar_funcio_client_en_espera4.daemon = True
            ejecutar_funcio_client_en_espera4.start()  
    else: 
        base_dades_inici = open("basedades.txt", "r")
        llegir_base_dades_inici = base_dades_inici.read()
        llista_verificadora_usuari = llegir_base_dades_inici.split(",")
        nom_verifer_inici_sessio = nom_client.decode()
        index_protocol_inici_sessio = nom_verifer_inici_sessio.index("&")
        nom_usuari_inci_sessio = nom_verifer_inici_sessio[0:index_protocol_inici_sessio]
        contrasenya_inici_sessio = nom_verifer_inici_sessio[index_protocol_inici_sessio+1:]
        base_dades_inici.close()
        print("{}:{}".format(nom_usuari_inci_sessio, contrasenya_inici_sessio))
        if "{}:{}".format(nom_usuari_inci_sessio,contrasenya_inici_sessio) in llista_verificadora_usuari and nom_usuari_inci_sessio not in nombre_clientes:
        #if nom_client.decode() not in nombre_clientes:
            socket_id_clientes.append(connexio)
            nombre_clientes.append(nom_usuari_inci_sessio)
            print("S'ha connectat l'usuari {} amb la IP --> {}".format(nom_usuari_inci_sessio, address))
            connexio.send("Correct".encode())  
            ejecutar_funcio = threading.Thread(target=recibir_mensajes, args=(connexio, address))
            ejecutar_funcio.daemon = True
            ejecutar_funcio.start()
        else:
            connexio.send("Error".encode())
            ejecutar_funcio_client_en_espera = threading.Thread(target=client_fallido_inici_sessio, args=(connexio,))
            ejecutar_funcio_client_en_espera.daemon = True
            ejecutar_funcio_client_en_espera.start()
            #connexio.close()
            #srv_clogin = socket.socket()

