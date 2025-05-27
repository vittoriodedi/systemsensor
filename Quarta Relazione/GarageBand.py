import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
from scipy.signal import find_peaks

filename1 = "diapason.wav"
filename2 = "distorta.wav"
filename3 = "pulita_semplice.wav"

data1, samplerate1 = sf.read(filename1)
data2, samplerate2 = sf.read(filename2)
data3, samplerate3 = sf.read(filename3)

def process_audio(data, samplerate):
    if data.ndim == 2:
        channel_1 = data[:, 0]
        channel_2 = data[:, 1]
        time = np.arange(len(channel_1)) / samplerate
        
        plt.figure(figsize=(10, 6))
        plt.subplot(2, 1, 1)
        plt.plot(time, channel_1, label="Canale 1")
        plt.title('Waveform - Canale 1')
        plt.xlabel('Tempo (s)')
        plt.ylabel('Ampiezza')
        plt.grid(True)
        
        plt.subplot(2, 1, 2)
        plt.plot(time, channel_2, label="Canale 2", color='r')
        plt.title('Waveform - Canale 2')
        plt.xlabel('Tempo (s)')
        plt.ylabel('Ampiezza')
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    N = len(channel_1)
    T = 1.0 / samplerate
    yf = fft(channel_1)
    xf = fftfreq(N, T)[:N // 2]


    power = np.abs(yf[:N // 2]) ** 2

    plt.figure(figsize=(10, 6))
    plt.plot(xf, power, label="Potenza")
    plt.title('Potenza della FFT')
    plt.xlabel('Frequenza (Hz)')
    plt.ylabel('Potenza')
    plt.grid(True)
    plt.show()


    peaks, _ = find_peaks(power, height=0.1, distance=100)
    peak_frequencies = xf[peaks]
    peak_powers = power[peaks]

    plt.figure(figsize=(10, 6))
    plt.plot(xf, power, label="Potenza")
    plt.plot(peak_frequencies, peak_powers, 'x', label="Picchi")
    plt.title('Picchi nella Potenza della FFT')
    plt.xlabel('Frequenza (Hz)')
    plt.ylabel('Potenza')
    plt.legend()
    plt.grid(True)
    plt.show()

    peak_widths = np.diff(peak_frequencies)

    def frequency_to_note(freq):
        A4_freq = 440.0
        semitone_ratio = 2 ** (1 / 12)
        semitone_distance = round(12 * np.log2(freq / A4_freq))
        notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        note = notes[semitone_distance % 12]
        octave = 4 + (semitone_distance // 12)
        return f"{note}{octave}"

    peak_notes = [frequency_to_note(f) for f in peak_frequencies]

    print("Frequenze dei picchi e le note corrispondenti:")
    for freq, note in zip(peak_frequencies, peak_notes):
        print(f"Frequenza: {freq:.2f} Hz - Nota: {note}")

    mask = np.ones(len(yf), dtype=complex)
    mask[peaks[0]] = 0

    filtered_yf = yf * mask

    filtered_data = np.real(np.fft.ifft(filtered_yf))

    return filtered_data

filtered_data1 = process_audio(data1, samplerate1)
filtered_data2 = process_audio(data2, samplerate2)
filtered_data3 = process_audio(data3, samplerate3)

sf.write('filtered_diapason.wav', filtered_data1, samplerate1)
sf.write('filtered_distorta.wav', filtered_data2, samplerate2)
sf.write('filtered_pulita_semplice.wav', filtered_data3, samplerate3)

