import vlc
import time
import tkinter as tk
from tkinter import Scale, simpledialog
import os
import json

# Archivo para guardar la URL
url_file = "stream_url.json"

# Cargar la URL guardada
def load_url():
    if os.path.exists(url_file):
        with open(url_file, 'r') as file:
            data = json.load(file)
            return data.get("url", "")
    return ""

# Guardar la URL
def save_url(url):
    with open(url_file, 'w') as file:
        json.dump({"url": url}, file)

# Crear una instancia de VLC
instance = vlc.Instance("--network-caching=1")  # Ajustar el buffer a 1 ms
player = instance.media_player_new()

def play_stream(url):
    media = instance.media_new(url)
    player.set_media(media)
    player.play()

def toggle_play_pause():
    if player.is_playing():
        player.pause()
        play_pause_button.config(text="Play")
    else:
        player.play()
        play_pause_button.config(text="Pause")

def set_volume(value):
    player.audio_set_volume(int(value))

def close_app():
    player.stop()
    root.destroy()

def check_connection():
    while True:
        state = player.get_state()
        if state in [vlc.State.Ended, vlc.State.Error]:
            update_connection_status(False)
            print("Desconectado. Intentando reconectar...")
            play_stream(stream_url)  # Reconectar al stream
        else:
            update_connection_status(True)
        time.sleep(1)

def update_connection_status(connected):
    if connected:
        connection_indicator.config(bg="green")
        connection_status_label.config(text="Conectado", fg="green")
    else:
        connection_indicator.config(bg="red")
        connection_status_label.config(text="Sin conexión. Reconectando...", fg="red")

# Crear la ventana principal
root = tk.Tk()
root.title("Reproductor de Streaming")
root.geometry("400x300")
root.configure(bg="#2E2E2E")

# Etiqueta de título
title_label = tk.Label(root, text="Reproductor de Streaming", bg="#2E2E2E", fg="#FFFFFF", font=("Helvetica", 18))
title_label.pack(pady=10)

# Indicador de conexión
connection_frame = tk.Frame(root, bg="#2E2E2E")
connection_frame.pack(pady=10)

connection_indicator = tk.Label(connection_frame, width=2, height=1, bg="red")
connection_indicator.pack(side=tk.LEFT)

connection_status_label = tk.Label(connection_frame, text="Sin conexión", bg="#2E2E2E", fg="red", font=("Helvetica", 12))
connection_status_label.pack(side=tk.LEFT, padx=5)

# Comprobar si hay un URL guardado
stream_url = load_url()
if stream_url:
    play_stream(stream_url)
    change_button = tk.Button(root, text="Cambiar URL", command=lambda: change_url(), bg="#4CAF50", fg="#FFFFFF", borderwidth=0, padx=10, pady=5)
    change_button.pack(pady=10)
else:
    url_input = simpledialog.askstring("Input", "Por favor, ingresa la URL del stream:", parent=root)
    if url_input:
        save_url(url_input)
        play_stream(url_input)

# Función para cambiar el URL
def change_url():
    new_url = simpledialog.askstring("Cambiar URL", "Por favor, ingresa la nueva URL del stream:", parent=root)
    if new_url:
        save_url(new_url)
        play_stream(new_url)

# Botón de Play/Pause
play_pause_button = tk.Button(root, text="Pause", command=toggle_play_pause, bg="#4CAF50", fg="#FFFFFF", borderwidth=0, padx=10, pady=5)
play_pause_button.pack(pady=10)

# Control de volumen
volume_scale = Scale(root, from_=0, to=100, orient='horizontal', label='Volumen', command=set_volume, bg="#2E2E2E", fg="#FFFFFF")
volume_scale.set(100)  # Volumen inicial al 100%
volume_scale.pack(pady=10)

# Botón de Cerrar
close_button = tk.Button(root, text="Cerrar", command=close_app, bg="#F44336", fg="#FFFFFF", borderwidth=0, padx=10, pady=5)
close_button.pack(pady=10)

# Iniciar el hilo de verificación de conexión
import threading
connection_thread = threading.Thread(target=check_connection, daemon=True)
connection_thread.start()

# Iniciar la interfaz
root.mainloop()