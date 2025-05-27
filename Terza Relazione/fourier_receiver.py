import socket
import numpy as np
import matplotlib.pyplot as plt

fs = 512
t = np.linspace(0, 1, fs)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 65432))

data_sq = sock.recv(4096)
waveform_sq = np.frombuffer(data_sq, dtype=np.float64)

plt.figure(figsize=(10, 6))
plt.plot(t, waveform_sq)
plt.title("Received Square Waveform")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.grid(True)

plt.show()

sock.close()