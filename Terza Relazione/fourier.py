import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

T = 1
f = 1 / T 
t = np.linspace(0, 2 * T, 1000)
n_coefficients = 1000

def square_wave_fourier(t, T, n_coefficients):
    signal = np.zeros_like(t)
    for n in range(1, n_coefficients + 1, 2):
        signal += (4 / (np.pi * n)) * np.sin(2 * np.pi * n * t / T)
    return signal

signal = square_wave_fourier(t, T, n_coefficients)

plt.figure(figsize=(10, 6))
plt.plot(t, signal, label=f"Onda quadra con {n_coefficients} coefficienti di Fourier")
plt.title("Sintesi di un'onda quadra usando i coefficienti di Fourier")
plt.xlabel("Tempo (s)")
plt.ylabel("Ampiezza")
plt.grid(True)
plt.legend()


fs = 10000
duration = 0.02
t = np.linspace(0, duration, int(fs * duration), endpoint=False)

def sinusoidal(frequency, t):
    return np.sin(2 * np.pi * frequency * t)

def triangular(frequency, t):
    return 2 * np.abs(2 * ((t * frequency) % 1) - 1) - 1

def square(frequency, t):
    return np.sign(np.sin(2 * np.pi * frequency * t))

frequencies = [100, 200, 440]


plt.figure(figsize=(12, 10))
for i, freq in enumerate(frequencies):
    plt.subplot(3, 3, i + 1)
    plt.plot(t, sinusoidal(freq, t))
    plt.title(f"Onda Sinusoidale {freq} Hz")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Ampiezza")
    plt.grid(True)
    
    plt.subplot(3, 3, i + 4)
    plt.plot(t, triangular(freq, t))
    plt.title(f"Onda Triangolare {freq} Hz")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Ampiezza")
    plt.grid(True)
    
    plt.subplot(3, 3, i + 7)
    plt.plot(t, square(freq, t))
    plt.title(f"Onda Quadra {freq} Hz")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Ampiezza")
    plt.grid(True)
plt.tight_layout()


def frequencies_fft(fun):
    return fftfreq(len(fun), 1 / fs)

def power_spectrum(fun):
    signal_fft = fft(fun, norm="forward")
    return np.abs(signal_fft) ** 2
        
plt.figure(figsize=(12, 10))
for i, freq in enumerate(frequencies):
    plt.subplot(3, 3, i + 1)
    plt.plot(frequencies_fft(sinusoidal(freq, t)), power_spectrum(sinusoidal(freq, t)))
    plt.title(f"Trasformata Onda Sinusoidale {freq} Hz")
    plt.xlabel("Frequenza fft")
    plt.ylabel("Ampiezza")
    plt.xlim(-2000, 2000)
    plt.grid(True)
    
    plt.subplot(3, 3, i + 4)
    plt.plot(frequencies_fft(triangular(freq, t)), power_spectrum(triangular(freq, t)))
    plt.title(f"Trasformata Onda Triangolare {freq} Hz")
    plt.xlabel("Frequenza fft")
    plt.ylabel("Ampiezza")
    plt.xlim(-2000, 2000)
    plt.grid(True)
    
    plt.subplot(3, 3, i + 7)
    plt.plot(frequencies_fft(square(freq, t)), power_spectrum(square(freq, t)))
    plt.title(f"Trasformata Onda Quadra {freq} Hz")
    plt.xlabel("Frequenza fft")
    plt.ylabel("Ampiezza")
    plt.xlim(-2000, 2000)
    plt.grid(True)
plt.tight_layout()


plt.figure(figsize=(12, 10))
plt.plot(t, sinusoidal(frequencies[0], t) + sinusoidal(frequencies[1], t) + sinusoidal(frequencies[2], t), color='b')
plt.title("somma di tre onde sinusoidali")
plt.xlabel("Tempo (s)")
plt.ylabel("Ampiezza")
plt.grid(True)
plt.tight_layout()


plt.figure(figsize=(12, 10))
plt.plot(frequencies_fft(sinusoidal(frequencies[0] + frequencies[1] + frequencies[2], t)), power_spectrum(sinusoidal(frequencies[0], t) + sinusoidal(frequencies[1], t) + sinusoidal(frequencies[2], t)), color='b')
plt.title("somma di tre onde sinusoidali")
plt.xlabel("Frequenza fft")
plt.xlim(-2000, 2000)
plt.ylabel("Ampiezza")
plt.grid(True)
plt.tight_layout()

plt.show()