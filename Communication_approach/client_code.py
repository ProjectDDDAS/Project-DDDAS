import socket
import numpy as np
from ping3 import ping

def detect_agents(addrs = None):
    if addrs == None:
        host = "192.168.0."
        addrs = []
        for i in range(100, 105):
            hostname = host + str(i)  # example
            response = ping(hostname)
            if type(response) == float:
                addrs.append(hostname)
                print(hostname)
    return addrs

def initialize_server(addrs):
    port = 8080 #convention
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    welcome_message = "welcome"
    count = 0
    num_agents = len(addrs)
    agents = {}
    finding_agents = True

    while finding_agents:
        for each_address in addrs:
            server.connect((each_address, port))  # Connect to the agent
            server.send(bytes(welcome_message.encode("utf-8")))  # Send welcome message
            answer = server.recv(4096).decode("utf-8")
            print(answer)
            if answer == "Firts connection successful":
                agents[addrs] = {"Id": answer} #Save agent info in a dict
        if len(agents) == num_agents:
            finding_agents = False
    return agents

def main():
    addrs = None
    print("Looking for agents...")
    ip_dir = detect_agents(addrs)
    print("Agents detected: \n", ip_dir)
    Ids = initialize_server(ip_dir)
    print("Dictionary with Ids: \n", Ids)
    
    # Initialize systems
    Ax1 = np.array([[1, 2, 3], [1, 2, 3], [1, 2, 3]])
    Ax2 = np.array([[1, 2, 3], [1, 2, 3], [1, 2, 3]])
    Ax3 = np.array([[1, 2, 3], [1, 2, 3], [1, 2, 3]])

    Bx1 = np.array([[1], [1], [1]])
    Bx2 = np.array([[1], [1], [1]])
    Bx3 = np.array([[1], [1], [1]])

    Ay1 = np.array([[1, 2, 3], [1, 2, 3], [1, 2, 3]])
    Ay2 = np.array([[1, 2, 3], [1, 2, 3], [1, 2, 3]])
    Ay3 = np.array([[1, 2, 3], [1, 2, 3], [1, 2, 3]])

    By1 = np.array([[1], [1], [1]])
    By2 = np.array([[1], [1], [1]])
    By3 = np.array([[1], [1], [1]])  # La matriz de adyacencia debe ir implícita en estas ecuaciones (sistemas L.T.I)

    A = np.array([Ax1, Ax2, Ax3, Ay1, Ay2, Ay3])
    B = np.array([Bx1, Bx2, Bx3, By1, By2, By3])

    initialize_server(ip_dir, num_agents)
    
main()