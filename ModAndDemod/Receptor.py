import sounddevice as sd
import numpy as np
import time as t
import matplotlib.pyplot as plt

recibido = []
data = []
recibiendo = False


def print_sound(indata, outdata, frames, time, status):
    # calcula la longitud del vector
    volume_norm = np.linalg.norm(indata)
    global recibiendo
    volume_norm = volume_norm * 10
    print(volume_norm)
    print("|" * int(volume_norm))
    if volume_norm > 3:
        data.append(volume_norm)
        recibiendo = True


stream = sd.Stream(callback=print_sound, samplerate=44100)
stream.start()

# Wait for user input to stop the program
input("Press Enter to stop...\n")

# Stop the audio stream and exit the program
stream.stop()

data[:] = [i // 10 for i in data]

print(f"Grafica: {data[0::10]}")
for i in range(3, len(data), 10):
    baudio = max(data[i:i + 6])
    print(f"[{i} - {i+6}], max: {baudio}, promedio {sum(data[i:i+6])/6}")
    if 36 < baudio < 45:
        recibido.append(1)
    if 10 < baudio < 33:
        recibido.append(0)

print(f"\n---Recibido: {recibido}---")

binary_string = ''.join(str(bit) for bit in recibido)
binary_characters = [binary_string[i:i+8] for i in range(0, len(binary_string), 8)]
word = ''.join(chr(int(binary_char, 2)) for binary_char in binary_characters)

print(f"Recibido: {word}")

plt.plot(data)
plt.show()
