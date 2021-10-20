import socket
from uuid import getnode as get_mac
import time
import numpy as np

def initialize_client():
    raspx = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    raspx.listen(5)
    while True:
        conn, addr = raspx.accept() #Server Ip obtained
        print("")
        message_first = conn.recv(4096).decode("utf-8")
        print(message_first)
        conn.send("Firts connection successful".encode("utf-8"))
        conn.close() #Connection closed
    return addr #Ip recovered

def initialize_system(server_ip, port):
    id = get_mac()

    raspx = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create socket for connection
    raspx.connect((server_ip, port))  # Connect to the server
    print("Connected to server")

    raspx.send(bytes(id.encode("utf-8")))  # Send clinet ID
    answer = raspx.recv(4096).decode("utf-8")
    agents = answer[0]

    initializing = True
    while initializing:  # Cycle that verifies server has identified all agents
        if answer[1] == agents:
            initializing = False
        time.sleep(5)
        raspx.send(bytes(id.encode("utf-8")))  # Send clinet ID
        answer = raspx.recv(4096).decode("utf-8")
    return  raspx

def update_values(message):
    x = np.zeros(agents)
    y = np.zeros(agents)
    for i in range(3, len(message)-1):
        if i%2 == 1:
            x[i] = float(message[i])
        else:
            y[i] = float(message[i])
    return {'x':np.transpose(x), 'y':np.transpose(y)}

def request_values(raspx):
    m3 = "Send new values"
    raspx.send(bytes(m3.encode("utf-8")))  # Send clinet model matrix request
    answer = raspx.recv(4096).decode("utf-8")
    return update_values(answer)

def request_model(raspx):
    m1 = "Request Model Matrix"
    raspx.send(bytes(m1.encode("utf-8")))  # Send clinet model matrix request
    answer = raspx.recv(4096).decode("utf-8")
    agents = int(answer[1])
    const = 2 * agents ** 2
    Ax = np.array(answer[:const- 1].split("#"), dtype=float).reshape((agents, agents))
    Bx = np.array(answer[const:2*const-1].split("#"), dtype=float).reshape((agents, agents))
    Ay = np.array(answer[2*const:3 * const - 1].split("#"), dtype=float).reshape((agents, agents))
    By = np.array(answer[3*const:4 * const - 1].split("#"), dtype=float).reshape((agents, agents))
    return {"Ax": Ax, "Bx": Bx, "Ay": Ay, "By": By}

def request_association(raspx):
    m2 = "Request Association Matrix"
    raspx.send(bytes(m2.encode("utf-8")))  # Send clinet model matrix request
    answer = raspx.recv(4096).decode("utf-8")
    matrix = np.array(answer.split("#"), dtype=float).reshape((agents, agents))
    return matrix

def verify_connection(raspx):
    m4 = "continue or stop"
    raspx.send(bytes(m4.encode("utf-8")))  # Send clinet model matrix request
    message = raspx.recv(4096).decode("utf-8")
    return  message

def request_id(raspx):
    m5 = "send id"
    raspx.send(bytes(m5.encode("utf-8")))  # Send clinet model matrix request
    id = raspx.recv(4096).decode("utf-8")
    return id

def main():
    port = 8080
    ip = initialize_client()
    raspx = initialize_system(ip, port)

    id = request_id(raspx)

    dict_model = request_model(raspx)
    as_matrix = request_association(raspx)

    Ax = dict_model['Ax']
    Bx = dict_model['Bx']

    Ay = dict_model['Ay']
    By = dict_model['By']

    operating = True
    while operating:
        pos = request_values(raspx)
        Xi = pos["x"]
        Yi = pos["y"]

        X_new = Ax*Xi+Bx
        Y_new = Ay*Yi+By

        verify = verify_connection(raspx)
        if verify[2] == 0:
            operating = False
        else:
            update = 2*str(agents)+str(id)+str(round(X_new[id],4))+str(round(Y_new[id],4))
            sending = "True"
            while sending:
                raspx.send(bytes(update.encode("utf-8")))  # Send clinet new data
                answer = raspx.recv(4096).decode("utf-8")
                if answer == "received":
                    sending = False


main()
