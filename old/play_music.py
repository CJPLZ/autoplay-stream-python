import vlc
import time
import tkinter as tk
from tkinter import Scale, simpledialog
import os
import json
import requests  # Necesitarás instalar requests: pip install requests
import threading  # Asegúrate de importar el módulo threading

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
instance = vlc.Instance("--network-caching=2000")  # Ajustar el buffer a 2000 ms
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

def check_internet_connection():
    try:
        requests.get("http://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False

def check_stream_accessible(url):
    try:
        response = requests.head(url, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

def check_connection():
    global stream_url
    while True:
        internet_connected = check_internet_connection()
        
        if internet_connected:
            state = player.get_state()
            if state in [vlc.State.Ended, vlc.State.Error]:
                update_connection_status(True, False)  # Conectado a Internet pero no al stream
                print("Desconectado del stream. Intentando reconectar...")
                time.sleep(5)  # Espera 5 segundos antes de intentar reconectar

                # Detener el reproductor antes de intentar reconectar
                player.stop()  
                
                # Verificar si el stream es accesible antes de intentar reproducirlo
                if check_stream_accessible(stream_url):
                    play_stream(stream_url)  # Reconectar al stream
                else:
                    print("El stream no está disponible en este momento.")
            else:
                update_connection_status(True, True)  # Conectado a Internet y al stream
        else:
            update_connection_status(False, False)  # Sin conexión a Internet
        time.sleep(1)

def update_connection_status(internet_connected, stream_connected):
    if internet_connected:
        connection_indicator.config(bg="green")
        connection_status_label.config(text="Conectado a Internet", fg="green")
    else:
        connection_indicator.config(bg="red")
        connection_status_label.config(text="Sin conexión a Internet", fg="red")

    if stream_connected:
        stream_status_label.config(text="Conectado al stream", fg="green")
    else:
        stream_status_label.config(text="Desconectado del stream", fg="red")

# Crear la ventana principal
root = tk.Tk()
root.title("Reproductor de Streaming")
root.geometry("400x300")
root.configure(bg="#2E2E2E")

# Etiqueta de título
title_label = tk.Label(root, text="Reproductor de Streaming", bg="#2E2E2E", fg="#FFFFFF", font=("Helvetica",  18))
title_label.pack(pady=10)

# Indicador de conexión
connection_frame = tk.Frame(root, bg="#2E2E2E")
connection_frame.pack(pady=10)

connection_indicator = tk.Label(connection_frame, width=2, height=1, bg="red")
connection_indicator.pack(side=tk.LEFT)

connection_status_label = tk.Label(connection_frame, text="Sin conexión a Internet", bg="#2E2E2E", fg="red", font=("Helvetica", 12))
connection_status_label.pack(side=tk.LEFT, padx=5)

stream_status_label = tk.Label(root, text="Desconectado del stream", bg="#2E2E2E", fg="red", font=("Helvetica", 12))
stream_status_label.pack(pady=5)

# Comprobar si hay un URL guardado
stream_url = load_url()
if stream_url:
    play_stream(stream_url)
    change_button = tk.Button(root, text="Cambiar URL", command=lambda : change_url(), bg="#4CAF50", fg="#FFFFFF", borderwidth=0, padx=10, pady=5)
    change_button.pack(pady=10)
else:
    url_input = simpledialog.askstring("Input", "Por favor, ingresa la URL del stream:", parent=root)
    if url_input:
        save_url(url_input)
        play_stream(url_input)

# Botones de control
control_frame = tk.Frame(root, bg="#2E2E2E")
control_frame.pack(pady=10)

play_pause_button = tk.Button(control_frame, text="Play", command=toggle_play_pause, bg="#4CAF50", fg="#FFFFFF", borderwidth=0, padx=10, pady=5)
play_pause_button.pack(side=tk.LEFT, padx=5)

stop_button = tk.Button(control_frame, text="Stop", command=close_app, bg="#FF0000", fg="#FFFFFF", borderwidth=0, padx=10, pady=5)
stop_button.pack(side=tk.LEFT, padx=5)

volume_slider = Scale(control_frame, from_=0, to=100, orient=tk.HORIZONTAL, command=set_volume, bg="#2E2E2E", fg="#FFFFFF")
volume_slider.set(50)
volume_slider.pack(side=tk.LEFT, padx=5)

# Iniciar la comprobación de conexión
check_connection_thread = threading.Thread(target=check_connection)
check_connection_thread.daemon = True
check_connection_thread.start()

root.mainloop()