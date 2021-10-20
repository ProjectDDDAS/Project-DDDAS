import socket
import numpy as np

def initialize_server(addrs, num_agents):
    port = 8080 #convention
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    welcome_message = "welcome"
    count = 0
    agents = {}
    finding_agents = True
    while finding_agents:
        for each_addres in addrs:
            server.connect((each_addres, port))  # Connect to the agent
            server.send(bytes(welcome_message.encode("utf-8")))  # Send welcome message
            answer = server.recv(4096).decode("utf-8")
            if answer == "Firts connection successful":
                count += 1
                agents[addrs] = {"Id": count} #Save agent info in a dict
        if len(agents) == num_agents:
            finding_agents = False
    return agents

def main():
    num_agents = 3  # Number of agents in the system
    ip_dir = ["domain 1", "domain 2", "domain 3"]  # Raspberry pie domains for TCP/IP connection

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