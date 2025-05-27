import socket
import numpy as np
import matplotlib.pyplot as plt

def square(frequency, t):
    return np.sign(np.sin(2 * np.pi * frequency * t))

fs = 512
t = np.linspace(0, 1, fs)
freq = 5 

waveform_sq = square(freq, t)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 65432))
sock.listen(1)

print("Waiting for a connection...")
connection, client_address = sock.accept()

try:
    print("Connection from", client_address)
    connection.sendall(waveform_sq.tobytes())
finally:
    connection.close()
    sock.close()